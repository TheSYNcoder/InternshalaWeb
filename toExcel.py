from xlsxwriter import Workbook
import json
import os
import csv



with open('data.json' , 'r') as file:
    data = json.load(file)


years =[]
for year in range(1970 , 2020):
    years.append(year)

heading =[]
heading.append('NAME')
heading.append('NATIONALITY')
for year in years:
    heading.append(year)
heading.append('Overall_score')


with open('data.csv', 'a') as file:
    writer = csv.writer(file)
    writer.writerow(heading)
    file.close()
for item in data['name']:
    li = []
    for k , v in item.items():
        li.append(k)
        li.append(v['nationality'])
        for year in years:
            if str(year) in v['runinfo']['runs']:
                li.append(v['runinfo']['runs'][str(year)])
            else:
                li.append(0)
        li.append(v['runinfo']['total'])
    with open('data.csv' , 'a') as file:
        writer = csv.writer(file)
        writer.writerow(li)
        file.close()

