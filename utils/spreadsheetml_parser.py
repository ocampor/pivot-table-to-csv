from io import BytesIO

from lxml import etree


def str_xml_to_csv(xml_str, batch_string, metadata=None):
    context = etree.iterparse(BytesIO(xml_str.encode("utf-8")))
    row = []
    idx = 0
    for _, elem in context:
        if elem.tag[-1] != "r":
            row += [get_value(elem.get("v", ""), elem.tag[-1], metadata[idx])]
            idx += 1
        else:
            batch_string.append(",".join(row) + "\n")
            row = []
            idx = 0


def split_xml(xml, n_batches=5):
    cut_size = int(len(xml) / n_batches)
    start_index = 0
    xml_chunks = []
    for idx in range(cut_size, len(xml), cut_size):
        cut_index = _get_next_valid_index(xml, idx)
        xml_chunks += [xml[start_index: cut_index]]
        start_index = cut_index
    return xml_chunks


def get_value(value, tag, metadata=None):
    if metadata is None or value == "":
        return cast_tag_value(tag, value)
    elif tag == "x":
        return cast_tag_value(tag, metadata["levels"][int(value)])
    else:
        return cast_tag_value(tag, value)


def cast_string(value):
    return '"{0}"'.format(value)


def cast_tag_value(tag, value):
    if tag == "s":
        return cast_string(value)
    elif tag == "n" or tag == "x" or tag == "m":
        return value
    else:
        raise TypeError("Tag {0} is not defined to be cased".format(tag))


def get_valid_pivot_cache_records_xml(file_chunks, index):
    header = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                    <pivotCacheRecords 
                        xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
                        xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="xr"
                        xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision" count="2647949">
    """
    footer = "</pivotCacheRecords>"
    if index == 0:
        return file_chunks[index] + footer
    elif index == len(file_chunks) - 1:
        return header + file_chunks[index]
    else:
        return header + file_chunks[index] + footer


def _get_next_valid_index(xml, seed, close_tag="</r>"):
    while xml[seed:seed + len(close_tag)] != close_tag:
        seed += 1
        if seed >= len(xml):
            return len(xml)
    return seed + len(close_tag)



