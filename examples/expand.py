#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to expand a concept
'''

from skosprovider_atramhasis.providers import AtramhasisProvider

periodprovider = AtramhasisProvider(
    {'id': 'Atramhasis'},
    scheme_uri='atramhasis/atramhasis'
)

results = periodprovider.expand('PM')

print('Results')
print('------')
for result in results:
    print(result)
