# -*- coding: utf-8 -*-
'''
Utility functions for :mod:`skosprovider_atramhasis`.
'''

from skosprovider.skos import (
    Concept,
    Label,
    Note,
    ConceptScheme, Collection, dict_to_label, dict_to_note)

import logging
import sys

log = logging.getLogger(__name__)

PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    binary_type = bytes
else:  # pragma: no cover
    binary_type = str


def _split_uri(uri, index):
    return uri.strip('/').rsplit('/', 1)[index]


def text_(s, encoding='latin-1', errors='strict'):
    """ If ``s`` is an instance of ``binary_type``, return
    ``s.decode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    return s


def dict_to_thing(dict):
    #todo matches en subordinate_arrays (when mocking tests are added)
    '''
    Transform a dict with keys `label`, `type` and `language` into a
    :class:`Label`.

    If the argument passed is already a :class:`Label`, this method just
    returns the argument.
    '''
    if isinstance(dict, Concept) or isinstance(dict, Collection):
        return dict
    else:
        if 'id' in dict:
            id = dict['id']
        else:
            raise ValueError("id: No id available in dict")

        if 'type' in dict:
            type = dict['type']
        else:
            raise ValueError("type: type is not defined in dict")

        if type == 'concept':
            thing = Concept(id)
        elif type == 'collection':
            thing = Collection(id)
        else:
            raise ValueError("type: type is not valid ('concept', 'collection') in dict")
        thing.type = type
        thing.uri = dict['uri'] if 'uri' in dict else None
        thing.label = dict['label'] if 'label' in dict else None
        thing.concept_scheme = ConceptScheme(dict['label']['uri']) if 'concept_scheme' in dict else None
        if 'labels' in dict:
            thing.labels = [(dict_to_label(l)) for l in dict['labels']]
        if 'notes' in dict:
            thing.notes = [(dict_to_note(n)) for n in dict['notes']]
        if 'narrower' in dict:
            thing.narrower = [(dict_to_thing(n)) for n in dict['narrower']]
        if 'broader' in dict:
            thing.broader = [(dict_to_thing(n)) for n in dict['broader']]
        if 'related' in dict:
            thing.related = [(dict_to_thing(n)) for n in dict['related']]
        if 'member_of' in dict:
            thing.member_of = [(dict_to_thing(n)) for n in dict['member_of']]
        if 'subordinate_arrays' in dict:
            thing.subordinate_arrays = [(dict_to_thing(n)) for n in dict['subordinate_arrays']]
        if 'matches' in dict:
            matches = dict['matches']
            for match_type in thing.matchtypes:
                if match_type not in matches.keys():
                    thing.matches[match_type] = []
            # for match_type in matches.keys():
            #     if match_type in thing.matchtypes:
            #         thing.matches[match_type] = matches.get(match_type, [])
        
        return thing


