#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

'''
To build the file:

Make sure the rinoh module is installed, this allows for PDFs to be created

cd /path/to/pytplot/docs
sphinx-build -b rinoh ./source ./build

Or for html files

sphinx-build -b html ./source ./build
'''


import os
import sys
sys.path.insert(0, os.path.realpath("../../"))

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.ifconfig',
    'rinoh.frontend.sphinx']

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'PyTplot'
copyright = '2017, Laboratory for Atmospheric and Space Physics'
author = 'Laboratory for Atmospheric and Space Physics'


version = '1.0.0'
revision = '1.0.0'
language = None

exclude_patterns = []

pygments_style = 'sphinx'

todo_include_todos = False


html_theme = 'alabaster'

html_static_path = ['_static']



htmlhelp_basename = 'PyTplotdoc'


man_pages = [
    (master_doc, 'pytplot', 'PyTplot Documentation',
     [author], 1)
]


autodoc_docstring_signature = True
add_module_names = False
rinoh_documents = [("index",            # top-level file (index.rst)
                    'PyTplot',           # output (target.pdf)
                    'PyTplot Documentation',   # document title
                    'Laboratory for Atmospheric and Space Physics')]   # document author
rinoh_template='article'