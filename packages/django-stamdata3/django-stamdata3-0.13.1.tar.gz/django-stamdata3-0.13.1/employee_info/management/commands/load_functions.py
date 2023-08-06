import csv
import requests
from django.core.management.base import BaseCommand

from employee_info.models import Function


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get('https://data.ssb.no/api/klass/v1//versions/1366.csv?language=nb')
        functions = response.text.splitlines()
        reader = csv.DictReader(functions, quoting=csv.QUOTE_ALL, delimiter=';')
        for row in reader:
            if row['code'][0] == 'F':
                continue
            key = int('10' + row['code'])  # Workaround to avoid conflicts with old id
            Function.objects.update_or_create(id=key, value=row['code'], defaults={'description': row['name']})
