from __future__ import print_function

import csv
import os
from glob import glob

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из csv в db.'

    def handle(self, *args, **options):
        for csv_file in glob('../../data/*.csv'):
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if os.path.basename(csv_file) == os.path.basename(
                            r'../data/ingredients.csv'):
                        ingredient, created = Ingredient.objects.update_or_create(
                            name=row['name'],
                            measurement_unit=row['measurement_unit']
                        )
