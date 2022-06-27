import csv
import os
import json
from helpers import get_redfin_csv_address

redfin_csv_dir = f'{os.getcwd()}/extractor/redfin/redfin_csv'
jsonFilePath = f'{os.getcwd()}/extractor/redfin/redfin_json/redfin.json'

jsonArray = []

for root, dirs, files in os.walk(redfin_csv_dir, topdown=False):
    for filename in files:
        print(filename)
        with open(f'{redfin_csv_dir}/{filename}', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                jsonArray.append(row)
                print(get_redfin_csv_address(row))


with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
    jsonString = json.dumps(jsonArray, indent=4)
    jsonf.write(jsonString)