#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Add logical documentation here later TODO."""
import os
import pathlib
import sys

import tabula_rasa.tabula_rasa as tr

DEBUG = os.getenv("TABULA_RASA_DEBUG")


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
                if record:
                    tr.update_from(record, legend)
        else:
            data = text
            record = tr.parse_legend_entry(data)
            if record:
                tr.update_from(record, legend)

    if DEBUG:
        for entry in legend:
            print(tr.dump_record(entry))

    if legend:
        rules = tr.rules_from(legend)
        print(f"Table no. {rules['table']}:")
        for field in range(len(rules['field_indices'])):
            print(
                f"  Field[{rules['field_indices'][field]}]({rules['names'][field]})(type='{rules['domain_codes'][field]}',"
                f" byte_sizes_max={rules['byte_sizes'][field][-1]}, comment='{rules['comments'][field]}'")
                                                                                    
        tr.json_from(rules)

