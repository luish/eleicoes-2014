import csv
import json
import urllib2

estados = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
#cargos = ["gov","vice_gov","sen","sen_sup_1","sen_sup_2","dep_fed","dep_est"]
cargos = ["gov", "sen"]

folder = 'data/candidatos/csv/'

def get_item_data(estado, cargo):
    filename = folder + estado + '/' + cargo + '.csv'
    
    with open(filename, 'rb') as f:
        r = csv.reader(f, delimiter=';', quotechar='|')
        data = []
        indexes = None

        i = 0
        for row in r:
            if i > 0:
                data.append(row)
            i += 1

        return data

def create_item_dict(array):
    dic = {}
    if (len(array) == 7):
        dic = {
            'nome': array[0].decode('utf-8').lower().title(),
            'nome_urna': array[1].decode('utf-8').lower().title(),
            'cargo': array[2].decode('utf-8').lower().title(),
            'numero': array[3],
            'partido': array[4],
            'situacao': array[5].decode('utf-8').lower().title(),
            'coligacao': array[6].decode('utf-8')
        }

        return dic;

    return None

def get_candidates(estado, cargo):
    array = get_item_data(estado, cargo)
    candidates = []

    for cand in array:
        dic = create_item_dict(cand)
        if dic:
            candidates.append(dic)

    return json.dumps(candidates)
