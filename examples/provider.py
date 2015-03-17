#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to get the concept of
'STYLE-traditioneel'.
'''

import responses

from skosprovider_atramhasis.providers import AtramhasisProvider
from tests import init_responses


def main():
    #you can adapt this example by using the base_url of another atramhasis-instance and provide an available scheme_id and id within this conceptscheme
    provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://glacial-bastion-1106.herokuapp.com', scheme_id='TREES')
    id = 1

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
    init_responses()
    main()
