#!/usr/bin/python3

import sys, os
import smartsheet
import pprint
import json
import dict2xml
import argparse


smart = smartsheet.Smartsheet()
smart.errors_as_exceptions(False)


def get_sheet_data(sheet_id: int):
    """
    Retrieves and groups customer data from SmartSheet platform
    :param sheet_id: int
    :return: grouped smartsheet sheet data
    """
    grp = {
        'level1': 'country',
        'level2': 'state'
    }
    result = {}

    next_page = 1
    pg_size = 50
    columns = None

    lvl1_id = lvl2_id = 0

    while True:

        raw_data = smart.Sheets.get_sheet(sheet_id, page=next_page, page_size=pg_size)

        if not columns:
            columns = load_columns(raw_data.columns)

            lvl1_id = get_column_id(raw_data.columns, grp.get('level1'))
            lvl2_id = get_column_id(raw_data.columns, grp.get('level2'))

        for row in raw_data.rows:

            row_values = {}
            lvl1 = lvl2 = ''

            for cell in row.cells:

                row_values.update({columns[cell.column_id]: cell.value})

                if cell.column_id == lvl1_id:
                    if not cell.value in result.keys():
                        result.update({cell.value: {'arrTotal': 0, 'Unique States': [], 'States': []}})

                    lvl1 = row_values[grp.get('level1')]

                elif cell.column_id == lvl2_id:
                    lvl1 = row_values[grp.get('level1')]

                    if not cell.value in result[lvl1]['Unique States']:
                        result[lvl1]['States'].append({cell.value: {'arrTotal': 0, 'customers': []}})
                        result[lvl1]['Unique States'].append(cell.value)

                    lvl2 = row_values[grp.get('level2')]

            result[lvl1]['arrTotal'] += row_values.get('arr')

            for e in result[lvl1]['States']:
                if lvl2 in e.keys():
                    e[lvl2]['arrTotal'] += row_values.get('arr')
                    e[lvl2]['customers'].append(row_values)

        if (next_page * pg_size) >= raw_data.total_row_count:
            break

        next_page = next_page + 1

    return result


def load_columns(columns_data) -> dict :
    """
    Extracts the columns from sheet data object
    :param columns_data:
    :return: serialised columns
    """
    cols = {}

    for col in columns_data:
        cols.update({col.id: col.title})

    return cols


def get_column_id(columns: dict, column_name: str) -> str:
    """
    Converts column title to column Id
    :param columns:
    :param column_name:
    :return:
    """
    for col in columns:
        if column_name == col.title:
            return col.id


def get_sheet_id(sheetname):
    """
    Get the sheet id based on a given sheet name
    :param sheetname:
    :return:
    """
    pg = 1

    while True:
        shts = smart.Sheets.list_sheets(page=pg)

        for sht in shts.data:
            if sht.name == sheetname:
                return sht.id
        if (pg * 100) >= shts.total_pages:
            break
    raise Exception('Smartsheet name not found')
    #print("ErroSmartsheet name not found")
    #sys.exit(2)


def process_output(data: dict, output_type, destination=""):
    # pprint.pprint(data, indent=5)
    # sys.exit(0)

    fullpath = os.path.join(destination, f'output.{output_type}')

    if output_type == 'json':
        with open(fullpath, 'w') as f:
            json.dump(data, f, indent=True)
    elif output_type == "xml":
        with open(fullpath, 'w') as f:
            f.write(dict2xml.dict2xml(data))
    elif output_type == "cli":
        pprint.pprint(data, indent=5)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="Output type, default is json", choices=['json', 'xml', 'cli'], default='json')
    parser.add_argument("-d", help="Output file directory", default='')
    #parser.add_argument("-g", type=int, help="number of grouping")
    parser.add_argument("-s", "--sheet-name", help="Name of the Smartsheet sheet", default='data')
    parser.add_argument("-i", help="Test Installation", action="store_true")
    args = parser.parse_args()

    if args.i:
        print('Inspection: program is correctly configured')
        sys.exit(1)

    sheet_id = get_sheet_id(args.sheet_name)

    cy = get_sheet_data(sheet_id, )

    process_output(cy, args.o, args.d)
