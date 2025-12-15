.. _general:

Introduction
============

This library offers an implementation of the
:class:`skosprovider.providers.VocabularyProvider` interface against an
`Atramhasis <http://atramhasis.readthedocs.org>`_ backend. This allows you to
use an Atramhasis instance as a central SKOS repository that can easily be
called by other applications. Either through using this Skosprovider, or by
using the services provided by Atramhasis directly.

While this library works with Atramhasis, the services that Atramhasis exposes
are in fact provided by `pyramid_skosprovider
<http://pyramid_skosprovider.readthedocs.org>`_. So, if you're not using
Atramhasis, but do have a backend that implements the services offered by
pyramid_skosprovider, you can use :mod:`skosprovider_atramhasis` as well.

Finally, if you have a backend that does not implement
:mod:`pyramid_skosprovider`, but implements exactly the same services, you could
use that as well.

Installation
------------

To be able to use this library you need to have a modern version of Python
installed. Currently we're supporting the last 3 versions of
Python 3.

This easiest way to install this library is through :command:`pip` or
:command:`easy install`:

.. code-block:: bash

    $ pip install skosprovider_atramhasis

This will download and install :mod:`skosprovider_atramhasis` and a few libraries it
depends on.


.. _examples:

Using the providers
===================
For demonstration purposes of :class:`~skosprovider_atramhasis.providers.AtramhasisProvider`,
the following examples use the `Flanders Heritage <https://www.onroerenderfgoed.be>`_ thesauri 
hosted at it's own `thesaurus website <https://thesaurus.onroerenderfgoed.be>`_.
You can adapt the examples with your own instance of Atramhasis, by changing the *base_url* 
and *scheme_id*.

Using AtramhasisProvider
--------------------------

The :class:`~skosprovider_atramhasis.providers.AtramhasisProvider` is a
general provider for the Atramhasis vocabularies. It's use is identical to
all other SKOSProviders. A base_url of the Atramhasis instance and a scheme_id are required to indicate the vocabulary
to be used. Please consult :ref:`supported_thesauri` for a complete list.

For better perfomance in an environment with a  :class:`skosprovider.registry.Registry`
we recommend manually providing the *uri* parameter as metadata. This can 
cut out the need for a call to the backend upon initialisation.

.. literalinclude:: ../../examples/provider.py
   :language: python

Finding concepts
----------------

See the :meth:`skosprovider_atramhasis.providers.AtramhasisProvider.find`
method for a detailed description of how this works.

.. literalinclude:: ../../examples/find.py
   :language: python

Using expand()
--------------

The expand method return the id's of all the concepts that are narrower
concepts of a certain concept or collection.

See the :meth:`skosprovider_atramhasis.providers.AtramhasisProvider.expand` method for
a detailed description of how this works.

.. literalinclude:: ../../examples/expand.py
   :language: python

Adding a cache
--------------

Skosprovider_atramhasis has to do a lot of HTTP requests. Depending on your use
case, this might cause a lot of overhead. Therefor we've made it possible to
add a `Dogpile cache <https://dogpilecache.sqlalchemy.org/en/latest/>_`. To
configure the cache, simple add a `cache_config` key when instantiating the
provider. This config will de passed to the Dogpile CacheRegion's
configure_from_config method.

.. literalinclude:: ../../examples/cache.py
   :language: python

.. _supported_thesauri:

Supported thesauri
------------------

Currently the only known publically available backed is Flanders Heritage
Ageny's own `thesaurus website <https://thesaurus.onroerenderfgoed.be>`_. It
offers a range of thesauri dealing with cultural heritage in general and
specifically in Flanders. Examples are a thesaurus of heritage types, a
thesaurus of cultures and periods, a thesaurus of heritage even types, ...
