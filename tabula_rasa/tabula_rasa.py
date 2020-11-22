# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Add logical documentation here later TODO."""
import sys
ENCODING = 'utf-8'


def parse(text):
    """Temporary implementation to bootstrap testing."""
    return text


def load(path):
    """Temporary implementation to bootstrap testing file loading."""
    with open(path, "rt", encoding=ENCODING) as handle:
        for line in handle:
            yield line.strip().strip('\r')  # HACK A DID ACK
