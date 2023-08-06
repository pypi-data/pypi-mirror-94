from datetime import datetime
from typing import BinaryIO

import PyPDF2
import io

import sign_generator


def sign(name: str, date: datetime, a_hash: str, in_file: BinaryIO) -> io.BytesIO:
    bs = sign_generator.convert(name, date, a_hash)
    original = PyPDF2.PdfFileReader(in_file)
    last_page = original.getPage(original.getNumPages() - 1)
    foreground = PyPDF2.PdfFileReader(bs).getPage(0)
    last_page.mergePage(foreground)
    writer = PyPDF2.PdfFileWriter()
    for i in range(original.getNumPages()):
        page = original.getPage(i)
        writer.addPage(page)

    fp = io.BytesIO()
    writer.write(fp)
    return fp
