#!/usr/bin/env python

import sys
import os

project = 'Bit'
copyright = '2012, Tres Walsh'

version = '0.4'
release = '0.4'

html_theme = 'default' if os.environ.get('READTHEDOCS', None) else 'haiku'

exclude_patterns = ['_build']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
todo_include_todos = True
extension = ['sphinx.ext.todo']
