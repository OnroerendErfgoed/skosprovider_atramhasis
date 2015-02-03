#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to get the concept of
'STYLE-traditioneel'.
'''

import responses

from skosprovider_atramhasis.providers import AtramhasisProvider
from tests import init_responses


@responses.activate
def main():
    provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES')

    result = provider.get_by_id(1)


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
