from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.shortcuts import render, redirect

from employee_info.models import Resource, Company, Organisation, CostCenter

title = 'Vis informasjon om ansatte'


def index(request):
    return render(request, 'employee_info/index.html', {'companies': Company.objects.all(),
                                                        'title': title})


@permission_required('employee_info.view_employment')
def resource(request):
    employee_num = request.GET.get('employee')
    if not employee_num:
        employee_num = request.GET.get('value')

    company = request.GET.get('company')
    resource_id = request.GET.get('id')

    resource_obj = Resource.objects.prefetch_related('employments', 'employments__costCenter', 'employments__function', 'employments__organisation')

    if resource_id:
        try:
            resource_obj = resource_obj.get(id=resource_id)
        except Resource.DoesNotExist:
            raise Http404('Ugyldig id')

    elif employee_num and company:
        try:
            resource_obj = resource_obj.get(company__companyCode=company,
                                            resourceId=employee_num)
        except Resource.DoesNotExist:
            return render(request, 'employee_info/index.html',
                          {'companies': Company.objects.all(),
                           'error_resource':
                               'Ingen ansatt i %s med ressursnummer %s' %
                               (company, employee_num)})
    else:
        return redirect('employee_info_browser:index')

    return render(request, 'employee_info/resource.html',
                  {'resource': resource_obj,
                   'title': 'Ansatt',
                   'companies': Company.objects.all()})


@permission_required('employee_info.view_organisation')
def organisation(request):
    company = request.GET.get('company')
    organisation_num = request.GET.get('value')
    if not company:
        return render(request, 'employee_info/select_company.html', {'title': 'Velg firma',
                                                                     'companies': Company.objects.all()
                                                                     })
    elif not organisation_num:
        organisation_obj = Organisation.objects.filter(company__companyCode=company)
        organisation_obj = organisation_obj.select_related('manager', 'parent')

        return render(request, 'employee_info/select_organisation.html',
                      {'title': 'Velg organisasjonsenhet',
                       'organisations': organisation_obj,
                       'company': company})
    try:
        organisation_obj = Organisation.objects.select_related('manager', 'parent'). \
            prefetch_related('employments__resource'). \
            get(company__companyCode=company, orgId=organisation_num)

        return render(request, 'employee_info/organisation.html',
                      {'organisation': organisation_obj, 'company': company})
    except Organisation.DoesNotExist:
        return render(request, 'employee_info/index.html',
                      {'title': title,
                       'companies': Company.objects.all(),
                       'error_org':
                           'Ingen organisasjonsenhet i %s med nummer %s' %
                           (company, organisation_num)})


@permission_required('employee_info.view_costcenter')
def cost_center(request):
    company = request.GET.get('company')
    value = request.GET.get('value')
    if not company:
        return redirect('employee_info_browser:index')
    if not value:
        organisation_obj = CostCenter.objects.filter(company__companyCode=company)
        organisation_obj = organisation_obj.order_by('value')

        return render(request, 'employee_info/select_cost_center.html',
                      {'title': 'Velg ansvar i %s' % company,
                       'organisations': organisation_obj,
                       'company': company})

    try:
        cost_center_obj = CostCenter.objects.select_related('company') \
            .prefetch_related('employments__resource') \
            .get(company__companyCode=company, value=value)
    except CostCenter.DoesNotExist:
        return render(request, 'employee_info/index.html',
                      {'companies': Company.objects.all(),
                       'error_cost_center':
                           'Ingen ansvar i %s med nummer %s' %
                           (company, value)})

    return render(request, 'employee_info/cost_center.html',
                  {'relation': cost_center_obj,
                   'title': 'Ansatte på ansvar %s i %s' % (value, company)
                   })
