#!/usr/bin/env python
# coding: utf-8

# Copyright (c) IBM Research
# Distributed under the terms of the Modified BSD License.

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension/static',
        'dest': 'ibm_quantum_widgets',
        'require': 'ibm_quantum_widgets/extension'
    }]
