# -*- coding: utf-8 -*-
'''
This module implements a :class:`skosprovider.providers.VocabularyProvider`
for Atramhasis
'''

import requests
from requests.exceptions import ConnectionError

import warnings
import logging
from skosprovider.skos import ConceptScheme
from skosprovider_atramhasis.utils import _split_uri, dict_to_thing

log = logging.getLogger(__name__)

from skosprovider.exceptions import ProviderUnavailableException
from skosprovider.providers import VocabularyProvider

class AtramhasisProvider(VocabularyProvider):
    """A provider that can work with the Atramhasis REST services (based on pyramid_skosprovider)
    """

    def __init__(self, metadata, **kwargs):
        """ Constructor of the :class:`skosprovider_atramhasis.providers.AtramhasisProvider`

        :param (dict) metadata: metadata of the provider
        :param kwargs: arguments defining the provider.
            * Typical argument is `scheme_uri`.
                The `scheme_uri` is a composition of the `base_scheme_uri` and `scheme_id`
            * The :class:`skosprovider_Atramhasis.providers.AtramhasisProvider`
                is the default :class:`skosprovider_Atramhasis.providers.AtramhasisProvider`
        """
        if not 'default_language' in metadata:
            metadata['default_language'] = 'en'
        if 'scheme_uri' in kwargs:
            self.base_scheme_uri = _split_uri(kwargs['scheme_uri'], 0)
            self.scheme_id = _split_uri(kwargs['scheme_uri'], 1)
        else:
            self.base_scheme_uri = 'http://localhost:6543/conceptschemes'
            self.scheme_id = 'STYLES'
        self.scheme_uri = self.base_scheme_uri + "/" + self.scheme_id
        concept_scheme = ConceptScheme(self.scheme_uri)
        super(AtramhasisProvider, self).__init__(metadata, concept_scheme=concept_scheme, **kwargs)

    def _get_language(self, **kwargs):
        return self.metadata['default_language']

    def get_by_id(self, id):
        """ Get a :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Collection` by id

        :param (str) id: integer id of the :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`
        :return: corresponding :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`.
            Returns None if non-existing id
        """
        request = self.scheme_uri + "/c/" + str(id)
        response = self._request(request, {'Accept': 'application/json'})
        if response.status_code == 404:
            return False
        answer = dict_to_thing(response.json())
        return answer

    def get_by_uri(self, uri):
        """ Get a :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Collection` by uri

        :param (str) uri: string uri of the :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`
        :return: corresponding :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Concept`.
            Returns None if non-existing id
        """
        id = _split_uri(uri, 1)
        return self.get_by_id(id)

    def find(self, query):
        '''Find concepts that match a certain query.

        Currently query is expected to be a dict, so that complex queries can
        be passed. You can use this dict to search for concepts or collections
        with a certain label, with a certain type and for concepts that belong
        to a certain collection.

        .. code-block:: python

            # Find anything that has a label of church.
            provider.find({'label': 'church'}

            # Find all concepts that are a part of collection 5.
            provider.find({'type': 'concept', 'collection': {'id': 5})

            # Find all concepts, collections or children of these
            # that belong to collection 5.
            provider.find({'collection': {'id': 5, 'depth': 'all'})

        :param query: A dict that can be used to express a query. The following
            keys are permitted:

            * `label`: Search for something with this label value. An empty \
                label is equal to searching for all concepts.
            * `type`: Limit the search to certain SKOS elements. If not \
                present `all` is assumed:

                * `concept`: Only return :class:`skosprovider.skos.Concept` \
                    instances.
                * `collection`: Only return \
                    :class:`skosprovider.skos.Collection` instances.
                * `all`: Return both :class:`skosprovider.skos.Concept` and \
                    :class:`skosprovider.skos.Collection` instances.
            * `collection`: Search only for concepts belonging to a certain \
                collection. This argument should be a dict with two keys:

                * `id`: The id of a collection. Required.
                * `depth`: Can be `members` or `all`. Optional. If not \
                    present, `members` is assumed, meaning only concepts or \
                    collections that are a direct member of the collection \
                    should be considered. When set to `all`, this method \
                    should return concepts and collections that are a member \
                    of the collection or are a narrower concept of a member \
                    of the collection.

        :returns: A :class:`lst` of concepts and collections. Each of these
            is a dict with the following keys:

            * id: id within the conceptscheme
            * uri: :term:`uri` of the concept or collection
            * type: concept or collection
            * label: A label to represent the concept or collection. It is \
                determined by looking at the `**kwargs` parameter, the default \
                language of the provider and finally falls back to `en`.
        '''

        # #  interprete and validate query parameters (label, type and collection)
        # Label
        label = None
        if 'label' in query:
            label = query['label']

        # Type: 'collection','concept' or 'all'
        type_c = 'all'
        if 'type' in query:
            type_c = query['type']
        if type_c not in ('all', 'concept', 'collection'):
            raise ValueError("type: only the following values are allowed: 'all', 'concept', 'collection'")

        #Collection to search in (optional)
        children = False
        if 'collection' in query:
            collection = query['collection']
            if not 'id' in collection:
                raise ValueError("collection: 'id' is required key if a collection-dictionary is given")
            depth_all = False
            if 'depth' in collection:
                if collection['depth'] in ['members', 'all']:
                    depth_all = collection['depth'] == 'all'
                else:
                    raise ValueError(
                    "collection - 'depth': only the following values are allowed: 'members', 'all'")
            if depth_all:
                children = self.expand(collection['id'])
            else:
                answer = self.get_children_display(collection['id'])
                children = [a['id'] for a in answer]

        request = self.scheme_uri + "/c/"
        params = dict()
        params['type'] = type_c
        if label:
            params['label'] = label
        response = self._request(request, {'Accept':'application/json'}, params)
        if response.status_code == 404:
            return False
        if children:
            return [r for r in response.json() if r['id'] in children]
        else:
            return response.json()

    def get_all(self):
        '''Returns all concepts and collections in this provider.

        :returns: A :class:`lst` of concepts and collections. Each of these is a dict
            with the following keys:

            * id: id within the conceptscheme
            * uri: :term:`uri` of the concept or collection
            * type: concept or collection
            * label: A label to represent the concept or collection. It is \
                determined by looking at the `**kwargs` parameter, the default \
                language of the provider and finally falls back to `en`.
        '''
        request = self.scheme_uri + "/c/"
        response = self._request(request, {'Accept':'application/json'})
        if response.status_code == 404:
            return False
        return response.json()

    def get_top_concepts(self):
        """  Returns all concepts that form the top-level of a display hierarchy.

        :return: A :class:`lst` of concepts.
        """
        request = self.scheme_uri + "/topconcepts"
        response = self._request(request, {'Accept':'application/json'})
        if response.status_code == 404:
            return False
        return response.json()

    def get_top_display(self):
        """  Returns all concepts or collections that form the top-level of a display hierarchy.
        :return: A :class:`lst` of concepts and collections.
        """
        request = self.scheme_uri + "/displaytop"
        response = self._request(request, {'Accept':'application/json'})
        if response.status_code == 404:
            return False
        return response.json()

    def get_children_display(self, id):
        """ Return a list of concepts or collections that should be displayed under this concept or collection.

        :param str id: A concept or collection id.
        :returns: A :class:`lst` of concepts and collections.
        """
        request = self.scheme_uri + "/c/" + str(id) + "/displaychildren"
        response = self._request(request, {'Accept':'application/json'})
        if response.status_code == 404:
            return False
        return response.json()

    def expand(self, id):
        """ Expand a concept or collection to all it's narrower concepts.
            If the id passed belongs to a :class:`skosprovider.skos.Concept`,
            the id of the concept itself should be include in the return value.

        :param str id: A concept or collection id.
        :returns: A :class:`lst` of id's. Returns false if the input id does not exists
        """
        request = self.scheme_uri + "/c/" + str(id) + "/expand"
        response = self._request(request, {'Accept':'application/json'})
        if response.status_code != 200:
            return False
        return response.json()


    def _request(self, request, headers=None, params=None):
        try:
            res = requests.get(request, headers=headers, params=params)
        except ConnectionError as e:
            raise ProviderUnavailableException("Request could not be executed - Request: %s" % (request,))
        if not res.encoding:
            res.encoding = 'utf-8'
        return res
