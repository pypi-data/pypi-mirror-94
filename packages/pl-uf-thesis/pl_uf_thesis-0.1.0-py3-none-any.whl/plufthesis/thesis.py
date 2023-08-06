import datetime
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Union, List, Optional, Sequence, Callable, Dict

import pyexlatex as pl
from pyexlatex import Package
from pyexlatex.logic.builder import build
from pyexlatex.models.control.documentclass.documentclass import DocumentClass
from pyexlatex.models.section.sections import Chapter
from pyexlatex.models.credits.author import Author
from pyexlatex.models.document import DocumentBase
from pyexlatex.models.format.paragraph.sloppy import Sloppy
from pyexlatex.models.title.title import Title
from pyexlatex.typing import PyexlatexItems
import plufthesis.info_models as im

from plufthesis.info_models import ThesisTypes


class UFThesis(DocumentBase):
    """
    The main high-level class for creating UF theses/dissertations
    """
    name = 'document'

    def __init__(self, content: PyexlatexItems, title: str, author: str,
                 major: str, chair: str, abstract: PyexlatexItems,
                 bibliography: pl.Bibliography,
                 dedication_contents: PyexlatexItems = 'I dedicate this to...',
                 acknowledgements_contents: PyexlatexItems = 'I would like to thank...',
                 biographical_contents: PyexlatexItems = 'Nick made this Pyexlatex template from the LaTeX template, then got a Ph.D.',
                 abbreviation_contents: Optional[PyexlatexItems] = None,
                 appendix_contents: Optional[Sequence[Chapter]] = None,
                 multiple_appendices: bool = False,
                 bibliography_style: str = 'amsplain',
                 co_chair: Optional[str] = None,
                 thesis_type: ThesisTypes = ThesisTypes.DISSERTATION,
                 degree_type: str = 'Doctorate of Philosophy',
                 degree_year: int = datetime.datetime.today().year,
                 degree_month: str = 'May',
                 has_tables: bool = False, has_figures: bool = False,
                 has_objects: bool = False,
                 packages: Optional[List[Union[Package, str]]]=None,
                 pre_env_contents: Optional[PyexlatexItems] = None,
                 pre_output_func: Optional[Callable] = None):

        self.init_data()

        self.document_class_obj = DocumentClass(
            document_type='uf-thesis-dissertation',
            options=['editMode'],
        )

        from pyexlatex.models.item import ItemBase
        if pre_env_contents is None:
            pre_env_contents_list = []
        elif isinstance(pre_env_contents, (ItemBase, str)):
            pre_env_contents_list = [pre_env_contents]
        else:
            pre_env_contents_list = pre_env_contents  # type: ignore

        if has_tables:
            pre_env_contents_list.append(pl.Raw(r'\haveTablestrue'))
        if has_figures:
            pre_env_contents_list.append(pl.Raw(r'\haveFigurestrue'))
        if has_objects:
            pre_env_contents_list.append(pl.Raw(r'\haveObjectstrue'))

        self.temp_tex_contents: Dict[str, PyexlatexItems] = dict(
            dedicationFile=dedication_contents,
            acknowledgementsFile=acknowledgements_contents,
            abstractFile=abstract,
            referenceFile=bibliography,
            biographyFile=biographical_contents,
        )

        set_ref_file = r'\setReferenceFile{referenceFile}{' + bibliography_style + '}%'

        pre_env_contents_list.extend([
            Sloppy(),
            Title(title),
            im.DegreeType(degree_type),
            im.Major(major),
            Author(author, short_author=None),
            im.ThesisType(thesis_type),
            im.DegreeYear(degree_year),
            im.DegreeMonth(degree_month),
            im.Chair(chair, co_chair),
            pl.Raw(r"""
\setDedicationFile{dedicationFile}%                 Dedication Page
\setAcknowledgementsFile{acknowledgementsFile}%     Acknowledgements Page
\setAbstractFile{abstractFile}%                     Abstract Page (This should only include the abstract itself)
\setBiographicalFile{biographyFile}%                Biography file of the Author (you).
            """),
            pl.Raw(set_ref_file),
        ])

        if multiple_appendices:
            pre_env_contents_list.append(pl.Raw(r"""
\multipleAppendixtrue%                          Uncomment this if you have more than one appendix, 
%                                                   comment it if you have only one appendix.
            """))

        if abbreviation_contents is not None:
            pre_env_contents_list.append(pl.Raw(r"""
\setAbbreviationsFile{abbreviations}%           Abbreviations Page
            """))
            self.temp_tex_contents.update(abbreviations=abbreviation_contents)

        if appendix_contents is not None:
            pre_env_contents_list.append(pl.Raw(r"""
\setAppendixFile{appendix}%                     Appendix Content; hyperlinking might be weird.
                        """))
            self.temp_tex_contents.update(appendix=appendix_contents)

        super().__init__(
            content,
            packages=packages,
            pre_env_contents=pre_env_contents_list,
            pre_output_func=pre_output_func,
        )

    def _write_temp_tex_file(self, name: str, content: PyexlatexItems, directory: Path):
        out_path = directory / f'{name}.tex'
        text_content = build(content)
        out_path.write_text(text_content)
        self.data.filepaths.append(str(out_path))
        self.data.binaries.append(bytes(text_content, 'utf8'))

    def _write_temp_tex_files(self, directory: Path):
        for name, content in self.temp_tex_contents.items():
            self._write_temp_tex_file(name, content, directory)

    def to_pdf(self, *args, **kwargs):
        with TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            orig_data = deepcopy(self.data)
            self._write_temp_tex_files(tmp_dir)
            result = super().to_pdf(*args, **kwargs)
            self.data = orig_data
        return result

    def to_html(self, *args, **kwargs):
        with TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            orig_data = deepcopy(self.data)
            self._write_temp_tex_files(tmp_dir)
            result = super().to_html(*args, **kwargs)
            self.data = orig_data
        return result
