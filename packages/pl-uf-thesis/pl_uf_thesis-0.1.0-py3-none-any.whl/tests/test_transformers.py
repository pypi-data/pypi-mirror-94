import pyexlatex as pl
import pytest
from pyexlatex.logic.builder import build

from plufthesis.transformers import elevate_sections_by_one_level

SUB_SUB_SECTION = pl.SubSubSection("Sub sub content", title="Sub Sub section")
SUB_SECTION = pl.SubSection(["Sub content", SUB_SUB_SECTION], title="Sub section")
SECTION = pl.Section(["Section content", SUB_SECTION], title="Section")
CHAPTER = pl.Chapter(["Chapter content", SECTION], title='Chapter')

SECTIONS_BY_TEXT = r"""
\section{Section}
Section content
\subsection{Sub section}
Sub content
\subsubsection{Sub Sub section}
Sub sub content
"""

CHAPTERS_BY_TEXT = r"""
\chapter{Chapter}
Chapter content
""" + SECTIONS_BY_TEXT


def test_elevate_sections_objects_success():
    content = build([SECTION])
    revised = elevate_sections_by_one_level(content)
    assert (
        revised
        == "\\begin{chapter}{Section}\nSection content\n\\begin{section}{Sub section}\nSub content\n\\begin{subsection}{Sub Sub section}\nSub sub content\n\\end{subsection}\n\\end{section}\n\\end{chapter}"
    )


def test_elevate_sections_text_success():
    revised = elevate_sections_by_one_level(SECTIONS_BY_TEXT)
    assert (
        revised
        == "\n\\chapter{Section}\nSection content\n\\section{Sub section}\nSub content\n\\subsection{Sub Sub section}\nSub sub content\n"
    )


def test_elevate_sections_objects_chapter():
    content = build([CHAPTER])
    with pytest.raises(ValueError) as exc_info:
        elevate_sections_by_one_level(content)
    assert 'cannot convert' in str(exc_info.value)


def test_elevate_sections_text_chapter():
    with pytest.raises(ValueError) as exc_info:
        elevate_sections_by_one_level(CHAPTERS_BY_TEXT)
    assert 'cannot convert' in str(exc_info.value)
