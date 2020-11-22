# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import io
import pathlib
import pytest  # type: ignore

import tabula_rasa.cli as cli
import tabula_rasa.tabula_rasa as tr


TEXT_FIXTURE_LEGEND_PATH = pathlib.Path('tests', 'fixtures', 'text', 'tabula.txt')
CSV_FIXTURE_RULES_PATH = pathlib.Path('tests', 'fixtures', 'csv', 'tabula.txt')
TSV_FIXTURE_DATA_PATH = pathlib.Path('tests', 'fixtures', 'tsv', 'tabula.txt')


def test_main_ok_minimal(capsys):
    job = ['does not matter']
    report_expected = tr.EMPTY
    assert cli.main(job) is None
    out, err = capsys.readouterr()
    assert out.strip() == report_expected.strip()


def test_main_ok_file(capsys):
    job = [str(TEXT_FIXTURE_LEGEND_PATH)]
    report_expected = (
        'Table no. 3:\n'
        "  Field[1](A_KEY)(type='A/N', byte_sizes_max=4, comment='A KEY OR SO THEY SAY'\n"
        "  Field[2](LABEL)(type='A', byte_sizes_max=84, comment='A LABEL OR WHATEVER'\n"
        "  Field[3](NAME)(type='A', byte_sizes_max=123, comment='NAME'\n"
        "  Field[4](ANOTHER)(type='N', byte_sizes_max=3, comment='ANOTHER KEY UNEXPECTEDLY'"
    )

    assert cli.main(job) is None
    out, err = capsys.readouterr()
    assert out.strip() == report_expected.strip()


def generate_tsv_data():
    tab = '\t'
    out_path = str(TSV_FIXTURE_DATA_PATH)
    data = (
        ('A_KEY', 'LABEL', 'NAME', 'ANOTHER',),
        ('EDDK', 'RUNWAY OR SO', 'IS IT JUST A NAME OR IS IT SOMETHING ELSE?', '123',),
        ('KJFK', 'SOMETHING ACROSS THE OCEAN', 'DO NOT WORRY ABOUT THE NAME', '456',),
    )
    with open(out_path, 'wt', encoding=tr.ENCODING) as handle:
        for row in data:
            handle.write(tab.join(row))
            handle.write('\n')

    assert TSV_FIXTURE_DATA_PATH.is_file() is True
