#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to expand a concept
'''
import responses

from skosprovider_atramhasis.providers import AtramhasisProvider
from tests import init_responses


def main():
    #you can adapt this example by using the base_url of another atramhasis-instance and provide an available scheme_id and the id within this concept scheme to expand
    provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://glacial-bastion-1106.herokuapp.com', scheme_id='TREES')
    id = 3

    results = provider.expand(id)

    print('Results')
    print('------')
    for result in results:
        print(result)


if __name__ == "__main__":
    init_responses()
    main()
