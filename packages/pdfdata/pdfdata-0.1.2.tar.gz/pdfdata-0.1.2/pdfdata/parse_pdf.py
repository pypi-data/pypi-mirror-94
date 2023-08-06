import fitz


def parse_pdf(file_path):
    doc = fitz.Document(file_path)
    return doc




