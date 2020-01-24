#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to get the concept of
'water tricks'.
'''

from skosprovider_atramhasis.providers import AtramhasisProvider

def main():
    # you can adapt this example by using the base_url of another
    # atramhasis-instance and provide an available scheme_id and
    # id within this conceptscheme
    provider = AtramhasisProvider(
        {'id': 'vioe-erfgoedtypes)'},
        base_url='https://thesaurus.onroerenderfgoed.be',
        scheme_id='ERFGOEDTYPES')
    id = 1524

    result = provider.get_by_id(id)


    print('Labels')
    print('------')
    for l in result.labels:
       print(l.language + ': ' + l.label + ' [' + l.type + ']')

    print('Notes')
    print('-----')
    for n in result.notes:
        print(n.language + ': ' + n.note + ' [' + n.type + ']')


if __name__ == "__main__":
    main()
