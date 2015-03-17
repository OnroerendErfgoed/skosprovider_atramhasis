#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to expand a concept
'''
import responses

from skosprovider_atramhasis.providers import AtramhasisProvider
from tests import init_responses


def main():
    provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://glacial-bastion-1106.herokuapp.com', scheme_id='TREES')

    results = provider.expand(3)

    print('Results')
    print('------')
    for result in results:
        print(result)


if __name__ == "__main__":
    init_responses()
    main()
