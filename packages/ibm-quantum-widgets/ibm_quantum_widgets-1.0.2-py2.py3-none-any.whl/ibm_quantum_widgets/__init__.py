#!/usr/bin/env python
# coding: utf-8

# Copyright (c) IBM Research.
# Distributed under the terms of the Modified BSD License.

import os

enable_widgets = os.environ.get('IQX_WIDGETS')
if (enable_widgets == 'yes'):
  from .circuit_composer import CircuitComposer
  from .draw_circuit import draw_circuit
  from .edit_circuit import edit_circuit

from ._version import __version__, version_info
from .nbextension import _jupyter_nbextension_paths
