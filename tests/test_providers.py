import unittest
from contextlib import contextmanager

import pytest
import responses
from skosprovider.exceptions import ProviderUnavailableException
from skosprovider.skos import Concept
from skosprovider.skos import ConceptScheme

from skosprovider_atramhasis.providers import AtramhasisProvider
from tests import init_responses


@unittest.skip("Tests that use the OE thesaurus are skipped by default to "
               "avoid dependencies.")
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
        cls.base_url = 'https://thesaurus.onroerenderfgoed.be'
        cls.scheme_id = 'ERFGOEDTYPES'
        cls.concept_id = 1
        cls.concept_uri = 'https://id.erfgoed.net/thesauri/erfgoedtypes/1'
        cls.collection_id = 1373
        cls.collection_uri = 'https://id.erfgoed.net/thesauri/erfgoedtypes/1373'

    def test_get_top_concepts_provider(self):
        provider = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id)
        assert len(provider.get_top_concepts()) > 0

    def test_get_by_id_concept(self):
        c = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id).get_by_id(self.concept_id)
        assert c.uri ==  self.concept_uri
        assert c.type == 'concept'

    def test_get_by_id_collection(self):
        c = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id).get_by_id(self.collection_id)
        assert c.uri == self.collection_uri
        assert c.type == 'collection'

    def test_get_by_id_nonexistant_id(self):
        c = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id).get_by_id('-1')
        assert not c

    def test_get_by_uri_concept(self):
        c = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id).get_by_uri(self.concept_uri)
        assert c.uri ==  self.concept_uri
        assert c.type == 'concept'

    def test_get_by_uri_collection(self):
        c = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id).get_by_uri(self.collection_uri)
        assert c.uri == self.collection_uri
        assert c.id == self.collection_id
        assert c.type == 'collection'

    def test_get_all(self):
        provider = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id)
        assert len(provider.get_all()) > 0

    def test_get_top_display(self):
        top_atramhasis_display = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url,
                                                    scheme_id=self.scheme_id).get_top_display()
        assert len(top_atramhasis_display) > 0
        keys_first_display = top_atramhasis_display[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            assert key in keys_first_display

    def test_get_top_concepts(self):
        top_atramhasis_concepts = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url,
                                                     scheme_id=self.scheme_id).get_top_concepts()
        assert len(top_atramhasis_concepts) > 0

    def test_get_childeren_display(self):
        childeren_atramhasis = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url,
                                                  scheme_id=self.scheme_id).get_children_display(self.collection_id)
        assert len(childeren_atramhasis) > 0
        keys_first_display = childeren_atramhasis[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            assert key in keys_first_display

    def test_unexisting_scheme(self):
        with pytest.raises(ProviderUnavailableException):
            cs = AtramhasisProvider(
                {'id': 'ERFGOEDTYPES'},
                base_url=self.base_url,
                scheme_id='ONBEKEND'
            ).concept_scheme

    def test_find_with_collection_all(self):
        r = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id).find(
            {'type': 'concept', 'collection': {'id': self.collection_id, 'depth': 'all'}})
        assert len(r) > 0
        keys_first_display = r[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            assert key in keys_first_display
        for res in r:
            assert res['type'] == 'concept'

    def test_find_with_collection_invalid_params(self):
        provider = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id)
        self.assertRaises(ValueError, provider.find,
                          {'type': 'concept', 'collection': {'id': self.collection_id, 'depth': 'very deep'}})
        self.assertRaises(ValueError, provider.find, {'type': 'concept', 'collection': {'depth': 'all'}})

    def test_find_collections(self):
        r = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id).find(
            {'type': 'collection'})
        assert len(r) > 0
        for res in r:
            assert res['type'] == 'collection'

    def test_find_all_concepts_collections(self):
        r = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id).find(
            {'type': 'all'})
        assert len(r) > 0
        for res in r:
            assert res['type'] in ['collection', 'concept']

    def test_find_keyword(self):
        r = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id).find(
            {'label': 'aal', 'type': 'concept'})
        assert len(r) > 0
        for c in r:
            assert c['type'] == 'concept'

    def test_expand(self):
        expand = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url, scheme_id=self.scheme_id).expand(self.collection_id)
        assert len(expand) > 0

    def test_expand_invalid(self):
        all_childeren_invalid = AtramhasisProvider({'id': 'ERFGOEDTYPES'}, base_url=self.base_url,
                                                   scheme_id=self.scheme_id).expand('-1')
        assert not all_childeren_invalid


