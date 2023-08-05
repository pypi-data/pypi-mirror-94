import petl

from .metadataheaders import parse_metadata_header


# CSV
################################################################################

def fromcsvwithheader(source, **kwargs):
    """
    Call `petl.fromcsv` and automatically parse metadata header if present.
    """
    # preliminary open for inspection
    rawtable = petl.fromcsv(source, header=None, **kwargs)
    metadata, header, data = parse_metadata_header(rawtable)

    # transfer data to a in-memory data buffer
    databuffer = petl.MemorySource()
    petl.tocsv(data, databuffer, write_header=True, encoding='utf-8')
    databuffer.s = databuffer.getvalue()

    # re-open with right headers and add metadata
    table = petl.fromcsv(databuffer, header=header)
    table.metadata = metadata

    return table


def tocsvwithheader(table, source, **kwargs):
    """
    Use `petl.tocsv` to write CSV data in `table` to file `source`, including
    key-value metadata header if passed in as the keyword argument `metadata`.
    The first row in `table` is assumed to contain the header columns.
    """
    metadata = kwargs.pop("metadata", {})
    kwargs.pop("write_header", None)      # make sure write_header not in kwargs

    # prepare header
    header = petl.header(table)

    # prepare metadata rows using #-prefix, and :-suffix for keys
    metadata_rows = []
    for key, value in metadata.items():
        metadata_row = [''] * len(header)
        metadata_row[0] = '#' + str(key) + ':'
        metadata_row[1] = str(value)
        metadata_rows.append(metadata_row)

    # prepare data (stripped of header)
    data = petl.data(table)

    # combine metadata + header + data the write out
    combined = metadata_rows + [header] + list(data)
    petl.tocsv(combined, source, write_header=True, **kwargs)




# XLS
################################################################################

def fromxlswithheader(filename, sheet, **kwargs):
    """
    Call `petl.fromcsv` and automatically parse metadata header if present.
    """
    # preliminary open for inspection
    rawtable = petl.fromxls(filename, sheet, header=None, **kwargs)
    metadata, header, data = parse_metadata_header(rawtable)

    # transfer data to a in-memory data buffer
    databuffer = petl.MemorySource()
    petl.tocsv(data, databuffer, write_header=True, encoding='utf-8')
    databuffer.s = databuffer.getvalue()

    # re-open with right headers and add metadata
    table = petl.fromcsv(databuffer, header=header)
    table.metadata = metadata

    return table


def toxlswithheader(table, filename, sheet, **kwargs):
    """
    Use `petl.tocsv` to write CSV data in `table` to file `source`, including
    key-value metadata header if passed in as the keyword argument `metadata`.
    The first row in `table` is assumed to contain the header columns.
    """
    metadata = kwargs.pop("metadata", {})

    # prepare header
    header = petl.header(table)

    # prepare metadata rows using #-prefix, and :-suffix for keys
    metadata_rows = []
    for key, value in metadata.items():
        metadata_row = [''] * len(header)
        metadata_row[0] = '#' + str(key) + ':'
        metadata_row[1] = str(value)
        metadata_rows.append(metadata_row)

    # prepare data (stripped of header)
    data = petl.data(table)

    # combine metadata + header + data the write out
    combined = metadata_rows + [header] + list(data)
    petl.toxls(combined, filename, sheet, **kwargs)
