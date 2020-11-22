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
        '3,1,42,*,A KEY OR SO THEY SAY,A_KEY,A/N,4\n'
        '3,2,142, ,A LABEL OR WHATEVER,LABEL,A,42/84\n'
        '3,3,2, ,NAME,NAME,A,123\n'
        '3,4,7,*,ANOTHER KEY UNEXPECTEDLY,ANOTHER,N,3'
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
