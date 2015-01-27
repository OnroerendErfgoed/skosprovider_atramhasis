#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to find the concepts with 'iron' in their label
'''

from skosprovider_atramhasis.providers import AtramhasisProvider

periodprovider = AtramhasisProvider(
    {'id': 'Atramhasis'},
    scheme_uri='atramhasis/atramhasis'
)

results = periodprovider.find(
    {
        'label': 'iron',
        'type': 'concept'
    }
)

print('Results')
print('------')
for result in results:
    print(result)
