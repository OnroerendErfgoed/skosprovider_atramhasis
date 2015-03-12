#!/usr/bin/python
# -*- coding: utf-8 -*-

from skosprovider_atramhasis.providers import (
    AtramhasisProvider
)
from skosprovider.exceptions import ProviderUnavailableException
import unittest
import responses
import requests
from tests import init_responses

class AtramhasisProviderTests(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     pass
    #     #init_responses()

    def setUp(self):
        init_responses()

    def test_default_provider_no_scheme_uri(self):
        self.assertRaises(ValueError, AtramhasisProvider, {'id': 'Atramhasis'})

    @responses.activate
    def test_scheme_uri_not_available(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6544/conceptschemes/STYLES')
        self.assertRaises(ProviderUnavailableException, provider.get_by_id, 1)

    @responses.activate
    def test_get_top_concepts_provider(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES')
        self.assertEqual(len(provider.get_top_concepts()), 51)

    @responses.activate
    def test_get_by_id_concept(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES').get_by_id('1')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'urn:x-vioe:styles:1')
        self.assertEqual(concept['type'], 'concept')
        self.assertIsInstance(concept['labels'], list)

        preflabels = [{'nl': 'traditioneel'}]
        preflabels_conc = [{label['language']: label['label']} for label in concept['labels']
                           if label['type'] == 'prefLabel']
        self.assertGreater(len(preflabels_conc), 0)
        for label in preflabels:
            self.assertIn(label, preflabels_conc)

    @responses.activate
    def test_get_by_id_concept_matches(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/TREES').get_by_id('2')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'urn:x-skosprovider:trees/2')
        self.assertEqual(concept['type'], 'concept')
        self.assertIsInstance(concept['labels'], list)

        preflabels = [{'en': 'The Chestnut'}]
        preflabels_conc = [{label['language']: label['label']} for label in concept['labels']
                           if label['type'] == 'prefLabel']
        self.assertGreater(len(preflabels_conc), 0)
        for label in preflabels:
            self.assertIn(label, preflabels_conc)


    @responses.activate
    def test_get_by_id_nonexistant_id(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES').get_by_id('123')
        self.assertFalse(concept)

    @responses.activate
    def test_get_by_uri(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES').get_by_uri('http://localhost/conceptschemes/STYLES/c/1')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'urn:x-vioe:styles:1')
        self.assertEqual(concept['id'], 1)

    @responses.activate
    def test_get_all(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES')
        self.assertEqual(len(provider.get_all()), 71)

    @responses.activate
    def test_unknown_concept_scheme(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/ONBEKEND')
        r = provider.get_all()
        self.assertFalse(r)
        r = provider.get_top_concepts()
        self.assertFalse(r)
        r = provider.get_children_display("100")
        self.assertFalse(r)
        r = provider.get_top_display()
        self.assertFalse(r)

    @responses.activate
    def test_get_top_display(self):
        top_atramhasis_display = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES').get_top_display()
        self.assertIsInstance(top_atramhasis_display, list)
        self.assertGreater(len(top_atramhasis_display), 0)
        keys_first_display = top_atramhasis_display[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        #self.assertIn('1', [label['label'] for label in top_atramhasis_display])

    @responses.activate
    def test_get_top_concepts(self):
        top_atramhasis_concepts = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES').get_top_concepts()
        self.assertIsInstance(top_atramhasis_concepts, list)
        self.assertGreater(len(top_atramhasis_concepts), 0)

    @responses.activate
    def test_get_childeren_display(self):
        childeren_atramhasis = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/MATERIALS').get_children_display(8)
        self.assertIsInstance(childeren_atramhasis, list)
        self.assertGreater(len(childeren_atramhasis), 0)
        keys_first_display = childeren_atramhasis[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn("aluminium", [label['label'] for label in childeren_atramhasis])

    @responses.activate
    def test_find_404(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/TREES').find({'type': 'concept', 'collection': {'id': '100', 'depth': 'all'}})
        self.assertFalse(r)
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/ONBEKEND').find({'type': 'concept'})
        self.assertFalse(r)

    @responses.activate
    def test_find_with_collection_all(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/MATERIALS').find({'type': 'concept', 'collection': {'id': '0', 'depth': 'all'}})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        keys_first_display = r[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn("aluminium", [label['label'] for label in r])
        for res in r:
            self.assertEqual(res['type'], 'concept')

    @responses.activate
    def test_find_with_collection_invalid_params(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/MATERIALS')
        self.assertRaises(ValueError, provider.find, {'type': 'concept', 'collection': {'id': '0', 'depth': 'very deep'}})
        self.assertRaises(ValueError, provider.find, {'type': 'concept', 'collection': {'depth': 'all'}})


    @responses.activate
    def test_find_with_collection_members(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/MATERIALS').find({'type': 'concept', 'collection': {'id': '0', 'depth': 'members'}})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        keys_first_display = r[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn("ijzer", [label['label'] for label in r])
        for res in r:
            self.assertEqual(res['type'], 'concept')

    @responses.activate
    def test_find_collections(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES').find({'type': 'collection'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'collection')

    @responses.activate
    def test_find_all_concepts_collections(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/MATERIALS').find({'type': 'all'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertIn(res['type'], ['collection','concept'])

    @responses.activate
    def test_find_wrong_type(self):
        self.assertRaises(ValueError, AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES').find, {'type': 'collectie'})

    @responses.activate
    def test_find_keyword(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES').find({'label': 'mod', 'type': 'concept'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'concept')

    @responses.activate
    def test_expand(self):
        all_childeren = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES').expand(1)
        self.assertIsInstance(all_childeren, list)
        self.assertGreater(len(all_childeren), 0)
        self.assertIn('1', all_childeren)

    @responses.activate
    def test_expand(self):
        all_childeren = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/MATERIALS').expand(8)
        self.assertIsInstance(all_childeren, list)
        self.assertGreater(len(all_childeren), 0)
        self.assertIn(8, all_childeren)
        self.assertIn(48, all_childeren)

    @responses.activate
    def test_expand_invalid(self):
        all_childeren_invalid = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES').expand('invalid')
        self.assertFalse(all_childeren_invalid)

    @responses.activate
    def test_request_encoding(self):
        provider =  AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost/conceptschemes/STYLES')
        response = provider._request("http://localhost/no_encoding")
        self.assertEqual(response.encoding, "utf-8")