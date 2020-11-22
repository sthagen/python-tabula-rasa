#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Add logical documentation here later TODO."""
import os
import sys

import tabula_rasa.tabula_rasa as tr

DEBUG = os.getenv("TABUA_RASA_DEBUG")


# pylint: disable=expression-not-assigned
def main(argv=None, inline_mode=False, streaming_mode=False):
    """Process ... TODO."""
    argv = argv if argv else sys.argv[1:]
    DEBUG and print(f"Arguments after hand over: ({argv})")
    for text in argv:
        print(tr.parse(text))
