# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Add logical documentation here later TODO."""
import collections
import re
import sys

ENCODING = 'utf-8'
#         '3 .  1 .  42 * A KEY OR SO THEY SAY A_KEY A/N 4\n'
#         '3 .  2 .  142  A LABEL OR WHATEVER LABEL A 42/84\n'
#         '3 .  3 .  2  NAME NAME (Version 8.1) A 123\n'
#         '3 .  4 .  7 * ANOTHER KEY UNEXPECTEDLY ANOTHER N 3'
#          t    v    f k c                        n       d b
RECORD_PATTERN = re.compile(r'(?P<t>\d+?)\s\.\s(?P<v>\d+?)\s\.\s(?P<f>\d+?)(?P<k>[ *]+)(?P<c>.*)\s(?P<n>[^ ]+)\s(?P<d>[^ ]+)\s(?P<b>[^ ]+)')
META_KEYS = ('t', 'v', 'f', 'k', 'c', 'n', 'd', 'b')
Record = collections.namedtuple('Record', META_KEYS)

STOP_TOKENS = (
    '(Version 8.1)',
)
EMPTY = ''
SEP = ','


def remove_stop_tokens(text):
    """Special case ..."""
    for stop_token in STOP_TOKENS:
        if stop_token in text:
            text = text.replace(stop_token, EMPTY)
    return text


def parse_legend_entry(text):
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
    # Normalize space like characters to single space
    fields = ' '.join(remove_stop_tokens(text).split())
    m = RECORD_PATTERN.search(fields)
    if not m:
        return EMPTY

    data = [m[key] for key in META_KEYS]

    patch_key_field = data[3].strip()
    if not patch_key_field:
        patch_key_field = ' '
    data[3] = patch_key_field

    record = Record(*data)
    return SEP.join(record)


def load(path):
    """Temporary implementation to bootstrap testing file loading."""
    with open(path, "rt", encoding=ENCODING) as handle:
        for line in handle:
            yield line.strip().strip('\r')  # HACK A DID ACK
