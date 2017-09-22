from multiprocessing import Process, Manager
from utils import xml_utils
import logging
from optparse import OptionParser


def _get_valid_xml(file_chunks, index):
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


def _parse_console_input():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="Path to input file", metavar="FILE")
    parser.add_option("-o", "--output", dest="outputname", default="output.csv",
                      help="Path to output file", metavar="FILE")
    parser.add_option("-n", "--nchunks", dest="nchunks", default=5, type="int",
                      help="Path to output file", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help="Log in console", metavar="FILE")
    (options, _) = parser.parse_args()

    if options.filename is None:
        parser.error("Filename not given")

    if options.verbose is True:
        logging.basicConfig(level=logging.DEBUG)

    return options.filename, options.outputname, options.nchunks


def _write_csv(io, string):
    file = None
    try:
        file = open(io, "w")
        file.write("".join(string))
        file.flush()
    except IOError:
        logging.error("Output file couldn't be opened")
    finally:
        file.close()


if __name__ == "__main__":
    file_name, output_file, n_chunks = _parse_console_input()

    batch_string = Manager().list()
    logging.info("Splitting xml into %d chunks", n_chunks)

    chunks = xml_utils.split_xml(file_name, n_chunks)
    for idx in range(len(chunks)):
        logging.info("Converting chunk %d", idx)
        valid_xml = _get_valid_xml(chunks, idx)
        logging.debug("Chunk head %s", valid_xml[:1000])
        logging.debug("Chunk tail %s", valid_xml[-1000:])
        p = Process(target=xml_utils.str_xml_to_csv, args=(valid_xml, batch_string, ))
        p.start()
        p.join()
        logging.info("Chunk %d successfully converted", idx)

    _write_csv(output_file, batch_string)



