#!/usr/bin/env python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urllib
import re
import json
import pprint


class PartidosHTMLParser(HTMLParser):

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

        if tag != 'strong':
            self.lasttag = None
            self.lastattrs = None

    def handle_data(self, data):
        if self.lasttag == 'td' or (self.lasttag == 'strong' and len(remove_spaces(data)) > 1) or self.lasttag == 'a' or self.lasttag == 'span' \
         :

            #if 'align' in self.lastattrs:
            #    print self.lastattrs

            text = remove_spaces(data)
            
            if (len(text) > 0):
                self.actual.append(text)

    def parse(self, url):
        self.feed(url.read())
        return self.all
        

def remove_spaces(string):
    return re.sub(' +', ' ', string)

def create_item_dict(array):
    dic = {}
    if (len(array) == 6):
        dic = {
            'id': int(array[0]),
            'sigla': array[1],
            'name': array[2],
            'deferimento': array[3],
            'presidente_nacional': array[4],
            'numero': array[5]
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

def get_partidos():
    url = urllib.urlopen('http://www.tse.jus.br/partidos/partidos-politicos/registrados-no-tse')
    parser = PartidosHTMLParser()
    data = parser.parse(url)
    return create_json(data)

if __name__ == '__main__':
    print get_partidos()
    

    