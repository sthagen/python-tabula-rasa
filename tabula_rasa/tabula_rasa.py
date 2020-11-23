# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Add logical documentation here later TODO."""
import collections
import json
import re
import sys
from typing import Union, List


ENCODING = 'utf-8'
#         '3 .  1 .  42 * A KEY OR SO THEY SAY A_KEY A/N 4\n'
#         '3 .  2 .  142  A LABEL OR WHATEVER LABEL A 42/84\n'
#         '3 .  3 .  2  NAME NAME (Version 8.1) A 123\n'
#         '3 .  4 .  7 * ANOTHER KEY UNEXPECTEDLY ANOTHER N 3'
#          t    v    f k c                        n       d b
RECORD_PATTERN = re.compile(r'(?P<t>\d+?)\s\.\s(?P<v>\d+?)\s\.\s(?P<f>\d+?)(?P<k>[ *]+)(?P<c>.*)\s(?P<n>[^ ]+)\s(?P<d>[^ ]+)\s(?P<b>[^ ]+)')
META_KEYS = ('t', 'v', 'f', 'k', 'c', 'n', 'd', 'b')
KEY_INDEX = META_KEYS.index('k')
Record = collections.namedtuple('Record', META_KEYS)

STOP_TOKENS = (
    '(Version 8.1)',
)
EMPTY = ''
SEP = ','
VARIANT_SEP = '/'


def parse_bytes_rule(field: str) -> List[int]:
    """Bytes may contain variants separated by a slash (/)."""
    return [int(v) for v in field.split(VARIANT_SEP)] if VARIANT_SEP in field else [int(field)]


def rules_from(legend: List[Record]):
    """Extract parsing rules from legend."""
    table = legend[0][0]
    rules = {
        'table': int(table),
        'field_indices': [],
        'field_domain_refs': [],
        'key_filter': [],
        'comments': [],
        'names': [],
        'domain_codes': [],
        'byte_sizes': [],
    }

    for entry in legend:
        rules['field_indices'].append(int(entry.v))
        rules['field_domain_refs'].append(int(entry.f))
        rules['key_filter'].append(entry.k)
        rules['comments'].append(entry.c)
        rules['names'].append(entry.n)
        rules['domain_codes'].append(entry.d)
        rules['byte_sizes'].append(parse_bytes_rule(entry.b))
    return rules


def json_from(rules: Dict) -> None:
    """Transform to parser rules schema JSON format.
    {
      "name": "IR_CTRY",
      "summary": "ICAO Region country record.",
      "fields": [ "FIELD" ],
      "is_key_field": [ true ],
      "number_triple": [ [1, 1, 2] ],
      "type_code": [ "A/N" ],
      "length_bytes": [ 7 ],
      "labels": [ "LABEL" ],
      "sample_header": "TSV_HEADER_ROW\n",
      "sample_data": "TSV_DATA_ROW\n"
    },
    """
    name = "NOT_YET_COLLECTED"
    summary = "NOT_YET_COLLECTED_EITHER"
    triplets = [[rules['table'], i, dr] for i, dr in zip(rules['field_indices'], rules['field_domain_refs'])]
    data = {
          "name": name,
          "summary": summary,
          "fields": rules['names'],
          "is_key_field": [True if c == '*' else False for c in rules['key_filter']],
          "number_triple": triplets,
          "type_code": rules['domain_codes'],
          "length_bytes": rules['byte_sizes'],
          "labels": rules['comments'],
          "sample_header": "TSV_HEADER_ROW\n",
          "sample_data": "TSV_DATA_ROW\n"
    },
    path = f'{name}.json'
    with open(path, "wt", encoding=ENCODING) as handle:
        json.dump(data, handle, indent=2)


def update_from(record: Record, legend: Union[List, None] = None) -> List:
    """Add legend entry from record."""
    if legend is None:
        legend = []
    legend.append(record)
    return legend


def remove_stop_tokens(text: str) -> str:
    """Special case ..."""
    for stop_token in STOP_TOKENS:
        if stop_token in text:
            text = text.replace(stop_token, EMPTY)
    return text


def parse_legend_entry(text) -> Union[Record, str]:
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

    patch_key_field(data)

    return Record(*data)


def patch_key_field(data):
    """Replace ' * ' with '*' and keep non-key field marker as ' '."""
    entry = data[KEY_INDEX].strip()
    if not entry:
        entry = ' '
    data[KEY_INDEX] = entry


def dump_record(record: Record):
    """DRY."""
    return SEP.join(record)


def load(path):
    """Temporary implementation to bootstrap testing file loading."""
    with open(path, "rt", encoding=ENCODING) as handle:
        for line in handle:
            yield line.strip().strip('\r')  # HACK A DID ACK
