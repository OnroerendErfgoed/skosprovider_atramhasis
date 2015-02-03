#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to expand a concept
'''
import responses

from skosprovider_atramhasis.providers import AtramhasisProvider
from tests import init_responses


@responses.activate
def main():
    provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/MATERIALS')

    results = provider.expand(8)

    print('Results')
    print('------')
    for result in results:
        print(result)


if __name__ == "__main__":
    init_responses()
    main()
