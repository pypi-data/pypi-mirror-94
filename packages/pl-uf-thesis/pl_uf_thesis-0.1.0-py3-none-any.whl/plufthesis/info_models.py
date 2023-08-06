from enum import Enum
from typing import Optional

from pyexlatex.models.item import SimpleItem


class DegreeType(SimpleItem):
    name = 'degreeType'

    def __init__(self, dtype: str):
        self.dtype = dtype
        super().__init__(self.name, dtype)


class DegreeYear(SimpleItem):
    name = 'degreeYear'

    def __init__(self, year: int):
        self.year = year
        super().__init__(self.name, str(year))


class DegreeMonth(SimpleItem):
    name = 'degreeMonth'

    def __init__(self, month: str):
        self.month = month
        super().__init__(self.name, month)


class Major(SimpleItem):
    name = 'major'

    def __init__(self, major: str):
        self.major = major
        super().__init__(self.name, major)


class ThesisTypes(str, Enum):
    DISSERTATION = 'Dissertation'
    THESIS = 'Thesis'


class ThesisType(SimpleItem):
    name = 'thesisType'

    def __init__(self, ttype: ThesisTypes):
        self.ttype = ttype
        super().__init__(self.name, ttype.value)


class Chair(SimpleItem):
    name = 'chair'

    def __init__(self, chair: str, co_chair: Optional[str] = None):
        self.chair = chair
        self.co_chair = co_chair
        modifiers: Optional[str] = None
        if co_chair:
            modifiers = self._wrap_with_bracket(co_chair)
        super().__init__(self.name, chair, pre_modifiers=modifiers)