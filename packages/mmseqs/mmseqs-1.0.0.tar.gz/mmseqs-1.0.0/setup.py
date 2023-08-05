# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mmseqs']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.78,<2.0', 'pandas>=1.2.1,<2.0.0', 'sqlitedict>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'mmseqs',
    'version': '1.0.0',
    'description': 'MMSEQS Python bindings',
    'long_description': '# MMseqs2 bindings for Python\n\nThis project provides bidings for mmseqs. It\'s still work in progress.\nThis is the base usage scenario:\n```python\nimport mmseqs\n\n#\n# Demonstration of basic mmseqs2 operations\n#\n\n# Create a client\nclient = mmseqs.MMSeqs()\n\n# Create a database from fasta file\n# Here we specify name of the database, description and input file\n# (The input can also be a Seq/SeqRecord list/iterator/etc.)\nclient.databases.create("test", "Test database", "example/a.fasta")\n\n# Get description of the database\nprint(client.databases[0].description)\n\n# Perform search on a database\n# Note that the search queries can be a string with a patch to the FASTA file with queries\nresults = client.databases[0].search(\n    [\n        "ACTAGCTCAGTCAACTAGCTCAGTCCTCAGTCAACTAGCTCAGTCTATATATATACAAC",\n        "ACTAGCTCAGTCAACTAGCTCAGTCCTCAGTCAACTAGCT",\n        "ACTAGCTCAGTCAACTAGCT",\n        "ACTAGCTCAGT",\n    ],\n    search_type="nucleotides",\n)\n\n# Load queries from file:\n# results = client.databases[0].search_file("input.fasta", search_type="nucleotides")\n\n# You can pass list of headers to get:\n#   query_sequence_id\n#   target_sequence_id\n#   query_sequence_content\n#   target_sequence_content\n#   sequence_identity\n#   alignment_length\n#   number_of_mismatches\n#   number_of_gap_openings\n#   domain_start_index_query\n#   domain_end_index_query\n#   domain_start_index_target\n#   domain_end_index_target\n#   e_value\n#   bit_score\n# For example:\n# results2 = client.databases[0].search(\n#     [\n#         "ACTAGCTCAGTCAACTAGCTCAGTCCTCAGTCAACTAGCTCAGTCTATATATATACAAC",\n#         "ACTAGCTCAGTCAACTAGCTCAGTCCTCAGTCAACTAGCT",\n#         "ACTAGCTCAGTCAACTAGCT",\n#         "ACTAGCTCAGT",\n#     ],\n#     search_type="nucleotides",\n#     headers=["query_sequence_id", "target_sequence_id", "sequence_identity", "alignment_length", "number_of_mismatches"]\n# )\n\n# results.records is a list of lists. Each item contains alignments for each query.\n# Each list of alignments consists of single result\n# print(results.records)\n\n# You can also get a pandas dataframe\nprint(results.dataframe)\n\n```\n',
    'author': 'Piotr Styczyński',
    'author_email': 'piotr@styczynski.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
