import os
import sys

if sys.version_info < (3,5):
    sys.exit('Sorry, Python < 3.5 is not supported')

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tei2neo',
    version= '0.3.0',
    description='TEI (Text Encoding Initiative) parser to extract information and store it in Neo4j database',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://sissource.ethz.ch/sis/semper-tei',
    author='Swen Vermeul • ID SIS • ETH Zürich',
    author_email='swen@ethz.ch',
    license='BSD',
    packages=[
        'tei2neo',
    ],
    install_requires=[
        'pytest',
        'py2neo',
        'bs4',
        'lxml',
        'spacy',
        'requests',
    ],
    entry_points={ 
        'console_scripts' : [
            'tei2neo=tei2neo.import_files:cli',
            'delete_tei_categories=tei2neo.import_files:delete_all_categories',
            'import_tei_categories=tei2neo.import_files:import_categories_from_path',
            'import_tei_from_path=tei2neo.import_files:import_tei_from_path',
        ]
    },
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
