#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to find concepts with
'kerk' in their label
'''

from skosprovider_atramhasis.providers import AtramhasisProvider

def main():
    # you can adapt this example by using the base_url of another
    # atramhasis-instance and provide an available scheme_id and
    # the keyword to search for
    provider = AtramhasisProvider(
        {'id': 'vioe-erfgoedtypes)'},
        base_url='https://thesaurus.onroerenderfgoed.be',
        scheme_id='ERFGOEDTYPES')

    keyword = 'kerk'

    results = provider.find({
        'label': keyword,
        'type': 'concept'
    })


    print('Results')
    print('------')
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
