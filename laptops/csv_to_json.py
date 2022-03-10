import csv
import json

with open('data/laptops.csv') as f:
    cols = []
    laptops = []
    csv_reader = csv.reader(f, delimiter=',')
    for i, row in enumerate(csv_reader):
        if i == 0:
            cols = row
        else:
            laptop = {}
            laptops.append(laptop)
            for k, v in zip(cols, row):
                laptop[k] = v
with open('data/laptops.json', 'w') as f:
    json.dump(laptops, f)