class AtramhasisProviderMockTests(unittest.TestCase):
    def setUp(self):
        init_responses()

    def test_default_provider_no_base_url_and_scheme_id(self):
        with pytest.raises(ValueError):
            p = AtramhasisProvider({'id': 'Atramhasis'})

    def test_default_provider_no_scheme_id(self):
        with pytest.raises(ValueError):
            p = AtramhasisProvider(
                {'id': 'Atramhasis'},
                base_url='http://localhost'
            )

    def test_base_url_not_available(self):
        with pytest.raises(ProviderUnavailableException):
            cs = AtramhasisProvider(
                {'id': 'Atramhasis'},
                base_url='http://not_available', scheme_id='STYLES'
            ).concept_scheme

    @responses.activate
    def test_scheme_id_not_available(self):
        with pytest.raises(ProviderUnavailableException):
            cs = AtramhasisProvider(
                {'id': 'Atramhasis'},
                base_url='http://localhost',
                scheme_id='ONBEKEND'
            ).concept_scheme

    def test_set_custom_session(self):
        import requests
        sess = requests.Session()
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES', session=sess)
        assert sess == provider.session

    @responses.activate
    def test_conceptscheme(self):
        cs = AtramhasisProvider(
            {'id': 'Atramhasis'},
            base_url='http://localhost',
            scheme_id='MATERIALS'
        ).concept_scheme
        assert isinstance(cs, ConceptScheme)
        assert len(cs.labels) == 2
        assert len(cs.notes) == 1
        assert len(cs.sources) == 1

    def test_request_retries(self):
        with responses.RequestsMock() as rsps:
            for response_status in (500, 500, 500, 500, 200):
                rsps.add(
                    method=rsps.GET,
                    url='http://localhost/conceptschemes/MATERIALS',
                    status=response_status,
                    json={
                        'uri': 'http://localhost/conceptschemes/MATERIALS',
                        'labels': [],
                        'notes': [],
                        'sources': [],
                        'languages': [],
                    }
                )
            cs = AtramhasisProvider(
                {'id': 'Atramhasis'},
                base_url='http://localhost',
                scheme_id='MATERIALS',
            ).concept_scheme
            assert isinstance(cs, ConceptScheme)

    @responses.activate
    def test_get_top_concepts_provider(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES')
        assert len(provider.get_top_concepts()) == 51

    @responses.activate
    def test_get_by_id_concept(self):
        concept = AtramhasisProvider(
            {'id': 'Atramhasis'},
            base_url='http://localhost', scheme_id='STYLES'
        ).get_by_id('1')
        assert isinstance(concept, Concept)
        assert concept.uri == 'urn:x-vioe:styles:1'
        assert concept.type == 'concept'
        assert len(concept.labels) > 0
        assert 'traditioneel' in [l.label for l in concept.labels if l.type == 'prefLabel']
        assert 2 in concept.narrower
        assert 60 in concept.member_of

    @responses.activate
    def test_get_by_id_concept_matches(self):
        concept = AtramhasisProvider(
            {'id': 'Atramhasis'},
            base_url='http://localhost', scheme_id='TREES'
        ).get_by_id('2')

        assert isinstance(concept, Concept)
        assert concept.uri == 'urn:x-skosprovider:trees/2'
        assert concept.type == 'concept'
        assert len(concept.labels) > 0
        assert 'The Chestnut' in [l.label for l in concept.labels if l.type == 'prefLabel']
        assert 3 in concept.member_of

    @responses.activate
    def test_get_by_id_nonexistant_id(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').get_by_id(
            '123')
        assert not concept

    @responses.activate
    def test_get_by_uri(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').get_by_uri(
            'http://localhost/conceptschemes/STYLES/c/1')
        assert concept.id == 1
        assert concept.uri == 'urn:x-vioe:styles:1'

    @responses.activate
    def test_get_by_uri_404(self):
        concept = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').get_by_uri(
            'http://localhost/conceptschemes/STYLES/c/1234567')
        assert not concept

    @responses.activate
    def test_get_by_uri_wrong_scheme_id(self):
        concept = AtramhasisProvider(
            {'id': 'Atramhasis'},
            base_url='http://localhost',
            scheme_id='STYLESS'
        ).get_by_uri(
            'http://localhost/conceptschemes/STYLES/c/1234'
        )
        assert not concept

    @responses.activate
    def test_get_all(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES')
        assert len(provider.get_all()) == 71

    @responses.activate
    def test_get_all_404(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='TREES')
        assert not provider.get_all()

    @responses.activate
    def test_get_top_display(self):
        top_atramhasis_display = AtramhasisProvider(
            {'id': 'Atramhasis'},
            base_url='http://localhost', scheme_id='STYLES'
        ).get_top_display()
        assert isinstance(top_atramhasis_display, list)
        assert len(top_atramhasis_display) > 0
        keys_first_display = top_atramhasis_display[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            assert key in keys_first_display

    @responses.activate
    def test_get_top_display_404(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='TREES')
        assert not provider.get_top_display()

    @responses.activate
    def test_get_top_concepts(self):
        top_atramhasis_concepts = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                     scheme_id='STYLES').get_top_concepts()
        assert isinstance(top_atramhasis_concepts, list)
        assert len(top_atramhasis_concepts) > 0

    @responses.activate
    def test_get_top_concepts_404(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                     scheme_id='TREES')
        assert not provider.get_top_concepts()

    @responses.activate
    def test_get_childeren_display(self):
        childeren_atramhasis = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                  scheme_id='MATERIALS').get_children_display(8)
        assert len(childeren_atramhasis) > 0
        keys_first_display = childeren_atramhasis[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            assert key in keys_first_display
        assert "aluminium" in [label['label'] for label in childeren_atramhasis]

    @responses.activate
    def test_get_childeren_display_404(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                                  scheme_id='TREES')
        assert not provider.get_children_display(3)

    @responses.activate
    def test_find_404(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='TREES').find(
            {'type': 'concept', 'collection': {'id': '100', 'depth': 'all'}})
        assert not r
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='TREES').find(
            {'type': 'concept', 'collection': {'id': '3', 'depth': 'all'}})
        assert not r

    @responses.activate
    def test_find_with_collection_all(self):
        r = AtramhasisProvider(
            {'id': 'Atramhasis'},
            base_url='http://localhost',
            scheme_id='ERFGOEDTYPES'
        ).find({
            'type': 'concept',
            'collection': {'id': 2132, 'depth': 'all'}
        })
        assert len(r) == 2
        keys_first_display = r[0].keys()
        for key in ['id', 'type', 'label', 'uri']:
            assert key in keys_first_display
        assert "paleobodems" in [label['label'] for label in r]
        for res in r:
            assert res['type'] == 'concept'

    @responses.activate
    def test_find_with_collection_invalid_params(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='MATERIALS')
        with pytest.raises(ValueError):
            provider.find({
                'type': 'concept', 'collection': {'id': '0', 'depth': 'very deep'}
            })
        with pytest.raises(ValueError):
            provider.find({
                'type': 'concept', 'collection': {'depth': 'all'}
            })

    @responses.activate
    def test_find_with_collection_members(self):
        with pytest.raises(ValueError):
            r = AtramhasisProvider(
                {'id': 'Atramhasis'},
                base_url='http://localhost',
                scheme_id='MATERIALS'
            ).find({
                'type': 'concept',
                'collection': {'id': '0', 'depth': 'members'}
            })

    @responses.activate
    def test_find_collections(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').find(
            {'type': 'collection'}, sort='id')
        assert len(r) == 5
        assert all([res['type'] =='collection' for res in r])
        assert [0, 60, 61, 62, 63] == [res['id'] for res in r]

    @responses.activate
    def test_find_collections_sort_desc(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES').find(
            {'type': 'collection'}, sort='id', sort_order='desc')
        assert len(r) == 5
        assert all([res['type'] =='collection' for res in r])
        assert [63, 62, 61, 60, 0] == [res['id'] for res in r]

    @responses.activate
    def test_find_all_concepts_collections(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='MATERIALS').find({
            'type': 'all'
        })
        assert len(r) > 0
        for res in r:
            assert res['type'] in ['collection', 'concept']

    @responses.activate
    def test_find_wrong_type(self):
        r = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='MATERIALS').find(
            {'type': 'all'})
        r2 = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='MATERIALS').find(
            {'type': 'collection'})
        assert len(r) == len(r2)

    @responses.activate
    def test_find_keyword(self):
        r = AtramhasisProvider(
            {'id': 'Atramhasis'},
            base_url='http://localhost', scheme_id='STYLES'
        ).find({'label': 'mod', 'type': 'concept'})
        assert len(r) > 0
        for res in r:
            assert res['type'] == 'concept'

    @responses.activate
    def test_find_match(self):
        r = AtramhasisProvider(
            {'id': 'Atramhasis'},
            base_url='http://localhost',
            scheme_id='ERFGOEDTYPES'
        ).find({
            'matches': {
                'uri': 'http://vocab.getty.edu/aat/300004983'
            }
        })
        assert len(r) == 1
        veekralen = r[0]
        assert veekralen['type'] == 'concept'
        assert veekralen['uri'] == 'https://id.erfgoed.net/thesauri/erfgoedtypes/1314'

    @responses.activate
    def test_find_match_close(self):
        r = AtramhasisProvider(
            {'id': 'Atramhasis'},
            base_url='http://localhost',
            scheme_id='ERFGOEDTYPES'
        ).find({
            'matches': {
                'uri': 'http://vocab.getty.edu/aat/300004983',
                'type': 'close'
            }
        })
        assert len(r) == 1
        veekralen = r[0]
        assert veekralen['type'] == 'concept'
        assert veekralen['uri'] == 'https://id.erfgoed.net/thesauri/erfgoedtypes/1314'

    @responses.activate
    def test_find_match_no_uri(self):
        with pytest.raises(ValueError):
            r = AtramhasisProvider(
                {'id': 'Atramhasis'},
                base_url='http://localhost',
                scheme_id='ERFGOEDTYPES'
            ).find({
                'matches': {
                    'type': 'close'
                }
            })

    @responses.activate
    def test_expandi_not_found(self):
        all_children = AtramhasisProvider(
            {'id': 'Atramhasis'},
            base_url='http://localhost', scheme_id='TREES'
        ).expand(100)
        assert not all_children

    @responses.activate
    def test_expand(self):
        all_children = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                           scheme_id='STYLES').expand(1)
        assert len(all_children) > 0
        assert '1' in all_children

    @responses.activate
    def test_expand(self):
        all_childeren = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost',
                                           scheme_id='MATERIALS').expand(8)
        assert len(all_childeren) > 0
        assert 8 in all_childeren
        assert 48 in all_childeren

    @responses.activate
    def test_expand_invalid(self):
        with pytest.raises(ProviderUnavailableException) as e:
            AtramhasisProvider(
                {'id': 'Atramhasis'},
                base_url='http://localhost', scheme_id='STYLES'
            ).expand('invalid')

    @responses.activate
    def test_request_encoding(self):
        provider = AtramhasisProvider({'id': 'Atramhasis'}, base_url='http://localhost', scheme_id='STYLES')
        response = provider._request("http://localhost/no_encoding")
        assert response.encoding == "utf-8"


