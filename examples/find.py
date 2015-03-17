#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to find the concepts with 'iron' in their label
'''

import responses

from skosprovider_atramhasis.providers import AtramhasisProvider
from tests import init_responses


def main():
    #you can adapt this example by using the base_url of another atramhasis-instance and provide an available scheme_id and the keyword to search for
    provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://glacial-bastion-1106.herokuapp.com', scheme_id='TREES')
    keyword = 'Lar'
    results = provider.find(
    {
        'label': keyword,
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
