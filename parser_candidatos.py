#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urllib
import re
import json

URL_BASE = 'http://divulgacand2014.tse.jus.br/divulga-cand-2014/eleicao/2014/'

class ListaCandidatosHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.actual = []
        self.all = []
        self.lasttag = None
        self.lastattrs = None

    def handle_starttag(self, tag, attrs):
        self.lasttag = tag
        self.lastattrs = attrs

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.all.append(self.actual)
            self.actual = []

        if tag != 'td':
            self.lasttag = None
            self.lastattrs = None

    def handle_data(self, data):

        if self.lasttag == 'td' or (self.lasttag == 'strong' and len(remove_spaces(data)) > 1) or self.lasttag == 'a' or self.lasttag == 'span' \
         :
            if self.lastattrs and len(self.lastattrs) == 2:
                cont = False
                for attr in self.lastattrs:
                    if 'id' in attr:
                        cont = True
                    if 'href' in attr and cont:
                        self.actual.append(self.lastattrs[0][1])
                        self.actual.append(self.lastattrs[1][1])

            text = remove_spaces(data)
            
            if (len(text) > 0):
                self.actual.append(text)

    def parse(self, url):
        self.feed(url.read())
        return self.all
        


class CandidatoHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.actual = []
        self.all = []
        self.lasttag = None
        self.lastattrs = None

    def handle_starttag(self, tag, attrs):
        self.lasttag = tag
        self.lastattrs = attrs

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.all.append(self.actual)
            self.actual = []

        if tag != 'td':
            self.lasttag = None
            self.lastattrs = None

    def handle_data(self, data):

        if self.lasttag in ['td', 'th']:
            if self.lastattrs and len(self.lastattrs) == 2:
                cont = False
                for attr in self.lastattrs:
                    if 'id' in attr:
                        cont = True
                    if 'href' in attr and cont:
                        self.actual.append(self.lastattrs[0][1])
                        self.actual.append(self.lastattrs[1][1])

            text = remove_spaces(data)
            
            if (len(text) > 0):
                self.actual.append(text)

    def parse(self, url):
        self.feed(url.read())
        return self.all
        


def remove_spaces(string):
    s = re.sub('[\n\r\t]+', '', string)
    s = re.sub(' +', ' ', s)
    if len(s) == 1:
        s = ""
    return s


def create_candidate_item_dict(array):
    dic = {}

    if (len(array) > 0):

        for subarray in array:
            i = 0
            for item in subarray:
                if i % 2 == 0 and i + 1 < len(subarray):
                    dic[item] = subarray[i+1]

                i += 1

    return dic


def create_item_dict(array, estado, cargo):
    dic = {}
    if (len(array) == 8):
        dic = {
            'id': int(array[0].replace('link-', '')),
            'url': array[1],
            'nome': array[2].decode('utf-8').lower().title(),
            'nome_urna': array[3].decode('utf-8').lower().title(),
            'numero': array[4],
            'situacao': array[5],
            'partido': array[6],
            'coligacao': None if array[7] == array[6] else array[7].decode('utf-8').lower().title(),
        }

        dic['foto'] = URL_BASE + 'UF/%s/foto/%d.jpg' % (estado, dic['id'])

        return dic;

    return None

def create_json(array, estado, cargo):
    partidos = []
    for partido in array:
        dic = create_item_dict(partido, estado, cargo)
        if dic:
            partidos.append(dic)

    return json.dumps(partidos)


def get_candidates(estado, cargo):
    u = URL_BASE + 'UF/%s/candidatos/cargo/%s' % (estado, cargo)
    print u
    url = urllib.urlopen(u)
    parser = ListaCandidatosHTMLParser()
    data = parser.parse(url)
    return create_json(data, estado, cargo)


def get_candidate_url(cargo, estado, cand_id):
    if cargo and estado and cand_id:
        return URL_BASE + 'idEleicao/143/cargo/%d/UF/%s/candidato/%d' % (cargo, estado, cand_id)
    return None


if __name__ == '__main__':
    candidates = get_candidates()

    for candidate in json.loads(candidates):
        url = urllib.urlopen(get_candidate_url(1, 'BR', candidate['id']))

        parser = CandidatoHTMLParser()
        data = parser.parse(url)

        print json.dumps(candidate)
        print json.dumps(create_candidate_item_dict(data))
        print 
        print '*' * 30
        print
