import smartsheet
import pprint
import json

# t0un2qneccxnvi5l8t5h6vybj5

smart = smartsheet.Smartsheet('t0un2qneccxnvi5l8t5h6vybj5')
smart.errors_as_exceptions(True)


def get_sheet_data(sheet_id, grp):
    result = {}

    next_page = 1
    pg_size = 50
    sheet_total = 0
    current_version = 0

    columns = None

    while True:

        raw_data = smart.Sheets.get_sheet(sheet_id, page=next_page, page_size=pg_size)

        sheet_total = raw_data.total_row_count

        if not columns:
            columns = load_columns(raw_data.columns)

        lvl1_id = get_column_id(raw_data.columns, grp.get('level1'))
        lvl2_id = get_column_id(raw_data.columns, grp.get('level2'))

        # get uniques

        # todo Get columns
        for row in raw_data.rows:
            curr_grp1 = ''
            row_arr = 0

            row_values = {}
            lvl1 = lvl2 = ''

            for cell in row.cells:

                row_values.update({columns[cell.column_id]: cell.value})

                lvl1 = row_values[grp.get('level1')]
                lvl2 = row_values[grp.get('level2')]

                if cell.column_id == lvl1_id:
                    if not cell.value in result.keys():
                        result.update({cell.value: {'arrTotal': 0, 'uniqstates': [], 'States': []}})

                elif cell.column_id == lvl2_id:


                    if not cell.value in result[lvl1]['uniqstates']:
                        result[lvl1]['States'].append({cell.value: {'arrTotal': 0, 'customers': []}})
                        result[lvl1]['uniqstates'].append(cell.value)



            result[lvl1]['arrTotal'] += row_values.get('arr')

            for e in result[lvl1]['States']:
                if lvl2 in e.keys():
                    e[lvl2]['arrTotal'] += row_values.get('arr')
                    e[lvl2]['customers'].append(row_values)

            pass

        if (next_page * pg_size) >= sheet_total:
            break

        next_page += 1

        break  # loop for more records

    return result


def load_columns(columns_data):
    cols = {}

    for col in columns_data:
        cols.update({col.id: col.title})

    return cols


# # function to return key for any value
# def get_key(val):
#     for key, value in my_dict.items():
#         if val == value:
#             return key

# return "key doesn't exist"

def get_column_id(columns, column_name):
    for col in columns:
        if column_name == col.title:
            return col.id


def get_column_name(columns, column_id):
    for col in columns:
        if col.id == column_id:
            return col.title


# result = smart.Sheets.list_sheets()

# for s in result.data:
#     print(s))
# print(result)
# #pprint.pprint(json.loads(result.data))


# reslt = smart.Sheets.get_sheet(583973299611524, page_size=50, page=2, include=['filterDefinitions'],
#                                if_version_after=4, exclude=['userSettings'])  # , filter_id=[7404526140450692])
# # , row_ids=[6882842618947460])
# print(reslt)
# for r in reslt.rows:
#     print(r)
#
# for c in reslt.columns:
#     print(c)
#
# print(reslt)
# print(reslt.total_row_count)
# print(get_column_id(reslt.columns, 'zipcode'))
# print(len(reslt.rows))


if __name__ == '__main__':
    cy = get_sheet_data(583973299611524, grp={
        'level1': 'country',
        'level2': 'state'
    })
    pprint.pprint(cy, indent=4)