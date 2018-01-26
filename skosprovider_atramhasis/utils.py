# -*- coding: utf-8 -*-
'''
Utility functions for :mod:`skosprovider_atramhasis`.
'''

from skosprovider.skos import (
    Concept,
    ConceptScheme, Collection,
    dict_to_label, dict_to_note, dict_to_source)

import logging
import sys

log = logging.getLogger(__name__)

PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    binary_type = bytes
else:  # pragma: no cover
    binary_type = str


def text_(s, encoding='latin-1', errors='strict'):
    """ If ``s`` is an instance of ``binary_type``, return
    ``s.decode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    return s


def dict_to_thing(dict):
    '''
    Transform a dict into a
    :class:`Concept` or :class:`Collection` .

    If the argument passed is already a :class:`Concept` or :class:`Collection`, this method just
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
            if 'subordinate_arrays' in dict:
                thing.subordinate_arrays = [(dict_to_thing(n)) for n in dict['subordinate_arrays']]
            if 'matches' in dict:
                matches = dict['matches']
                for match_type in thing.matchtypes:
                    if match_type in matches:
                        thing.matches[match_type] = matches[match_type]
        elif type == 'collection':
            thing = Collection(id)
            if 'superordinates' in dict:
                thing.superordinates = [(dict_to_thing(n)) for n in dict['superordinates']]
            if 'members' in dict:
                thing.members = [(dict_to_thing(n)) for n in dict['members']]
        else:
            raise ValueError("type: type is not valid ('concept', 'collection') in dict")
        thing.type = type
        thing.uri = dict['uri'] if 'uri' in dict else None
        thing.concept_scheme = ConceptScheme(dict['concept_scheme']) if 'concept_scheme' in dict else None
        if 'labels' in dict:
            thing.labels = [(dict_to_label(l)) for l in dict['labels']]
        if 'notes' in dict:
            thing.notes = [(dict_to_note(n)) for n in dict['notes']]
        if 'sources' in dict:
            thing.sources = [(dict_to_source(n)) for n in dict['sources']]
        if 'narrower' in dict:
            thing.narrower = [(dict_to_thing(n)) for n in dict['narrower']]
        if 'broader' in dict:
            thing.broader = [(dict_to_thing(n)) for n in dict['broader']]
        if 'related' in dict:
            thing.related = [(dict_to_thing(n)) for n in dict['related']]
        if 'member_of' in dict:
            thing.member_of = [(dict_to_thing(n)) for n in dict['member_of']]
        return thing


