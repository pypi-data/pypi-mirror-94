from pathlib import Path

from pyexlatex.models.control.documentclass.classtypes.documentclasstype import DocumentClassType

from plufthesis.config import ASSETS_PATH

UF_THESIS_DISSERTATION_CLS_FILE = ASSETS_PATH / "ufdissertation.cls"
UF_THESIS_DISSERTATION_CLS_TEXT = UF_THESIS_DISSERTATION_CLS_FILE.read_text()

class_type = DocumentClassType('uf-thesis-dissertation', UF_THESIS_DISSERTATION_CLS_TEXT)

# TODO [$602039315315e00008a1abd9]: replace this once pyexlatex has a more convenient way of adding custom class types
def register_doc_type():
    from pyexlatex.models.control.documentclass.classtypes.custom import CUSTOM_CLASS_TYPES
    CUSTOM_CLASS_TYPES[class_type.name] = class_type