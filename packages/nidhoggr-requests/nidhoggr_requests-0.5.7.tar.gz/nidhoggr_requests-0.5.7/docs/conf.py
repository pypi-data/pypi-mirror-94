#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import nidhoggr_requests

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']

templates_path = ['_templates']
source_suffix = '.rst'

master_doc = 'index'

project = 'nidhoggr-requests'
copyright = "2019, Roman Shishkin"
author = "Roman Shishkin"

version = nidhoggr_requests.__version__
release = nidhoggr_requests.__version__

language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

todo_include_todos = False

html_theme = 'alabaster'

html_theme_options = {
    "fixed_sidebar": True,
    "page_width": "60%"
}

# html_static_path = ['_static']

htmlhelp_basename = 'nidhoggr_requests_doc'
