"""
Functions which transform string content
"""
import re
from typing import Type, Sequence, Dict, cast

import pyexlatex as pl
from pyexlatex.models.section.base import SectionBase

SECTION_CLASSES: Sequence[Type[SectionBase]] = [
    pl.Chapter,
    pl.Section,
    pl.SubSection,
    pl.SubSubSection,
    pl.Paragraph,
    pl.SubParagraph,
]
SECTION_CLASSES_BY_NAME: Dict[str, Type[SectionBase]] = {
    cls.name: cls for cls in SECTION_CLASSES
}
NEXT_LEVEL_UP_CLASSES_BY_NAME: Dict[str, Type[SectionBase]] = {}
for name, cls in SECTION_CLASSES_BY_NAME.items():
    down_cls = cls.next_level_down_class
    if down_cls is not None:
        down_name = down_cls.name
        NEXT_LEVEL_UP_CLASSES_BY_NAME[down_name] = cls


def elevate_sections_by_one_level(content: str) -> str:
    """
    Converts Sections to Chapters, SubSections to Sections,
    SubSubSections to SubSections. Raises error if a Chapter is
    encountered

    :param content:
    :return:
    """
    patterns: Dict[str, str] = {}
    for name, cls in SECTION_CLASSES_BY_NAME.items():
        patterns[name] = r"\\" + name + "{"
        patterns[f"begin_{name}"] = r"\\begin{" + name + "}"
        patterns[f"end_{name}"] = r"\\end{" + name + "}"

    # Adapted from tokenizer example in re docs
    full_regex = "|".join(
        f"(?P<{name}>{pattern})" for name, pattern in patterns.items()
    )
    result = re.sub(full_regex, _replace_with_next_level_up_section, content)
    return result


def _replace_with_next_level_up_section(match: re.Match) -> str:
    kind = cast(str, match.lastgroup)
    name = kind.split("_")[-1]
    cls = SECTION_CLASSES_BY_NAME[name]
    new_cls = NEXT_LEVEL_UP_CLASSES_BY_NAME.get(name, None)
    if new_cls is None:
        raise ValueError(
            f"cannot convert {cls} to next level up as it is "
            f"not a next_level_down_class for any other section type. "
            f"Cannot convert {match.group()}"
        )
    new_name = new_cls.name
    if kind.startswith("begin"):
        return r"\begin{" + new_name + "}"
    if kind.startswith("end"):
        return r"\end{" + new_name + "}"

    # Must be plain match like \section{My Section}
    return "\\" + new_name + "{"
