# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import io
import pathlib
import pytest  # type: ignore

import tabula_rasa.cli as cli

TEXT_FIXTURE_PATH = pathlib.Path('tests', 'fixtures', 'text', 'tabula.txt')


def test_main_ok_minimal(capsys):
    job = ['does not matter']
    report_expected = ''
    assert cli.main(job) is None
    out, err = capsys.readouterr()
    assert out.strip() == report_expected.strip()


def test_main_ok_file(capsys):
    job = [str(TEXT_FIXTURE_PATH)]
    report_expected = (
        '3,1,42, * ,A KEY OR SO THEY SAY,A_KEY,A/N,4\n'
        '3,2,142, ,A LABEL OR WHATEVER,LABEL,A,42/84\n'
        '3,3,2, ,NAME,NAME,A,123\n'
        '3,4,7, * ,ANOTHER KEY UNEXPECTEDLY,ANOTHER,N,3'
    )
    assert cli.main(job) is None
    out, err = capsys.readouterr()
    assert out.strip() == report_expected.strip()
