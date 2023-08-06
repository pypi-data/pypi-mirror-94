from pdfdata import flag_decomposer


def pdf_doc_extract_span_df(pdf_doc):

    text = []

    # .. page - block - line span - info
    for page_i, page in enumerate(pdf_doc):
        blocks = page.getText("dict", flags = 11)["blocks"]

        for block_i, block_item in enumerate(blocks):  # iterate through the text blocks
            lines = block_item["lines"]

            for line_i, line_item in enumerate(lines):  # iterate through the text lines
                spans = line_item["spans"]

                for span_i, span_item in enumerate(line_item["spans"]):  # iterate through the text spans
                    flags = flag_decomposer(span_item["flags"])
                    text.append(
                        {
                            "page_number":      page_i + 1,
                            "page_blocks_n":    len(blocks),

                            "block_number":     block_i + 1,
                            "block_lines_n":    len(lines),
                            "block_bbox_x1":     blocks[block_i]["bbox"][0],
                            "block_bbox_y1":     blocks[block_i]["bbox"][1],
                            "block_bbox_x2":     blocks[block_i]["bbox"][2],
                            "block_bbox_y2":     blocks[block_i]["bbox"][3],

                            "line_number":      line_i + 1,
                            "line_spans_n":          len(spans),

                            "span_number":      span_i + 1,
                            "span_character_n": len(spans),
                            "span_font_size":   span_item["size"],
                            "span_font_color":  "#%06x" % (span_item["color"]),
                            "span_font_font":   span_item["font"],
                            "span_font_flags":  span_item["flags"],
                            "span_superscript": flags["superscript"],
                            "span_italic":      flags["italic"],
                            "span_serifed":     flags["serifed"],
                            "span_monospaced":  flags["monospaced"],
                            "span_bold":        flags["bold"],
                            "span_bbox_x1":     span_item["bbox"][0],
                            "span_bbox_y1":     span_item["bbox"][1],
                            "span_bbox_x2":     span_item["bbox"][2],
                            "span_bbox_y2":     span_item["bbox"][3],
                            "span_x":           span_item["origin"][0],
                            "span_y":           span_item["origin"][1],
                            "text":        span_item['text']
                        }
                    )
    # return
    return text


if __name__ == "__main__":
    from pdfdata.parse_pdf import parse_pdf
    from pprint import pprint
    doc_pdf = pdf_doc_extract_span_df(parse_pdf('../pdfs/0641-20.pdf'))
    pprint(doc_pdf)
