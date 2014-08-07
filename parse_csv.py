import csv
import json

folder = 'data/candidatos/csv/MG/'
filename = folder + 'governador.csv'

with open(filename, 'rb') as f:
    r = csv.reader(f, delimiter=';', quotechar='|')
    data = []
    indexes = None

    i = 0
    for row in r:
        if i == 0:
            indexes = row
        else:
            if indexes:
                j = 0
                d = {}
                for index in indexes:
                    if (j == len(indexes) - 1)  or j == 4:
                        d[indexes[j]] = row[j]
                    else:
                        d[indexes[j]] = row[j].decode('utf-8').lower().title()
                    j += 1
                
                data.append(d)
        i += 1

    print json.dumps(data)