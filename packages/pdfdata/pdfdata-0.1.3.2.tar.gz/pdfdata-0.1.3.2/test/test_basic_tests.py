
def test_import():
  import pdfdata


def test_parse_pdf():
  import pdfdata
  pdf = pdfdata.parse_pdf('pdfs/simple_ab.pdf')
  return pdf
  


import pdfdata
simple_ab_pdf = pdfdata.parse_pdf('pdfs/simple_ab.pdf')
simple_text_pdf = pdfdata.parse_pdf('pdfs/simple_text.pdf')
simple_text2_pdf = pdfdata.parse_pdf('pdfs/simple_text_2.pdf')



def test_pdf_doc_extract_line_df():
  pdf_data = pdfdata.pdf_doc_extract_block_line_df(simple_text_pdf)
  assert "text" in pdf_data[0].keys()



def test_pdf_doc_extract_span_df():
  pdf_data = pdfdata.pdf_doc_extract_span_df(simple_text_pdf)
  assert "text" in pdf_data[0].keys()


def test_pdf_doc_extract_span_list():
  pdf_data = pdfdata.pdf_doc_extract_span_list(simple_text_pdf)
  pdf_data


def test_pdf_text_to_jsonnl():
  pdfdata.pdf_text_to_jsonnl(
    file_in = 'pdfs/simple_ab.pdf', 
    file_out = 'pdfs/simple_ab.jsonnl'
  )
  import os
  os.remove('pdfs/simple_ab.jsonnl')
