from bs4 import BeautifulSoup as bs

__author__ = 'oswaldjones'


# functions that take html to find and process tables --------------

def extract_tables(html):

    html_tables = []

    soup = bs(clean_html(html), 'lxml') # Adding 'lxml' parameter
    html_tables = soup.find_all('table')

    return html_tables


def clean_html(html):

    return html.replace('\n', '')


def normalize(text):
    
    return text.lower().strip()


# higher level table functions -------------------------------------

def filter_by_headings(tables, must_match):

    found_tables = []

    for table in tables:
        found_headings = [normalize(heading) for heading in find_headings(table)]
        if must_match.issubset(set(found_headings)):
            found_tables.append(table)

    return found_tables


def valid_table(table, must_match):

    if not table or not must_match:
        return False

    found_headings = [normalize(found) for found in find_headings(table)]

    return must_match.issubset(found_headings)


def valid_twod(twod, must_match):

    if not twod or not must_match:
        return False

    found_headings = []

    for found in twod[0]:
        if type(found) is str or type(found) is unicode:
            found_headings.append(normalize(found))
        else:
            # this else is a hack for when there is a soup object instead of text
            found_headings.append(normalize(found.text))

    return must_match.issubset(found_headings)


# low level table functions -----------------------------------------

def find_headings(table):

    heading_cells = find_cells(find_rows(table)[0])

    return [heading.text for heading in heading_cells]


def find_rows(table):

    return table.find_all('tr')


def max_rows(table):

    return len(find_rows(table))


def max_cols(table):

    col_lenths = []

    for row in find_rows(table):
        col_lenths.append(len(find_cells(row)))

    return max(col_lenths)


def col_index(table, possible_headings):

    cdx = None

    possible_headings = possible_headings if type(possible_headings) == list else [possible_headings]

    found_headings = find_headings(table)
    for idx, found in enumerate([normalize(f) for f in found_headings]):
        for possible in possible_headings:
            if found == possible:
                cdx = idx

    return cdx


def col_idx(twod, possible_headings):

    cdx = None

    possible_headings = possible_headings if type(possible_headings) == list else [possible_headings]

    found_headings = []

    for cell in twod[0]:
        if type(cell) is str or type(cell):
            found_headings.append(cell)
        else:
            # this is a hack for when cell is soup object instead of text
            found_headings.append(cell.text)

    for idx, found in enumerate([f.lower().strip() for f in found_headings]):
        for possible in possible_headings:
            if found == possible.lower().strip():
                cdx = idx
                break

    return cdx


# column functions --------------------------------------------------


def col_to_list(twod, col_idx):

    col = []

    for rdx, row in enumerate(twod):
        for cdx, cell in enumerate(row):
            if cdx == col_idx:
                col.append(cell)

    return col


def column_data(table, possible_headings):

    twod = make2d(table)

    column = col_to_list(twod, col_idx(twod, possible_headings))

    return remove_headings(column, possible_headings)


def twod_col_data(twod, possible_headings):

    column = col_to_list(twod, col_idx(twod, possible_headings))

    return remove_headings(column, possible_headings)


def remove_headings(col_list, possible_headings):

    pop_count = 0
    possible_headings = possible_headings if type(possible_headings) == list else [possible_headings]

    for cdx, val in enumerate(col_list):
        # this ternary is hack for when val is soup object instead of text
        val = val if type(val) is str or type(val) is unicode else val.text
        if val.lower().strip() in [heading.lower().strip() for heading in possible_headings]:
            pop_count += 1
        else:
            break

    return col_list[pop_count:]


# row functions -----------------------------------------------------

def find_cell_in_row(row, col_idx):

    cell = None

    if not row or col_idx is None:
        return  cell

    if len(find_cells(row)) and abs(col_idx) < len(find_cells(row)):
        cell = find_cells(row)[col_idx]

    return cell


def find_cells(row):

    cells = []

    ths = row.find_all('th', recursive=False)
    if ths:
        cells.extend(ths)
    tds = row.find_all('td', recursive=False)
    if tds:
        cells.extend(tds)

    return cells


def first_col_cell(row):

    return row.find('th') if row.find('th') else row.find('td')


def has_row_heading(row):

    return True if row.find('th') else False


# these convert html into 2d list -----------------------------------

def make2d(table, text_only=True):

    twod = []

    for rdx, row in enumerate(find_rows(table)):
        twod.append([])
        for cell in find_cells(row):
            twod[rdx].append(cell)

    twod = insert_colspans(twod)
    twod = insert_rowspans(twod)

    if text_only:
        twod = textonly(twod)

    return twod


def textonly(twod):

    text2d = []

    for rdx, row in enumerate(twod):
        text2d.append([])
        for cell in row:
            text2d[rdx].append(cell.text.strip())

    return text2d


def insert_rowspans(twod):

    for rdx, row in enumerate(twod):
        for cdx, cell in enumerate(row):
            cell_rowspan = cell.get('rowspan')
            if cell_rowspan and cell_rowspan.isdigit() and not cell.get('row_done'):
                cell['row_done'] = True
                for x in range(1, int(cell_rowspan)):
                    if rdx + x < len(twod):
                        twod[rdx + x].insert(cdx, cell)

    # flip done attributes back because state is saved on following iterations
    for rdx, row in enumerate(twod):
        for cdx, cell in enumerate(row):
            if cell.get('row_done'):
                cell['row_done'] = False

    return twod


def insert_colspans(twod):

    for rdx, row in enumerate(twod):
        for cdx, cell in enumerate(row):
            cell_colspan = cell.get('colspan')
            if cell_colspan and cell_colspan.isdigit() and not cell.get('col_done'):
                cell['col_done'] = True
                for x in range(1, int(cell_colspan)):
                    if rdx == 0:
                        twod[rdx].insert(cdx, cell)
                    else:
                        if len(twod[rdx]) < len(twod[rdx - 1]):
                            twod[rdx].insert(cdx, cell)

    # flip done attributes back because state is saved on following iterations
    for rdx, row in enumerate(twod):
        for cdx, cell in enumerate(row):
            if cell.get('col_done'):
                cell['col_done'] = False

    return twod


# dict functions -----------------------------------------------------

def make_dict(table, rowstart):

    col_headings = find_headings(table)
    twod = make2d(table)

    events = []
    for row in twod[rowstart:]:
        headings_cells = zip(col_headings, row)
        event = dict()
        for heading, cell in headings_cells:
            event[heading] = cell
        events.append(event)

    return events







