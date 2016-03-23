# -*- coding: utf-8 -*-
import unittest
from skosprovider.exceptions import ProviderUnavailableException
from skosprovider.skos import Concept, Collection, ConceptScheme

from skosprovider_atramhasis.utils import text_, dict_to_thing


class UtilsTests(unittest.TestCase):

    def setUp(self):
        self.concept = {"subordinate_arrays": [], "matches": {"related": ["http://id.python.org/different/types/of/trees/nr/17/the/other/chestnut"]}, "labels": [{"type": "prefLabel", "language": "en", "label": "The Chestnut"}, {"type": "altLabel", "language": "nl", "label": "De Paardekastanje"}, {"type": "altLabel", "language": "fr", "label": "la ch\u00e2taigne"}], "narrower": [], "related": [], "broader": [], "id": 2, "member_of": [{"labels": [{"type": "prefLabel", "language": "en", "label": "Trees by species"}, {"type": "prefLabel", "language": "nl", "label": "Bomen per soort"}], "label": "Bomen per soort", "type": "collection", "id": 3, "uri": "urn:x-skosprovider:trees/3"}], "notes": [{"note": "A different type of tree.", "type": "definition", "language": "en"}], "uri": "urn:x-skosprovider:trees/2", "label": "The Chestnut", "type": "concept"}
        self.collection = {"labels": [{"type": "prefLabel", "language": "en", "label": "Trees by species"}, {"type": "prefLabel", "language": "nl", "label": "Bomen per soort"}], "members": [{"labels": [{"type": "prefLabel", "language": "en", "label": "The Chestnut"}, {"type": "altLabel", "language": "nl", "label": "De Paardekastanje"}, {"type": "altLabel", "language": "fr", "label": "la ch\u00e2taigne"}], "label": "The Chestnut", "type": "concept", "id": 2, "uri": "urn:x-skosprovider:trees/2"}, {"labels": [{"type": "prefLabel", "language": "en", "label": "The Larch"}, {"type": "prefLabel", "language": "nl", "label": "De Lariks"}], "label": "De Lariks", "type": "concept", "id": 1, "uri": "urn:x-skosprovider:trees/1"}], "member_of": [], "superordinates": [], "label": "Bomen per soort", "type": "collection", "id": 3, "uri": "urn:x-skosprovider:trees/3"}
        self.concept_no_id = {}
        self.concept_no_type = {"id": 2}
        self.concept_invalid_type = {"id": 2, "type": "blabla"}
    def tearDown(self):
        pass

    def test_text(self):
        res = text_(b'test123')
        self.assertEqual(u'test123', res)

    def test_text_unicode(self):
        res = text_(u'test123')
        self.assertEqual(u'test123', res)

    def test_text_utf8(self):
        res = text_(b'LaPe\xc3\xb1a', 'utf-8')
        self.assertEqual(u'LaPe\xf1a', res)

    def test_dict_to_thing_concept(self):
        concept = dict_to_thing(self.concept)
        self.assertIsInstance(concept, Concept)
        self.assertEqual(concept.id, self.concept['id'])
        self.assertEqual(concept.type, "concept")
        self.assertEqual(concept.uri, self.concept['uri'])

    def test_dict_to_thing_concept_return(self):
        concept = Concept("uri", "scheme")
        concept_2 = dict_to_thing(concept)
        self.assertEqual(concept, concept_2)

    def test_dict_to_thing_collection(self):
        collection = dict_to_thing(self.collection)
        self.assertIsInstance(collection, Collection)
        self.assertEqual(collection.id, self.collection['id'])
        self.assertEqual(collection.type, "collection")
        self.assertEqual(collection.uri, self.collection['uri'])

    def test_dict_to_thing_invalid(self):
        self.assertRaises(ValueError, dict_to_thing, self.concept_no_id)
        self.assertRaises(ValueError, dict_to_thing, self.concept_no_type)
        self.assertRaises(ValueError, dict_to_thing, self.concept_invalid_type)
