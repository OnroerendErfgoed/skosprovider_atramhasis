# -*- coding: utf-8 -*-
'''
This module implements a :class:`skosprovider.providers.VocabularyProvider`
for Atramhasis
'''
import logging

import requests
from requests.exceptions import ConnectionError, Timeout
from dogpile.cache import make_region

from skosprovider_atramhasis.cache_utils import _atramhasis_key_generator
from skosprovider_atramhasis.cache_utils import _cache_on_arguments
from skosprovider_atramhasis.utils import dict_to_thing
from skosprovider.exceptions import ProviderUnavailableException
from skosprovider.providers import VocabularyProvider
from skosprovider.skos import ConceptScheme, Label, Note, dict_to_source

log = logging.getLogger(__name__)


class AtramhasisProvider(VocabularyProvider):
    """A provider that can work with the Atramhasis REST services (based on pyramid_skosprovider)
    """

    base_url = None
    '''Base URL of an Atramhasis instance.'''

    scheme_id = None
    '''Identifier of the ConceptScheme this provider is managing.'''

    session = None
    '''
    The :class:`requests.Session` being used to make HTTP requests.
    '''

    def __init__(self, metadata, **kwargs):
        """Create a new AtramhasisProvider

        :param (dict) metadata: metadata of the provider
        :param kwargs: arguments defining the provider.
            * `base_url` and `scheme_id` are required.
            * `session` is optional and can be used to pass a custom
                :class:`requests.Session`, eg. to configure caching strategies.
            * `cache_config` is an optional dict. Only keys starting with
                "cache." are relevant.
        """

        if not 'subject' in metadata:
            metadata['subject'] = []
        self.metadata = metadata
        self.allowed_instance_scopes = kwargs.get(
            'allowed_instance_scopes',
            ['single', 'threaded_thread']
        )
        if 'base_url' in kwargs:
            self.base_url = kwargs['base_url']
        else:
            raise ValueError("Please provide a base_url for the provider")
        if 'scheme_id' in kwargs:
            self.scheme_id = kwargs['scheme_id']
        else:
            raise ValueError("Please provide a scheme_id for the provider")

        if 'session' in kwargs:
            self.session = kwargs['session']
        else:
            self.session = requests.Session()

        self.caches = {
            'cache': make_region()
        }
        if not self.caches['cache'].is_configured:
            self.caches['cache'].configure_from_config(
                kwargs.get(
                    'cache_config',
                    {'cache.backend': 'dogpile.cache.null'}
                ),
                prefix='cache.'
            )

    @property
    def concept_scheme(self):
        return self._get_concept_scheme()

    def _get_concept_scheme(self):
        request = self.base_url + '/conceptschemes/' + self.scheme_id
        response = self._request(request, {'Accept': 'application/json'}, dict())
        if response.status_code == 404:
            raise ProviderUnavailableException(
                "Conceptscheme %s not found. Check your configuration." % request
            )
        cs = response.json()
        return ConceptScheme(
            cs['uri'],
            labels=[
                Label(l['label'] if 'label' in l.keys() else '<no label>',
                      l['type'] if 'type' in l.keys() else 'prefLabel',
                      l['language'] if 'language' in l.keys() else 'und')
                for l in cs['labels']
            ],
            notes=[
                Note(n['note'] if 'note' in n.keys() else '<no note>',
                     n['type'] if 'type' in n.keys() else 'note',
                     n['language'] if 'language' in n.keys() else 'und',
                     n['markup'] if 'markup' in n.keys() else None)
                for n in cs['notes']
            ],
            sources=[
                dict_to_source(s) for s in cs['sources']
            ],
            languages=cs['languages']
        )

    @_cache_on_arguments(cache_name='cache')
    def get_by_id(self, id):
        request = self.base_url + '/conceptschemes/' + self.scheme_id + "/c/" + str(id)
        response = self._request(request, {'Accept': 'application/json'})
        if response.status_code == 404:
            return False
        answer = dict_to_thing(response.json())
        return answer

    @_cache_on_arguments(cache_name='cache')
    def get_by_uri(self, uri):
        request = self.base_url + "/uris"
        params = {'uri': uri}
        response = self._request(request, {'Accept': 'application/json'}, params)
        if response.status_code == 404:
            return False
        if response.json()['concept_scheme']['id'] != self.scheme_id:
            return False
        return self.get_by_id(response.json()['id'])

    @_cache_on_arguments(cache_name='cache')
    def find(self, query, **kwargs):
        # interprete and validate query parameters

        params = {}
        params['language'] = self._get_language(**kwargs)
        params.update(self._get_sort_params(**kwargs))

        # Label
        if 'label' in query:
            params['label'] = query['label']

        # Type: 'collection' or 'concept' or 'all'
        if 'type' in query and query['type'] in ['concept', 'collection']:
            params['type'] = query['type']

        # Collection to search in (optional)
        if 'collection' in query:
            collection = query['collection']
            if not 'id' in collection:
                raise ValueError("collection: 'id' is required key if a collection-dictionary is given")
            params['collection'] = collection['id']
            if 'depth' in collection and collection['depth'] != 'all':
                    raise ValueError("collection - 'depth': only 'all' is supported by Atramhasis")

        # Match
        if 'matches' in query:
            match_uri = query['matches'].get('uri', None)
            if not match_uri:
                raise ValueError('Please provide a URI to match with.')
            else:
                params['match'] = match_uri
            match_type = query['matches'].get('type', None)
            if match_type:
                params['match_type'] = match_type

        search_url = self.base_url + '/conceptschemes/' + self.scheme_id + "/c/"
        response = self._request(search_url, {'Accept': 'application/json'}, params)
        if response.status_code == 404:
            return False
        return response.json()

    @_cache_on_arguments(cache_name='cache')
    def get_all(self, **kwargs):
        request = self.base_url + '/conceptschemes/' + self.scheme_id + "/c/"
        params = dict()
        params['language'] = self._get_language(**kwargs)
        params.update(self._get_sort_params(**kwargs))
        response = self._request(request, {'Accept': 'application/json'}, params)
        if response.status_code == 404:
            return False
        return response.json()

    @_cache_on_arguments(cache_name='cache')
    def get_top_concepts(self, **kwargs):
        request = self.base_url + '/conceptschemes/' + self.scheme_id + "/topconcepts"
        params = dict()
        params['language'] = self._get_language(**kwargs)
        params.update(self._get_sort_params(**kwargs))
        response = self._request(request, {'Accept': 'application/json'}, params)
        if response.status_code == 404:
            return False
        return response.json()

    @_cache_on_arguments(cache_name='cache')
    def get_top_display(self, **kwargs):
        request = self.base_url + '/conceptschemes/' + self.scheme_id + "/displaytop"
        params = dict()
        params['language'] = self._get_language(**kwargs)
        params.update(self._get_sort_params(**kwargs))
        response = self._request(request, {'Accept': 'application/json'}, params)
        if response.status_code == 404:
            return False
        return response.json()

    @_cache_on_arguments(cache_name='cache')
    def get_children_display(self, id, **kwargs):
        request = self.base_url + '/conceptschemes/' + self.scheme_id + "/c/" + str(id) + "/displaychildren"
        params = dict()
        params['language'] = self._get_language(**kwargs)
        params.update(self._get_sort_params(**kwargs))
        response = self._request(request, {'Accept': 'application/json'}, params)
        if response.status_code == 404:
            return False
        return response.json()

    @_cache_on_arguments(cache_name='cache')
    def expand(self, id):
        request = self.base_url + '/conceptschemes/' + self.scheme_id + "/c/" + str(id) + "/expand"
        response = self._request(request, {'Accept': 'application/json'})
        if response.status_code != 200:
            return False
        return response.json()

    def _get_sort_params(self, **kwargs):
        if 'sort' in kwargs:
            sort = kwargs.get('sort')
            if kwargs.get('sort_order', 'asc') == 'desc':
                sort = '-' + sort
            return {'sort': sort}
        return {}

    def _request(self, request, headers=None, params=None):
        try:
            res = self.session.get(request, headers=headers, params=params)
        except ConnectionError:
            raise ProviderUnavailableException("Request could not be executed \
                    due to connection issues- Request: %s" % (request,))
        except Timeout: # pragma: no cover
            raise ProviderUnavailableException("Request could not be executed \
                    due to timeout - Request: %s" % (request,))
        if res.status_code >= 500:
            raise ProviderUnavailableException("Request could not be executed \
                    due to server issues - Request: %s" % (request,))
        if not res.encoding:
            res.encoding = 'utf-8'
        return res
