# -*- coding: utf-8 -*-
'''
Utility functions for :mod:`skosprovider_atramhasis`.
'''

import requests
from skosprovider.skos import (
    Concept,
    Label,
    Note,
    ConceptScheme, Collection, dict_to_label, dict_to_note)
from skosprovider.exceptions import ProviderUnavailableException

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

# def map_concept(concept_json):
#     '''
#     Map a concept from json to the database.
#
#     :param skosprovider_sqlalchemy.models.Thing concept: A concept or
#         collection as known to the database.
#     :param dict concept_json: A dict representing the json sent to our REST
#         service.
#     :param session: A :class:`sqlalchemy.orm.session.Session`.
#     :returns: The :class:`skosprovider_sqlalchemy.models.Thing` enhanced
#         with the information from the json object.
#     '''
#     concept = Concept()
#     concept.type = concept_json.get('type', None)
#     if concept.type in ('concept', 'collection'):
#         for label in concept.labels:
#             concept.labels.remove(label)
#         labels = concept_json.get('labels', [])
#         for l in labels:
#             label = Label(label=l.get('label', ''), labeltype_id=l.get('type', ''), language_id=l.get('language', ''))
#             concept.labels.append(label)
#         for note in concept.notes:
#             concept.notes.remove(note)
#         notes = concept_json.get('notes', [])
#         for n in notes:
#             note = Note(note=n.get('note', ''), notetype_id=n.get('type', ''), language_id=n.get('language', ''))
#             concept.notes.append(note)
#
#         concept.member_of.clear()
#         member_of = concept_json.get('member_of', [])
#         for memberof in member_of:
#             try:
#                 memberof_collection = db_session.query(Collection)\
#                     .filter_by(concept_id=memberof['id'], conceptscheme_id=concept.conceptscheme_id).one()
#             except NoResultFound:
#                 memberof_collection = Collection(concept_id=memberof['id'], conceptscheme_id=concept.conceptscheme_id)
#             concept.member_of.add(memberof_collection)
#
#         if concept.type == 'concept':
#             concept.related_concepts.clear()
#             related = concept_json.get('related', [])
#             for related in related:
#                 try:
#                     related_concept = db_session.query(Concept).filter_by(concept_id=related['id'],
#                                                                           conceptscheme_id=concept.conceptscheme_id).one()
#                 except NoResultFound:
#                     related_concept = Concept(concept_id=related['id'], conceptscheme_id=concept.conceptscheme_id)
#                 concept.related_concepts.add(related_concept)
#             concept.narrower_concepts.clear()
#
#             concept.broader_concepts.clear()
#             broader = concept_json.get('broader', [])
#             for broader in broader:
#                 try:
#                     broader_concept = db_session.query(Concept).filter_by(concept_id=broader['id'],
#                                                                           conceptscheme_id=concept.conceptscheme_id).one()
#                 except NoResultFound:
#                     broader_concept = Concept(concept_id=broader['id'], conceptscheme_id=concept.conceptscheme_id)
#                 concept.broader_concepts.add(broader_concept)
#             narrower = concept_json.get('narrower', [])
#             for narrower in narrower:
#                 try:
#                     narrower_concept = db_session.query(Concept).filter_by(concept_id=narrower['id'],
#                                                                            conceptscheme_id=concept.conceptscheme_id).one()
#                 except NoResultFound:
#                     narrower_concept = Concept(concept_id=narrower['id'], conceptscheme_id=concept.conceptscheme_id)
#                 concept.narrower_concepts.add(narrower_concept)
#
#             matches = []
#             matchdict = concept_json.get('matches', {})
#             for type in matchdict:
#                 db_type = type + "Match"
#                 matchtype = db_session.query(MatchType).filter_by(name=db_type).one()
#                 for uri in matchdict[type]:
#                     concept_id = concept_json.get('id', -1)
#                     try:
#                         match = db_session.query(Match).filter_by(uri=uri, matchtype_id=matchtype.name, concept_id=concept_id).one()
#                     except NoResultFound:
#                         match = Match()
#                         match.matchtype = matchtype
#                         match.uri = uri
#                     matches.append(match)
#             concept.matches = matches
#
#             concept.narrower_collections.clear()
#             narrower_collections = concept_json.get('subordinate_arrays', [])
#             for narrower in narrower_collections:
#                 try:
#                     narrower_collection = db_session.query(Collection)\
#                         .filter_by(concept_id=narrower['id'], conceptscheme_id=concept.conceptscheme_id).one()
#                 except NoResultFound:
#                     narrower_collection = Collection(concept_id=narrower['id'], conceptscheme_id=concept.conceptscheme_id)
#                 concept.narrower_collections.add(narrower_collection)
#
#         if concept.type == 'collection':
#             concept.members.clear()
#             members = concept_json.get('members', [])
#             for member in members:
#                 try:
#                     member_concept = db_session.query(Thing).filter_by(concept_id=member['id'],
#                                                                            conceptscheme_id=concept.conceptscheme_id).one()
#                 except NoResultFound:
#                     member_concept = Concept(concept_id=member['id'], conceptscheme_id=concept.conceptscheme_id)
#                 concept.members.add(member_concept)
#
#             concept.broader_concepts.clear()
#             broader_concepts = concept_json.get('superordinates', [])
#             for broader in broader_concepts:
#                 try:
#                     broader_concept = db_session.query(Concept)\
#                         .filter_by(concept_id=broader['id'], conceptscheme_id=concept.conceptscheme_id).one()
#                 except NoResultFound:
#                     broader_concept = Concept(concept_id=broader['id'], conceptscheme_id=concept.conceptscheme_id)
#                 concept.broader_concepts.add(broader_concept)
#
#     return concept

def dict_to_thing(dict):
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
        thing.label = dict['label'] if 'label' in dict else None
        labels = dict['labels'] if 'labels' in dict else None
        for l in labels:
            thing.labels.append(dict_to_label(l))
        notes = dict['notes'] if 'notes' in dict else None
        for n in notes:
            thing.notes.append(dict_to_note(n))
        thing.uri = dict['uri'] if 'uri' in dict else None
        # thing.concept_scheme = dict['concept_scheme'] if 'concept_scheme' in dict else None
        # thing.broader = dict['broader'] if 'broader' in dict else None
        # thing.label = dict['label'] if 'label' in dict else None
        # thing.narrower = dict['narrower'] if 'narrower' in dict else None
        # thing.related = dict['related'] if 'related' in dict else None
        # thing.member_of = dict['member_of'] if 'member_of' in dict else None
        # thing.subordinate_arrays = dict['subordinate_arrays'] if 'subordinate_arrays' in dict else None
        # thing.matches = {}
        # for match_type in thing.matchtypes:
        #     if match_type not in matches.keys():
        #         matches[match_type] = []
        # for match_type in matches.keys():
        #     if match_type in thing.matchtypes:
        #         thing.matches[match_type] = matches.get(match_type, [])
        
        return thing


