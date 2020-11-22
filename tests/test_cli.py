# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import io
import pathlib
import pytest  # type: ignore

import tabula_rasa.cli as cli

TEXT_FIXTURE_PATH = pathlib.Path('tests', 'fixtures', 'text', 'tabula.txt')


def test_main_ok_minimal(capsys):
    job = ['does not matter']
    report_expected = job[0]
    assert cli.main(job) is None
    out, err = capsys.readouterr()
    assert out.strip() == report_expected.strip()


def test_main_ok_file(capsys):
    job = [str(TEXT_FIXTURE_PATH)]
    report_expected = ''
    assert cli.main(job) is None
    out, err = capsys.readouterr()
    assert out.strip() == report_expected.strip()
