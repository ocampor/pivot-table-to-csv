from lxml import etree
from io import BytesIO
from multiprocessing import Process, Manager


def get_next_valid_index(xml, seed, close_tag="</r>"):
    while xml[seed:seed + len(close_tag)] != close_tag:
        seed += 1
        if seed == len(xml):
            return len(xml)
    return seed + len(close_tag)


def split_xml(file_name, n_batches=5):
    long_xml = open(file_name).read()
    cut_size = int(len(long_xml) / n_batches)
    start_index = 0
    xml_chunks = []
    for idx in range(cut_size, len(long_xml), cut_size):
        cut_index = get_next_valid_index(long_xml, idx)
        xml_chunks += [long_xml[start_index: cut_index]]
        start_index = cut_index
    return xml_chunks


def str_xml_to_csv(xml_str, batch_string):
    context = etree.iterparse(BytesIO(xml_str.encode('utf-8')))
    row = []
    for _, elem in context:
        if elem.tag[-1] != 'r':
            row += [elem.get("v", "")]
        else:
            batch_string.append('^'.join(row) + '\n')
            row = []


def get_valid_xml(chunks, idx):
    header = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><pivotCacheRecords xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="xr" xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision" count="2647949">'
    footer = '</pivotCacheRecords>'
    if idx == 0:
        return chunks[idx] + footer
    elif idx == len(chunks) - 1:
        return header + chunks[idx]
    else:
        return header + chunks[idx] + footer


if __name__ == "__main__":
    file_name = '/home/ocampor/AMIS/SESAS_2016/robo/xl/pivotCache/pivotCacheRecords1.xml'
    output_file = 'theft_2016.csv'
    batch_string = Manager().list()
    chunks = split_xml(file_name, 5)
    for idx in range(len(chunks)):
        valid_xml = get_valid_xml(chunks, idx)
        p = Process(target=str_xml_to_csv, args=(valid_xml, batch_string, ))
        p.start()
        p.join()

    out_file = open(output_file, "w")
    out_file.write(''.join(batch_string))
    out_file.flush()
