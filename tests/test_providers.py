#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from skosprovider.exceptions import ProviderUnavailableException
import responses

from skosprovider_atramhasis.providers import (
    AtramhasisProvider
)
from tests import init_responses


@unittest.skip("Tests that use the attramhasis-demo are skipped by default to avoid dependencies.")
class AtramhasisProviderDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Configure the Atramhasis parameters to run all tests in this class: 
        *base_url
        *scheme_id
        *id of a concept in scheme_id
        *id of a collection in scheme_id
        """
        cls.base_url = 'http://glacial-bastion-1106.herokuapp.com'
        cls.scheme_id = 'TREES'
        cls.concept_id = 1
        cls.concept_uri = 'urn:x-skosprovider:trees/1'
        cls.collection_id = 3
        cls.collection_uri = 'urn:x-skosprovider:trees/3'

    def test_get_top_concepts_provider(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id)
        self.assertGreater(len(provider.get_top_concepts()), 0)

    def test_get_by_id_concept(self):
        c = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).get_by_id(self.concept_id)
        c = c.__dict__
        self.assertEqual(c['uri'], self.concept_uri)
        self.assertEqual(c['type'], 'concept')
        self.assertIsInstance(c['labels'], list)

    def test_get_by_id_collection(self):
        c = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).get_by_id(self.collection_id)
        c = c.__dict__
        self.assertEqual(c['uri'], self.collection_uri)
        self.assertEqual(c['type'], 'collection')
        self.assertIsInstance(c['labels'], list)

    def test_get_by_id_nonexistant_id(self):
        c = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).get_by_id('-1')
        self.assertFalse(c)

    def test_get_by_uri_concept(self):
        c = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).get_by_uri(self.concept_uri)
        c = c.__dict__
        self.assertEqual(c['uri'], self.concept_uri)
        self.assertEqual(c['id'], self.concept_id)

    def test_get_by_uri_collection(self):
        c = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).get_by_uri(self.collection_uri)
        c = c.__dict__
        self.assertEqual(c['uri'], self.collection_uri)
        self.assertEqual(c['id'], self.collection_id)

    def test_get_all(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id)
        self.assertGreater(len(provider.get_all()), 0)

    def test_get_top_display(self):
        top_atramhasis_display = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url,
                                                    scheme_id=self.scheme_id).get_top_display()
        self.assertIsInstance(top_atramhasis_display, list)
        self.assertGreater(len(top_atramhasis_display), 0)
        keys_first_display = top_atramhasis_display[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)

    def test_get_top_concepts(self):
        top_atramhasis_concepts = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url,
                                                     scheme_id=self.scheme_id).get_top_concepts()
        self.assertIsInstance(top_atramhasis_concepts, list)
        self.assertGreater(len(top_atramhasis_concepts), 0)

    def test_get_childeren_display(self):
        childeren_atramhasis = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url,
                                                  scheme_id=self.scheme_id).get_children_display(self.collection_id)
        self.assertIsInstance(childeren_atramhasis, list)
        self.assertGreater(len(childeren_atramhasis), 0)
        keys_first_display = childeren_atramhasis[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)

    def test_find_404(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).find(
            {'type': 'concept', 'collection': {'id': '-1', 'depth': 'all'}})
        self.assertFalse(r)
        self.assertRaises(Exception, AtramhasisProvider, {'id': 'Atramhasis'}, base_url=self.base_url,
                          scheme_id='ONBEKEND')

    def test_find_with_collection_all(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).find(
            {'type': 'concept', 'collection': {'id': self.collection_id, 'depth': 'all'}})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        keys_first_display = r[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        for res in r:
            self.assertEqual(res['type'], 'concept')

    def test_find_with_collection_invalid_params(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id)
        self.assertRaises(ValueError, provider.find,
                          {'type': 'concept', 'collection': {'id': self.collection_id, 'depth': 'very deep'}})
        self.assertRaises(ValueError, provider.find, {'type': 'concept', 'collection': {'depth': 'all'}})

    def test_find_with_collection_members(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).find(
            {'type': 'concept', 'collection': {'id': self.collection_id, 'depth': 'members'}})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        keys_first_display = r[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        for res in r:
            self.assertEqual(res['type'], 'concept')

    def test_find_collections(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).find(
            {'type': 'collection'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'collection')

    def test_find_all_concepts_collections(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).find(
            {'type': 'all'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertIn(res['type'], ['collection', 'concept'])

    def test_find_wrong_type(self):
        self.assertRaises(ValueError,
                          AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).find,
                          {'type': 'collectie'})

    def test_find_keyword(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).find(
            {'label': 'e', 'type': 'concept'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'concept')

    def test_expand(self):
        all_childeren = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url, scheme_id=self.scheme_id).expand(self.collection_id)
        self.assertIsInstance(all_childeren, list)
        self.assertGreater(len(all_childeren), 0)
        self.assertIn(self.concept_id, all_childeren)

    def test_expand_invalid(self):
        all_childeren_invalid = AtramhasisProvider({'id': 'Atramhasis'}, base_url=self.base_url,
                                                   scheme_id=self.scheme_id).expand('-1')
        self.assertFalse(all_childeren_invalid)


class AtramhasisProviderMockTests(unittest.TestCase):
    def setUp(self):
        init_responses()

    def test_default_provider_no_base_url_and_scheme_id(self):
        self.assertRaises(ValueError, AtramhasisProvider, {'id': 'Atramhasis'})

    def test_default_provider_no_scheme_id(self):
        self.assertRaises(ValueError, AtramhasisProvider, {'id': 'Atramhasis'}, base_url='http://localhost')

    @responses.activate
    def test_base_url_not_available(self):
        self.assertRaises(ProviderUnavailableException, AtramhasisProvider, {'id': 'Atramhasis'},
                          base_url='http://not_available', scheme_id='STYLES')

    @responses.activate
    def test_scheme_id_not_available(self):
        self.assertRaises(Exception, AtramhasisProvider, {'id': 'Atramhasis'},
                          base_url='http://localhost', scheme_id='ONBEKEND')

    @responses.activate
    def test_set_custom_session(self):
        import requests
        sess = requests.Session()
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES', session=sess)
        assert sess == provider.session

    @responses.activate
    def test_get_top_concepts_provider(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES')
        self.assertEqual(len(provider.get_top_concepts()), 51)

    @responses.activate
    def test_get_by_id_concept(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').get_by_id(
            '1')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'urn:x-vioe:styles:1')
        self.assertEqual(concept['type'], 'concept')
        self.assertIsInstance(concept['labels'], list)

        preflabels = [{'nl': 'traditioneel'}]
        preflabels_conc = [{label.language: label.label} for label in concept['labels']
                           if label.type == 'prefLabel']
        self.assertGreater(len(preflabels_conc), 0)
        for label in preflabels:
            self.assertIn(label, preflabels_conc)

    @responses.activate
    def test_get_by_id_concept_matches(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='TREES').get_by_id(
            '2')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'urn:x-skosprovider:trees/2')
        self.assertEqual(concept['type'], 'concept')
        self.assertIsInstance(concept['labels'], list)

        preflabels = [{'en': 'The Chestnut'}]
        preflabels_conc = [{label.language: label.label} for label in concept['labels']
                           if label.type == 'prefLabel']
        self.assertGreater(len(preflabels_conc), 0)
        for label in preflabels:
            self.assertIn(label, preflabels_conc)


    @responses.activate
    def test_get_by_id_nonexistant_id(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').get_by_id(
            '123')
        self.assertFalse(concept)

    @responses.activate
    def test_get_by_uri(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').get_by_uri(
            'http://localhost/conceptschemes/STYLES/c/1')
        concept = concept.__dict__
        self.assertEqual(concept['uri'], 'urn:x-vioe:styles:1')
        self.assertEqual(concept['id'], 1)

    @responses.activate
    def test_get_by_uri_404(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').get_by_uri(
            'http://localhost/conceptschemes/STYLES/c/1234567')
        self.assertFalse(concept)

    @responses.activate
    def test_get_by_uri_wrong_scheme_id(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').get_by_uri(
            'http://localhost/conceptschemes/STYLES/c/1234')
        self.assertFalse(concept)

    @responses.activate
    def test_get_all(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES')
        self.assertEqual(len(provider.get_all()), 71)

    @responses.activate
    def test_get_all_404(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='TREES')
        self.assertFalse(provider.get_all())

    @responses.activate
    def test_get_top_display(self):
        top_atramhasis_display = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                    scheme_id='STYLES').get_top_display()
        self.assertIsInstance(top_atramhasis_display, list)
        self.assertGreater(len(top_atramhasis_display), 0)
        keys_first_display = top_atramhasis_display[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)

    @responses.activate
    def test_get_top_display_404(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='TREES')
        self.assertFalse(provider.get_top_display())

    @responses.activate
    def test_get_top_concepts(self):
        top_atramhasis_concepts = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                     scheme_id='STYLES').get_top_concepts()
        self.assertIsInstance(top_atramhasis_concepts, list)
        self.assertGreater(len(top_atramhasis_concepts), 0)

    @responses.activate
    def test_get_top_concepts_404(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                     scheme_id='TREES')
        self.assertFalse(provider.get_top_concepts())

    @responses.activate
    def test_get_childeren_display(self):
        childeren_atramhasis = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                  scheme_id='MATERIALS').get_children_display(8)
        self.assertIsInstance(childeren_atramhasis, list)
        self.assertGreater(len(childeren_atramhasis), 0)
        keys_first_display = childeren_atramhasis[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            self.assertIn(key, keys_first_display)
        self.assertIn("aluminium", [label['label'] for label in childeren_atramhasis])

    @responses.activate
    def test_get_childeren_display_404(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                  scheme_id='TREES')
        self.assertFalse(provider.get_children_display(3))

    @responses.activate
    def test_find_404(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='TREES').find(
            {'type': 'concept', 'collection': {'id': '100', 'depth': 'all'}})
        self.assertFalse(r)
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='TREES').find(
            {'type': 'concept', 'collection': {'id': '3', 'depth': 'all'}})
        self.assertFalse(r)

    @responses.activate
    def test_find_with_collection_all(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='MATERIALS').find(
            {'type': 'concept', 'collection': {'id': '0', 'depth': 'all'}})
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
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='MATERIALS')
        self.assertRaises(ValueError, provider.find,
                          {'type': 'concept', 'collection': {'id': '0', 'depth': 'very deep'}})
        self.assertRaises(ValueError, provider.find, {'type': 'concept', 'collection': {'depth': 'all'}})


    @responses.activate
    def test_find_with_collection_members(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='MATERIALS').find(
            {'type': 'concept', 'collection': {'id': '0', 'depth': 'members'}})
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
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').find(
            {'type': 'collection'}, sort='-id')
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'collection')

    @responses.activate
    def test_find_all_concepts_collections(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='MATERIALS').find(
            {'type': 'all'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertIn(res['type'], ['collection', 'concept'])

    @responses.activate
    def test_find_wrong_type(self):
        self.assertRaises(ValueError, AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                         scheme_id='STYLES').find, {'type': 'collectie'})

    @responses.activate
    def test_find_keyword(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').find(
            {'label': 'mod', 'type': 'concept'})
        self.assertIsInstance(r, list)
        self.assertGreater(len(r), 0)
        for res in r:
            self.assertEqual(res['type'], 'concept')

    @responses.activate
    def test_expand(self):
        all_childeren = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                           scheme_id='STYLES').expand(1)
        self.assertIsInstance(all_childeren, list)
        self.assertGreater(len(all_childeren), 0)
        self.assertIn('1', all_childeren)

    @responses.activate
    def test_expand(self):
        all_childeren = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                           scheme_id='MATERIALS').expand(8)
        self.assertIsInstance(all_childeren, list)
        self.assertGreater(len(all_childeren), 0)
        self.assertIn(8, all_childeren)
        self.assertIn(48, all_childeren)

    @responses.activate
    def test_expand_invalid(self):
        all_childeren_invalid = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                   scheme_id='STYLES').expand('invalid')
        self.assertFalse(all_childeren_invalid)

    @responses.activate
    def test_request_encoding(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES')
        response = provider._request("http://localhost/no_encoding")
        self.assertEqual(response.encoding, "utf-8")
