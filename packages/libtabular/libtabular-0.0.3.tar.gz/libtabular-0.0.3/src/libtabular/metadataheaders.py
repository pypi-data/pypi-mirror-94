
def parse_metadata_header(table):
    """
    Given a PETL table-like object (an iterable of iterables) opened from any
    source with header=None, parse the rows to identify:
     - `metadatata` (dict): contents of header rows where each metadata row is
       interpreted as: key = first_column.rstrip(":"), value = second_column.
     - `header` list(str): the contents of the "column headers" row, which
       separates metadata rows from data rows.
     - `data` list(list(str)): the rest of the rows after the header
    """
    rows = list(table)
    assert rows, "unexpected empty table given"

    data_width = len(rows[0])
    for row in rows:
        if len(row) != data_width:
            raise ValueError("Unexpected 'ragged' rows table encountered")

    # convert to radded-rows (truncate row to end of non-empty values)
    succinct_rows = []
    for row in rows:
        succinct_row = []
        for colidx in range(0,len(row)):
            if all(col.strip() == "" for col in row[colidx:]):
                succinct_row = row[0:colidx]
                break
        if not succinct_row:
            succinct_row = row
        succinct_rows.append(succinct_row)

    assert len(succinct_rows[-1]) == data_width, "Unexpected width of last row"

    # go through `rows` to parse metadata, header, and data rows:
    metadata = {}
    header = None
    data = []
    for succinct_row in succinct_rows:
        if len(succinct_row) < data_width:
            key = succinct_row[0].lstrip('# ').strip(':')
            value = succinct_row[1].strip()
            metadata[key] = value
        else:
            if header is None:
                header = succinct_row  # found the header!
            else:
                data.append(succinct_row)

    return (metadata, header, data)
