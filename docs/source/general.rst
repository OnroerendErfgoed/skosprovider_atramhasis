.. _general:

Introduction
============

This library offers an implementation of the 
:class:`skosprovider.providers.VocabularyProvider` interface based on ...

Installation
------------

To be able to use this library you need to have a modern version of Python 
installed. Currently we're supporting versions 2.7, 3.3 and 3.4 of Python.

This easiest way to install this library is through :command:`pip` or 
:command:`easy install`:

.. code-block:: bash    
    
    $ pip install skosprovider_atramhasis

This will download and install :mod:`skosprovider_atramhasis` and a few libraries it
depends on. 

.. _supported_thesauri:


Using the providers
===================

Using AtramhasisProvider
--------------------------

The :class:`~skosprovider_atramhasis.providers.AtramhasisProvider` is a
general provider for the Atramhasis vocabularies. It's use is identical to
all other SKOSProviders. A scheme_uri is required to indicate the vocabulary
to be used. Please consult :ref:`supported_thesauri` for a complete list.

.. literalinclude:: ../../examples/traditioneel.py
   :language: python


Finding concepts
----------------

See the :meth:`skosprovider_atramhasis.providers.AtramhasisProvider.find`
method for a detailed description of how this works.

.. literalinclude:: ../../examples/find.py
   :language: python

Using expand()
--------------

The expand methods return the id's of all the concepts that are narrower 
concepts of a certain concept or collection.

See the :meth:`skosprovider_atramhasis.providers.AtramhasisProvider.expand` method for
a detailed description of how this works.

.. literalinclude:: ../../examples/expand.py
   :language: python
