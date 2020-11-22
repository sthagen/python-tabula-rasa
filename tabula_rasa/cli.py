#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Add logical documentation here later TODO."""
import os
import pathlib
import sys

import tabula_rasa.tabula_rasa as tr

DEBUG = os.getenv("TABUA_RASA_DEBUG")


# pylint: disable=expression-not-assigned
def main(argv=None, inline_mode=False, streaming_mode=False):
    """Process ... TODO."""
    argv = argv if argv else sys.argv[1:]
    DEBUG and print(f"Arguments after hand over: ({argv})")
    legend = []
    for text in argv:
        if pathlib.Path(text).is_file():
            for data in tr.load(text):
                record = tr.parse_legend_entry(data)
                tr.update_from(record, legend)
        else:
            data = text
            record = tr.parse_legend_entry(data)
            tr.update_from(record, legend)

    for entry in legend:
        print(tr.dump_record(entry))