#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to get the concept of
'POST MEDIEVAL'.
'''

from skosprovider_atramhasis.providers import AtramhasisProvider

periodprovider = AtramhasisProvider(
    {'id': 'Atramhasis'},
    scheme_uri='atramhasis/atramhasis'
)

pm = periodprovider.get_by_id('PM')

print('Labels')
print('------')
for l in pm.labels:
   print(l.language + ': ' + l.label + ' [' + l.type + ']')

print('Notes')
print('-----')
for n in pm.notes:
    print(n.language + ': ' + n.note + ' [' + n.type + ']')
