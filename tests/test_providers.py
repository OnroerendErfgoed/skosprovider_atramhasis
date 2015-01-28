#!/usr/bin/python
# -*- coding: utf-8 -*-

from skosprovider_atramhasis.providers import (
    AtramhasisProvider
)
from skosprovider.exceptions import ProviderUnavailableException
import unittest

class AtramhasisProviderTests(unittest.TestCase):


    def test_default_provider(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES')
        self.assertEqual(provider.base_scheme_uri, 'http://localhost:6543/conceptschemes')
        self.assertEqual(provider.scheme_id, 'STYLES')

    def test_scheme_uri_not_available(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6544/conceptschemes/STYLES')
        self.assertRaises(ProviderUnavailableException, provider.get_by_id, 1)

    def test_get_top_concepts_provider(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES')
        self.assertEqual(len(provider.get_top_concepts()), 51)

    def test_get_by_id_concept(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES').get_by_id('1')
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


    def test_get_by_id_nonexistant_id(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES').get_by_id('123')
        self.assertFalse(concept)

    def test_get_by_uri(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES').get_by_uri('http://localhost:6543/conceptschemes/STYLES/c/1')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'urn:x-vioe:styles:1')
        self.assertEqual(concept['id'], 1)

    def test_get_all(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES')
        self.assertEqual(len(provider.get_all()), 71)

    def test_get_top_display(self):
        top_atramhasis_display = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES').get_top_display()
        self.assertIsInstance(top_atramhasis_display, list)
        self.assertGreater(len(top_atramhasis_display), 0)
        keys_first_display = top_atramhasis_display[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        #self.assertIn('1', [label['label'] for label in top_atramhasis_display])

    def test_get_top_concepts(self):
        top_atramhasis_concepts = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES').get_top_concepts()
        self.assertIsInstance(top_atramhasis_concepts, list)
        self.assertGreater(len(top_atramhasis_concepts), 0)

    def test_get_childeren_display(self):
        childeren_atramhasis = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/MATERIALS').get_children_display(8)
        self.assertIsInstance(childeren_atramhasis, list)
        self.assertGreater(len(childeren_atramhasis), 0)
        keys_first_display = childeren_atramhasis[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn("aluminium", [label['label'] for label in childeren_atramhasis])



    def test_find_with_collection_all(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/MATERIALS').find({'type': 'concept', 'collection': {'id': '0', 'depth': 'all'}})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        self.assertEquals(len(r), 45)
        keys_first_display = r[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn("aluminium", [label['label'] for label in r])
        for res in r:
            self.assertEqual(res['type'], 'concept')

    def test_find_with_collection_members(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/MATERIALS').find({'type': 'concept', 'collection': {'id': '0', 'depth': 'members'}})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        self.assertEquals(len(r), 10)
        keys_first_display = r[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn("aardewerk", [label['label'] for label in r])
        for res in r:
            self.assertEqual(res['type'], 'concept')


    def test_find_collections(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES').find({'type': 'collection'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'collection')

    def test_find_all_concepts_collections(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/MATERIALS').find({'type': 'all'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertIn(res['type'], ['collection','concept'])


    def test_find_wrong_type(self):
        self.assertRaises(ValueError, AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES').find, {'type': 'collectie'})

    def test_find_keyword(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES').find({'label': 'mod', 'type': 'concept'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'concept')

    def test_expand(self):
        all_childeren = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES').expand(1)
        self.assertIsInstance(all_childeren, list)
        self.assertGreater(len(all_childeren), 0)
        self.assertIn('1', all_childeren)

    def test_expand(self):
        all_childeren = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/MATERIALS').expand(8)
        self.assertIsInstance(all_childeren, list)
        self.assertGreater(len(all_childeren), 0)
        self.assertIn(8, all_childeren)
        self.assertIn(48, all_childeren)

    def test_expand_invalid(self):
        all_childeren_invalid = AtramhasisProvider({'id': 'Atramhasis'}, scheme_uri='http://localhost:6543/conceptschemes/STYLES').expand('invalid')
        self.assertFalse(all_childeren_invalid)