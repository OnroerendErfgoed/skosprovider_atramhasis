#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This script demonstrates using the AtramhasisProvider to print a full thesaurus
as a simple rst tree. The generated tree can be saved as a file and turned into
a pdf or imported in a python Sphinx documentation project.
'''

from skosprovider_atramhasis.providers import AtramhasisProvider

import requests

# Use to only generate the tree for certain top terms.
# TOP_CONCEPTS = None
TOP_CONCEPTS = [359]


def title(title, underline='='):
    print(title)
    print(underline * len(title))


def list(items, provider, indent=''):
    print()
    for i in items:
        tpl = '%s* <`%s <%s>`_>' if i['type'] == 'collection' else '%s* `%s <%s>`_'
        print(tpl % (indent, i['label'], i['uri']))

        child = provider.get_children_display(
            i['id'],
            language='nl-BE',
            sort='label'
        )
        if (len(child)):
            list(child, provider, indent=indent + ' ')
    print()


def main():
    # Keep cache in between runs of the script
    # Value is considered valid for 1 day
    provider = AtramhasisProvider(
        {
            'id': 'vioe-erfgoedtypes)',
            'uri': 'https://id.erfgoed.net/thesauri/erfgoedtypes'
        },
        base_url='https://thesaurus.onroerenderfgoed.be',
        scheme_id='ERFGOEDTYPES',
        cache_config={
            'cache.backend': 'dogpile.cache.dbm',
            'cache.expiration_time': 60 * 60 * 24,
            'cache.arguments.filename': 'erfgoedtypes.dbm'
        }
    )

    title(provider.concept_scheme.label('nl-BE').label)

    if len(TOP_CONCEPTS) > 0:
        top = []
        for tcid in TOP_CONCEPTS:
            tc = provider.get_by_id(tcid)
            top.append({
                'id': tc.id,
                'uri': tc.uri,
                'type': tc.type,
                'label': tc.label('nl-BE').label
            })
    else:
        top = provider.get_top_display(language='nl-BE', sort='label')

    for t in top:
        tpl = '<%s> (%s)' if t['type'] == 'collection' else '%s (%s)'
        titel = tpl % (t['label'], t['uri'])
        title(titel, underline='-')

        child = provider.get_children_display(
            t['id'],
            language='nl-BE',
            sort='label'
        )
        list(child, provider)


if __name__ == "__main__":
    main()
