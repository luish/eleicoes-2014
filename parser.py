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
         or (self.lasttag == 'div' and 'align' in self.lastattrs):

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

def create_json(array):
    if (len(array) == 6):
        return json.dumps(array)
    return None

def get_partidos():
    url = urllib.urlopen('http://www.tse.jus.br/partidos/partidos-politicos/registrados-no-tse')
    parser = PartidosHTMLParser()
    data = parser.parse(url)

    pp = pprint.PrettyPrinter(indent=4)

    for partido in data:
        p = create_json(partido)
        pp.pprint(p)

if __name__ == '__main__':
    get_partidos()
    

    