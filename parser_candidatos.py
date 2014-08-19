#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urllib
import re
import json


class CandidatosHTMLParser(HTMLParser):

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
            print self.actual
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
        

def remove_spaces(string):
    s = re.sub('[\n\r]+', '', string)
    s = re.sub(' +', ' ', s)
    if len(s) == 1:
        s = ""
    return s

def create_item_dict(array):
    dic = {}
    if (len(array) == 8):
        dic = {
            'id': array[0],
            'url': array[1],
            'nome': array[2].decode('utf-8').lower().title(),
            'nome_urna': array[3],
            'numero': array[4],
            'situacao': array[5],
            'partido': array[6],
            'coligacao': array[7],
        }

        return dic;

    return None

def create_json(array):
    partidos = []
    for partido in array:
        dic = create_item_dict(partido)
        if dic:
            partidos.append(dic)

    return json.dumps(partidos)


def get_candidates():
    url = urllib.urlopen('http://divulgacand2014.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/BR/candidatos/cargo/1')
    parser = CandidatosHTMLParser()
    data = parser.parse(url)
    return create_json(data)


if __name__ == '__main__':
    print get_candidates()
