import csv

with open('v.csv', 'rb') as f:
    r = csv.reader(f, delimiter=';', quotechar='|')
    for row in r:
        print ', '.join(row)
