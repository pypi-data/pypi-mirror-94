from pyexlatex.models.document import DocumentBase

from tests.config import GENERATED_FILES_DIR, INPUT_FILES_DIR
from tests.utils.pdf import compare_pdfs


def compare_doc(doc: DocumentBase, name: str):
    doc.to_pdf(GENERATED_FILES_DIR, outname=name)
    compare_pdfs(INPUT_FILES_DIR / f'{name}.pdf', GENERATED_FILES_DIR / f'{name}.pdf')