@contextmanager
def real_cache(provider):
    """Enables the cache for the duration of the context.

    Caching is usually not desirable during testing, but this will turn it on
    temporarily.

    Usage:

       with real_cache():
           code
    """
    try:
        provider.caches['cache'].configure('dogpile.cache.memory',
                                           replace_existing_backend=True)
        yield
    finally:
        provider.caches['cache'].configure('dogpile.cache.null',
                                           replace_existing_backend=True)


class CacheTests(unittest.TestCase):

    def test_cached_unique_per_provider_scheme(self):
        url = 'http://127.0.0.1/thesaurus'
        schemes = ('GEBEURTENISTYPES', 'WAARDETYPES')
        with responses.RequestsMock() as rsps:
            for scheme in schemes:
                rsps.add(
                    method='GET',
                    url=url + '/conceptschemes/' + scheme + '/c/1',
                    json={
                        "label": scheme.title() + " type 1",
                        "id": 1,
                        "type": "concept"
                    })
                rsps.add(
                    method='GET',
                    url=url + '/conceptschemes/' + scheme + '/c/2',
                    json={
                        "label": scheme.title() + " type 2",
                        "id": 2,
                        "type": "concept"
                    })
            # Create 2 different providers
            provider1, provider2 = (
                AtramhasisProvider({'id': scheme.lower(), 'default_language': 'nl'},
                                   base_url=url,
                                   scheme_id=scheme)
                for scheme in schemes
            )

            with real_cache(provider1), real_cache(provider2):
                # Both request the same ID.
                thesaurus_calls = len(rsps.calls)
                result_1 = provider1.get_by_id('1')
                self.assertEqual(thesaurus_calls + 1, len(rsps.calls))
                result_2 = provider2.get_by_id('1')
                self.assertEqual(thesaurus_calls + 2, len(rsps.calls))
                # Results must be different
                self.assertNotEqual(result_1, result_2)

                # Do 2 more identical calls, they should return from cache.
                provider1.get_by_id('1')
                provider2.get_by_id('1')
                self.assertEqual(thesaurus_calls + 2, len(rsps.calls))

                # Do 2 other calls, they should not return from cache.
                provider1.get_by_id('2')
                provider2.get_by_id('2')
                self.assertEqual(thesaurus_calls + 4, len(rsps.calls))

    def test_cache_unique_per_url(self):
        urls = ('http://127.0.0.1/thesaurus1', 'http://127.0.0.1/thesaurus2')
        scheme = 'GEBEURTENISTYPES'
        with responses.RequestsMock() as rsps:
            for url in urls:
                rsps.add(
                    method='GET',
                    url=url + '/conceptschemes/' + scheme + '/c/1',
                    json={
                        "label": scheme.title() + " type 1",
                        "id": 1,
                        "type": "concept"
                    })
                rsps.add(
                    method='GET',
                    url=url + '/conceptschemes/' + scheme + '/c/2',
                    json={
                        "label": scheme.title() + " type 2",
                        "id": 2,
                        "type": "concept"
                    })
            # Create 2 different providers
            provider1, provider2 = (
                AtramhasisProvider({'id': scheme.lower(), 'default_language': 'nl'},
                                   base_url=url,
                                   scheme_id=scheme)
                for url in urls
            )
            with real_cache(provider1), real_cache(provider2):
                # Both request the same ID.
                thesaurus_calls = len(rsps.calls)
                result_1 = provider1.get_by_id('1')
                self.assertEqual(thesaurus_calls + 1, len(rsps.calls))
                result_2 = provider2.get_by_id('1')
                self.assertEqual(thesaurus_calls + 2, len(rsps.calls))
                # Results must be different
                self.assertNotEqual(result_1, result_2)

                # Do 2 more identical calls, they should return from cache.
                provider1.get_by_id('1')
                provider2.get_by_id('1')
                self.assertEqual(thesaurus_calls + 2, len(rsps.calls))

                # Do 2 other calls, they should not return from cache.
                provider1.get_by_id('2')
                provider2.get_by_id('2')
                self.assertEqual(thesaurus_calls + 4, len(rsps.calls))
