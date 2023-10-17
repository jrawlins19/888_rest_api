import sqlite3

con = sqlite3.connect("./db/main", check_same_thread=False)


# Builds a select query string from the table name and filters
def build_select_query(table, filters=None):
    query = "SELECT * FROM {0}".format(table)
    if filters:
        query += " WHERE"
        for item in filters:
            if type(item) == str:
                values = str_to_dict(item)
            else:
                values = item
            query += " {0} {1} {2} AND ".format(
                values['label'].replace("'", ""),
                values['type'].replace("'", ""),
                values['value']
            )
        # remove final AND
        query = query.removesuffix(' AND ')
    return query


def run_query(query):
    items = []
    with con:
        for row in con.execute(query):
            items.append(row)
    return items


# builds an update query string using the table name, values to update and filters to get which rows to update
def build_update_query(table, values, filters):
    query = "UPDATE {} SET".format(table)
    for item in values:
        query += " {0} = {1}, ".format(item, values[item])
    # remove final ,
    query = query.removesuffix(', ')
    # add filters
    query += " WHERE"
    for item in filters:
        query += " {0} AND ".format(item)
    # remove final AND
    query = query.removesuffix(' AND ')
    # finally add RETURNING so we can get the row back
    query += " RETURNING *"
    return query


# needed to convert the query params into a usable dict
def str_to_dict(string):
    # remove the curly braces from the string
    string = string.strip('{}')

    # split the string into key-value pairs
    pairs = string.split(', ')

    return {key[1:-1]: value for key, value in (pair.split(':') for pair in pairs)}
