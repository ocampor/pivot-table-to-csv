from lxml import etree
from io import BytesIO


def str_xml_to_csv(xml_str, batch_string):
    context = etree.iterparse(BytesIO(xml_str.encode("utf-8")))
    row = []
    for _, elem in context:
        if elem.tag[-1] != "r":
            row += [elem.get("v", "")]
        else:
            batch_string.append("^".join(row) + "\n")
            row = []


def split_xml(file_name, n_batches=5):
    long_xml = open(file_name).read()
    cut_size = int(len(long_xml) / n_batches)
    start_index = 0
    xml_chunks = []
    for idx in range(cut_size, len(long_xml), cut_size):
        cut_index = _get_next_valid_index(long_xml, idx)
        xml_chunks += [long_xml[start_index: cut_index]]
        start_index = cut_index
    return xml_chunks


def _get_next_valid_index(xml, seed, close_tag="</r>"):
    while xml[seed:seed + len(close_tag)] != close_tag:
        seed += 1
        if seed == len(xml):
            return len(xml)
    return seed + len(close_tag)
