0.3.1 (2020-02-19)
------------------

- Fix a bug in `dict_to_thing` that resulted in the provider exposing objects
  instead of id's in relations. (#80)

0.3.0 (2020-01-24)
------------------

- Update to `Skosprovider 0.7.0 <https://pypi.org/project/skosprovider/0.7.0/>`_.
- Add caching support to the provider. (#75)
- Don't load concepscheme at startup, since this prevents the provider from
  instantiating when an Atramhasis instance is down. (#66)
- This is the last version to support Python 2.7. Updated Python 3 support to
  3.6, 3.7 and 3.8.

0.2.1 (2019-11-13)
------------------

- Update supported Python version (#61)
- Add a long_description_content_type (#55)
- Correct handling of get_by_uri (#69)

0.2.0 (2017-08-24)
------------------

- Update to skosprovider 0.6.1
- Allow Notes with HTML (#17)
- Add languages to Conceptscheme (#18)
- Add sources to Conceptscheme, Collection and Concept (#19)
- Add sorting to finders (#20)

0.1.1 (2016-03-23)
------------------

- Official support for Py35
- Allow configuring a requests session. (#14)

0.1.0 (2015-03-19)
------------------

- Initial version
- Compatible with `SkosProvider 0.5.x <http://skosprovider.readthedocs.org/en/0.5.0>`_.
