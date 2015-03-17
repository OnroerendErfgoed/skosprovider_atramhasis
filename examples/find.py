#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to find the concepts with 'iron' in their label
'''

import responses

from skosprovider_atramhasis.providers import AtramhasisProvider
from tests import init_responses


def main():
    provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://glacial-bastion-1106.herokuapp.com', scheme_id='TREES')

    results = provider.find(
    {
        'label': 'Lar',
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
