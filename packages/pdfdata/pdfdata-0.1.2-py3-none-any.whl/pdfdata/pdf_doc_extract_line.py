

def pdf_doc_extract_line_df(pdf_doc):

    text = []

    # .. page - block - line span - info
    for page_i, page in enumerate(pdf_doc):
        blocks = page.getText("dict", flags = 11)["blocks"]

        for block_i, block_item in enumerate(blocks):  # iterate through the text blocks
            lines = block_item["lines"]

            for line_i, line_item in enumerate(lines):  # iterate through the text lines
                spans = line_item["spans"]

                line_text = ""
                for span_item in line_item["spans"]:  # iterate through the text spans
                    line_text = line_text.join(span_item['text'])

                text.append(
                    {
                        "page_number":   page_i + 1,
                        "page_blocks_n": len(blocks),
                        "block_number":  block_i + 1,
                        "block_lines_n": len(lines),
                        "block_bbox_x1": blocks[block_i]["bbox"][0],
                        "block_bbox_y1": blocks[block_i]["bbox"][1],
                        "block_bbox_x2": blocks[block_i]["bbox"][2],
                        "block_bbox_y2": blocks[block_i]["bbox"][3],
                        "line_number":   line_i + 1,
                        "line_spans_n":  len(spans),
                        "text":     line_text
                    }
                )
    # return
    return text


if __name__ == "__main__":
    
    from pdfdata.parse_pdf import parse_pdf
    from pprint import pprint
    import os

    pprint(os.getcwd())
    try:
      text_data = pdf_doc_extract_line_df(parse_pdf('../pdfs/simple_text_2".pdf'))
    except RuntimeError:
      text_data = pdf_doc_extract_line_df(parse_pdf('pdfs/simple_text_2.pdf'))

    pprint('\n'.join([e['text'] for e in text_data]))
    text = '\n'.join([e['text'] for e in text_data])


    with open('test_text.txt', mode="w") as f:
      f.write(text)

    with open('test_binary.txt', mode="wb") as f:
      f.write( text.encode("utf8") )
