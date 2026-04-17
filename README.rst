skosprovider_atramhasis
=======================

⚠️ This package is deprecated. Use
`skosprovider <https://github.com/OnroerendErfgoed/skosprovider/>`_ instead.

Starting from `skosprovider` 2.0.0 the functionality of this package has been
merged into the main `skosprovider <https://github.com/OnroerendErfgoed/skosprovider/>`_
repository. This package will remain usable with ``skosprovider < 2.0.0``, but is
no longer actively maintained. It is recommended to upgrade to
``skosprovider >= 2.0.0`` and use ``skosprovider_atramhasis`` from there.

Migrating to skosprovider 2.0.0
-------------------------------

1. Uninstall ``skosprovider_atramhasis`` and install ``skosprovider >= 2.0.0``::

       pip uninstall skosprovider_atramhasis
       pip install "skosprovider>=2.0.0"

2. Replace any ``skosprovider_atramhasis`` imports with their equivalent under
   ``skosprovider`` (see the `skosprovider
   <https://github.com/OnroerendErfgoed/skosprovider/>`_ documentation for the
   full mapping).

A `Skosprovider <http://skosprovider.readthedocs.org>`_ that can talk to an
`Atramhasis <http://atramhasis.readthedocs.org>`_ instance.

.. image:: https://travis-ci.org/OnroerendErfgoed/skosprovider_atramhasis.png?branch=master
        :target: https://travis-ci.org/OnroerendErfgoed/skosprovider_atramhasis
.. image:: https://coveralls.io/repos/OnroerendErfgoed/skosprovider_atramhasis/badge.png?branch=master
        :target: https://coveralls.io/r/OnroerendErfgoed/skosprovider_atramhasis

.. image:: https://readthedocs.org/projects/skosprovider-atramhasis/badge/?version=latest
        :target: https://readthedocs.org/projects/skosprovider-atramhasis/?badge=latest
.. image:: https://badge.fury.io/py/skosprovider_atramhasis.png
        :target: http://badge.fury.io/py/skosprovider_atramhasis

