import os
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laptops.settings")
import django
django.setup()
import csv

from django.db import transaction

from laptops_store.models import *


def get_resolution(res_text):
    resolution_match = re.search(r".*(\d{3,4})x(\d{3,4}).*", res_text)
    w, h = None, None
    if resolution_match:
        w = resolution_match.group(1)
        h = resolution_match.group(2)
    else:
        print(f"No resolution for {res_text}")
    return w, h


def load_laptops():
    with open('data/laptops.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue

            try:
                id_field = int(row[0])
                manufacturer_field = row[1]
                name_field = row[2]
                type_field = row[3]
                inches_field = float(row[4])
                res_w = get_resolution(row[5])
                res_h = get_resolution(row[5])
            except Exception as e:
                print(f"Error parsing {row}: {e}")


            with transaction.atomic():
                existing_manufacturers = Manufacturer.objects.all()

                found_manufacturer = None
                for m in existing_manufacturers:
                    if m.name == manufacturer_field:
                        found_manufacturer = m

                if not found_manufacturer:
                    manufacturer = Manufacturer(manufacturer_field)
                    # manufacturer.save()
                    # print(f"saved {manufacturer_field}")

                # laptop = Laptop(id = )



if __name__ == '__main__':
    # setup_django()
    load_laptops()