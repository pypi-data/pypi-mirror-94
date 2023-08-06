from pdfdata import flag_decomposer


def pdf_doc_extract_span_list ( pdf_doc ):
    text = {
        "pages":             [],
        "chapters":          [],
        "embedded_files_n":  pdf_doc.embeddedFileCount(),
        "table_of_contents": []
    }

    # toc
    for i, toc in enumerate(pdf_doc.getToC()):
        text["table_of_contents"].append({
            "toc_number":         i + 1,
            "toc_page":           toc[0],
            "toc_text":           toc[1],
            "toc_page_reference": toc[2]
        })

    # .. chapter info
    for i in range(pdf_doc.chapterCount):
        text["chapters"].append(
            {
                "pages_n": pdf_doc.chapterPageCount(i)
            }
        )

    # .. page - block - line span - info
    for page_i, page in enumerate(pdf_doc):
        blocks = page.getText("dict", flags = 11)["blocks"]
        text['pages'].append(
            {
                "page_number": page_i + 1,
                "blocks_n":    len(blocks),
                "blocks":      []
            }
        )

        for block_i, block_item in enumerate(blocks):  # iterate through the text blocks
            lines = block_item["lines"]
            text['pages'][page_i]['blocks'].append(
                {
                    "block_number": block_i + 1,
                    "lines_n":      len(lines),
                    "lines":        []
                }
            )
            for line_i, line_item in enumerate(lines):  # iterate through the text lines
                spans = line_item["spans"]
                text['pages'][page_i]['blocks'][block_i]["lines"].append(
                    {
                        "line_number": line_i + 1,
                        "spans_n":     len(spans),
                        "spans":       []
                    }
                )

                for span_i, span_item in enumerate(line_item["spans"]):  # iterate through the text spans
                    flags = flag_decomposer(span_item["flags"])
                    text['pages'][page_i]['blocks'][block_i]["lines"][line_i]["spans"].append(
                        {
                            "span_number": span_i + 1,
                            "character_n": len(span_item['text']),
                            "text":        span_item['text'],
                            "font_size":   span_item["size"],
                            "font_color":  "#%06x" % (span_item["color"]),
                            "font_font":   span_item["font"],
                            "font_flags":  span_item["flags"],
                            "superscript": flags["superscript"],
                            "italic":      flags["italic"],
                            "serifed":     flags["serifed"],
                            "monospaced":  flags["monospaced"],
                            "bold":        flags["bold"],
                            "bbox_x1":     span_item["bbox"][0],
                            "bbox_y1":     span_item["bbox"][1],
                            "bbox_x2":     span_item["bbox"][2],
                            "bbox_y2":     span_item["bbox"][3],
                            "x":           span_item["origin"][0],
                            "y":           span_item["origin"][1]
                        }
                    )

    # return
    return text
