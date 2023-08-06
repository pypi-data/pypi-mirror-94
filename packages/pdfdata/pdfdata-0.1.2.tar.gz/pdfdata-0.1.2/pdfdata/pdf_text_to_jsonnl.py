import json
from pdfdata import parse_pdf, pdf_doc_extract_span_df


def pdf_text_to_jsonnl(file_in, file_out):
    doc = parse_pdf(file_path=file_in)
    span_df = pdf_doc_extract_span_df(doc)

    with open(file=file_out, mode='a') as fout:
        fout.truncate(0)
        for j in span_df:
            json.dump(obj=j, fp=fout)
            fout.write('\n')
