import os
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laptops.settings")
import django
django.setup()
import csv

from django.db import transaction

from laptops_store.models import *


def get_resolution(res_text):
    resolution_match = re.search(r"(\d{3,4})x(\d{3,4})", res_text)
    w, h = None, None
    if resolution_match:
        w = int(resolution_match.group(1))
        h = int(resolution_match.group(2))
    else:
        print(f"No resolution for {res_text}")
    return w, h


def get_ram(ram_txt):
    ram_match = re.search(r".*(\d+)GB", ram_txt)
    if ram_match:
        ram_gb = ram_match.group(1)
    else:
        print(f"No RAM GB found for {ram_txt}")
    return ram_gb




def load_laptops():
    with open('data/laptops.csv') as f:
        # for line in f:
        #     cells = line.split(",")
        #     cells[0]
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
                res_w = get_resolution(row[5][0])
                res_h = get_resolution(row[5][1])
                cpu_field = row[6]
                ram_gb_field = get_ram(row[7])

                gpu_field = row[9]
                os_field = row[10]
                weight_field = float(row[11].replace('kg', ''))
                price_euro = float(row[12])



            except Exception as e:
                print(f"Error parsing {row}: {e}")


            with transaction.atomic():
                existing_manufacturers = Manufacturer.objects.all()

                found_manufacturer = None
                for m in existing_manufacturers:
                    if m.name == manufacturer_field:
                        found_manufacturer = m

                if not found_manufacturer:
                    found_manufacturer = Manufacturer(name=manufacturer_field)
                    found_manufacturer.save()
                    # print(f"saved {manufacturer_field}")

                laptop = Laptop(id=id_field,
                                manufacturer = found_manufacturer,
                                product_name=name_field,
                                type_name=type_field,
                                inches=inches_field,
                                resolution_w=res_w,
                                resolution_h=res_h,
                                cpu=cpu_field,
                                ram_gb=ram_gb_field,
                                gpu=gpu_field,
                                os=os_field,
                                weight_kg=weight_field,
                                price_euro=price_euro,
                                stock_amnt=id_field % 10
                                )
                laptop.save()



if __name__ == '__main__':
    # setup_django()
    load_laptops()