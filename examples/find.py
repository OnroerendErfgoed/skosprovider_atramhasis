#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to find the concepts with 'iron' in their label
'''

import responses

from skosprovider_atramhasis.providers import AtramhasisProvider
from tests import init_responses


@responses.activate
def main():
    provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/MATERIALS')

    results = provider.find(
    {
        'label': 'alu',
        'type': 'concept'
    }
)


    print('Results')
    print('------')
    for result in results:
        print(result)


if __name__ == "__main__":
    init_responses()
    main()
