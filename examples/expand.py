#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to expand a concept
'''

from skosprovider_atramhasis.providers import AtramhasisProvider


def main():
    # you can adapt this example by using the base_url of another
    # atramhasis-instance and provide an available scheme_id and the id
    # within this concept scheme to expand
    provider = AtramhasisProvider(
        {'id': 'vioe-erfgoedtypes)'},
        base_url='https://thesaurus.onroerenderfgoed.be',
        scheme_id='ERFGOEDTYPES')
    id = 63 # Id for auxiliary buildings

    results = provider.expand(id)

    print('Results')
    print('------')
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
