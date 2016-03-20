#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup
import requests

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


def main():
    request = urllib2.Request('http://pokemondb.net/pokedex/national')
    response = urllib2.urlopen(request)

    soup = BeautifulSoup(response.read())
    names = []
    add_normal = ['deoxys', 'rotom']

    for link in soup.findAll('a', {'class': 'ent-name'}):
        names.append(link.text)

    for name in names:
        parsed_name = name.lower()
        parsed_name = parsed_name.replace("'", "")
        parsed_name = parsed_name.replace(". ", "-")

        if name.find(u'\u2640') != -1:
            parsed_name = "nidoran-f"
        if name.find(u'\u2642') != -1:
            parsed_name = "nidoran-m"
        if name.find(u'\xe9') != -1:
            parsed_name = 'flabebe'
        if parsed_name in add_normal:
            parsed_name += '-normal'
        if parsed_name == 'wormadam':
            parsed_name += '-plant'
        if parsed_name == 'mime jr.':
            parsed_name = 'mime-jr'
        if parsed_name == 'giratina':
            parsed_name += '-altered'
        if parsed_name == 'shaymin':
            parsed_name += '-land'
        if parsed_name == 'darmanitan':
            parsed_name += '-standard'
        if parsed_name == 'meloetta':
            parsed_name += '-aria'
        if parsed_name == 'meowstic':
            parsed_name += '-male'
        if parsed_name == 'aegislash':
            parsed_name += '-blade'

        url = "http://img.pokemondb.net/artwork/{}.jpg".format(parsed_name)
        r = requests.get(url)
        if r.status_code != 200:
            print "error downloading {}".format(parsed_name)
        with open('img/{}.jpg'.format(parsed_name), 'wb') as f:
            f.write(r.content)

if __name__ == '__main__':
    main()