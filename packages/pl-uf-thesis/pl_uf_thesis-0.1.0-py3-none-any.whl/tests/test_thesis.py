from pathlib import Path

import pyexlatex as pl

from tests.config import INPUT_FILES_DIR
from tests.utils.doc import compare_doc
from tests.fixtures.thesis import (
    thesis,
    thesis_full_single_appendix,
    thesis_multiple_appendix,
    thesis_tables_and_figures,
    thesis_from_next_level_down,
)


def test_create_thesis(thesis):
    name = "thesis"
    doc = thesis

    thesis_path = INPUT_FILES_DIR / f"{name}.tex"
    assert str(doc) == thesis_path.read_text()
    compare_doc(doc, name)


def test_create_thesis_full_single_appendix(thesis_full_single_appendix):
    name = "thesis_full_single_appendix"
    doc = thesis_full_single_appendix

    thesis_path = INPUT_FILES_DIR / f"{name}.tex"
    assert str(doc) == thesis_path.read_text()
    compare_doc(doc, name)


def test_create_thesis_multiple_appendix(thesis_multiple_appendix):
    name = "thesis_multiple_appendix"
    doc = thesis_multiple_appendix

    thesis_path = INPUT_FILES_DIR / f"{name}.tex"
    assert str(doc) == thesis_path.read_text()
    compare_doc(doc, name)


def test_create_thesis_tables_and_figures(thesis_tables_and_figures):
    name = "thesis_tables_and_figures"
    doc = thesis_tables_and_figures

    thesis_path = INPUT_FILES_DIR / f"{name}.tex"
    assert str(doc) == thesis_path.read_text()
    compare_doc(doc, name)


def test_create_thesis_from_next_level_down(thesis_from_next_level_down):
    name = "thesis"
    doc = thesis_from_next_level_down

    thesis_path = INPUT_FILES_DIR / f"{name}.tex"
    assert str(doc) == thesis_path.read_text()
    compare_doc(doc, name)
