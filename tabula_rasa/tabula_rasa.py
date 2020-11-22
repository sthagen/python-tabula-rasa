# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Add logical documentation here later TODO."""
import sys
ENCODING = 'utf-8'


def parse(text):
    """Temporary implementation to bootstrap testing.

    Examples:
    ---------
    The inputs:
        '3 .  1 .  42 * A KEY OR SO THEY SAY A_KEY A/N 4\n'
        '3 .  2 .  142  A LABEL OR WHATEVER LABEL A 42/84\n'
        '3 .  3 .  2  NAME NAME (Version 8.1) A 123\n'
        '3 .  4 .  7 * ANOTHER KEY UNEXPECTEDLY ANOTHER N 3'

    should yield:
        3,1,42,*,A KEY OR SO THEY SAY,A_KEY,A/N,4
        3,2,142, ,A LABEL OR WHATEVER LABEL,A,42/84
        3,3,2, ,NAME,NAME,A,123
        3,4,7,*,ANOTHER KEY UNEXPECTEDLY,ANOTHER,N,3
    (one per call)
    """

    return text


def load(path):
    """Temporary implementation to bootstrap testing file loading."""
    with open(path, "rt", encoding=ENCODING) as handle:
        for line in handle:
            yield line.strip().strip('\r')  # HACK A DID ACK
