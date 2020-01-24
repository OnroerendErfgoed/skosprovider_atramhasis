#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to get concepts with or
without cache.
'''

from skosprovider_atramhasis.providers import AtramhasisProvider
import timeit

def main():
    # you can adapt this example by using the base_url of another
    # atramhasis-instance and provide an available scheme_id and
    # id within this conceptscheme
    id = 1524

    number = 50

    # No caching
    print('Fetching without cache')
    print('----------------------')

    provider = AtramhasisProvider(
        {'id': 'vioe-erfgoedtypes)'},
        base_url='https://thesaurus.onroerenderfgoed.be',
        scheme_id='ERFGOEDTYPES'
    )

    print('%d times: %.5f\n' % (number,
        timeit.timeit(lambda: provider.get_by_id(id),number=number)))


    # Only caching during the script
    print('Fetching with in memory cache')
    print('-----------------------------')

    provider = AtramhasisProvider(
        {'id': 'vioe-erfgoedtypes)'},
        base_url='https://thesaurus.onroerenderfgoed.be',
        scheme_id='ERFGOEDTYPES',
        cache_config={
            'cache.backend' : 'dogpile.cache.memory'
        }
    )

    print('%d times: %.5f\n' % (number,
        timeit.timeit(lambda: provider.get_by_id(id),number=number)))


    # Keep cache in between runs of the script
    # Value is considered valid for 1 day
    print('Fetching with file cache')
    print('------------------------')

    provider = AtramhasisProvider(
        {'id': 'vioe-erfgoedtypes)'},
        base_url='https://thesaurus.onroerenderfgoed.be',
        scheme_id='ERFGOEDTYPES',
        cache_config={
            'cache.backend': 'dogpile.cache.dbm',
            'cache.expiration_time': 60 * 60 * 24,
            'cache.arguments.filename': 'erfgoedtypes.dbm'
        }
    )

    print('%d times: %.5f\n' % (number,
        timeit.timeit(lambda: provider.get_by_id(id),number=number)))

if __name__ == "__main__":
    main()
