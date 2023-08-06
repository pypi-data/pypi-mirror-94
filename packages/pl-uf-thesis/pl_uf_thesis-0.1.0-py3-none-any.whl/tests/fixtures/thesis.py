from copy import deepcopy

import pytest
import pyexlatex as pl
import pandas as pd

from plufthesis.info_models import ThesisTypes
from plufthesis.thesis import UFThesis
from plufthesis.transformers import elevate_sections_by_one_level
from tests.config import INPUT_FILES_DIR

EXAMPLE_BODY = [
    pl.Chapter(
        [
            'Some content',
            pl.UnorderedList(['a', 'b', 'c']),
        ],
        title='First'
    ),
    pl.Chapter(
        [
            'Chapter content',
            pl.Section(
                [
                    'Section content',
                    pl.SubSection(
                        [
                            'Subsection content',
                            pl.SubSubSection(
                                [
                                    'Subsubsubsection content'
                                ],
                                title='First sub sub'
                            )
                        ],
                        title='First sub'
                    )
                ],
                title='First section'
            )
        ],
        title='Second'
    )
]
EXAMPLE_BODY_NEXT_LEVEL_DOWN = [
    pl.Section(
        [
            'Some content',
            pl.UnorderedList(['a', 'b', 'c']),
        ],
        title='First'
    ),
    pl.Section(
        [
            'Chapter content',
            pl.SubSection(
                [
                    'Section content',
                    pl.SubSubSection(
                        [
                            'Subsection content',
                            pl.Paragraph(
                                [
                                    'Subsubsubsection content'
                                ],
                                title='First sub sub'
                            )
                        ],
                        title='First sub'
                    )
                ],
                title='First section'
            )
        ],
        title='Second'
    )
]
TITLE = 'Insert Title Here'
AUTHOR = 'Nick DeRobertis'
MAJOR = 'Insert Major Here'
CHAIR = 'Insert Chair Here'
ABSTRACT = "Insert abstract here"
BIBLIOGRAPHY = pl.Bibliography([pl.BibTexArticle('person', 'Last, First', 'An article title', 'Journal of Journals', '2021', '10', '1', '255-256')])
DEGREE_YEAR = 2021

EXAMPLE_DF = pd.DataFrame(
    [
        (1, 2),
        (3, 4)
    ],
    columns=('a', 'b')
)
GRAPHIC_FILE = INPUT_FILES_DIR / 'nd-logo.png'
EXAMPLE_BODY_WITH_TABLES_FIGURES = deepcopy(EXAMPLE_BODY)
EXAMPLE_BODY_WITH_TABLES_FIGURES.append(
    pl.Chapter(
        [
            'Some text',
            pl.Table.from_list_of_lists_of_dfs([[EXAMPLE_DF]], caption='My Table'),
            'More text',
            pl.Figure.from_dict_of_names_and_filepaths({'My Figure': str(GRAPHIC_FILE)})
        ],
        title='My Tables and Figures'
    )
)

# Optional arguments
ABBREVIATIONS = 'ABC is for the alphabet',
APPENDIX_ONE = pl.Chapter('First appendix content', 'Appendix One')
APPENDIX_TWO = pl.Chapter('Second appendix content', 'Appendix Two')
SINGLE_APPENDIX = (APPENDIX_ONE,)
MULTIPLE_APPENDIX = (APPENDIX_ONE, APPENDIX_TWO)
CO_CHAIR = 'Insert Co-Chair Here'
THESIS_TYPE = ThesisTypes.THESIS
DEGREE_TYPE = 'Master of Science'
DEGREE_MONTH = 'August'

ARGS = (
    EXAMPLE_BODY,
    TITLE,
    AUTHOR,
    MAJOR,
    CHAIR,
    ABSTRACT,
    BIBLIOGRAPHY
)

KWARGS = dict(
    degree_year=DEGREE_YEAR
)


@pytest.fixture(scope='session')
def thesis():
    return UFThesis(*ARGS, **KWARGS)


@pytest.fixture(scope='session')
def thesis_full_single_appendix():
    return UFThesis(
        *ARGS, **KWARGS,
        abbreviation_contents=ABBREVIATIONS,
        appendix_contents=SINGLE_APPENDIX,
        co_chair=CO_CHAIR,
        thesis_type=THESIS_TYPE,
        degree_type=DEGREE_TYPE,
        degree_month=DEGREE_MONTH,
    )


@pytest.fixture(scope='session')
def thesis_multiple_appendix():
    return UFThesis(
        *ARGS, **KWARGS,
        appendix_contents=MULTIPLE_APPENDIX,
        multiple_appendices=True,
    )


@pytest.fixture(scope='session')
def thesis_tables_and_figures():
    tf_args = (
        EXAMPLE_BODY_WITH_TABLES_FIGURES,
        *ARGS[1:]
    )
    return UFThesis(
        *tf_args, **KWARGS,
        has_figures=True,
        has_tables=True,
    )


@pytest.fixture(scope='session')
def thesis_from_next_level_down():
    tf_args = (
        EXAMPLE_BODY_NEXT_LEVEL_DOWN,
        *ARGS[1:]
    )
    return UFThesis(*tf_args, **KWARGS, pre_output_func=elevate_sections_by_one_level)