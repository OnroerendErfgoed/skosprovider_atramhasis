import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

packages = [
    'skosprovider_atramhasis'
]

requires = [
    'skosprovider>=0.7.1',
    'requests',
    'dogpile.cache>=1.1.0',
]
setup(
    name='skosprovider_atramhasis',
    version='1.0.0',
    description='Skosprovider implementation of Atramhasis Vocabularies',
    long_description=README,
    long_description_content_type='text/x-rst',
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    author='Flanders Heritage Agency',
    author_email='ict@onroerenderfgoed.be',
    url='https://github.com/OnroerendErfgoed/skosprovider_atramhasis',
    keywords='atramhasis skos skosprovider thesauri vocabularies',
)
