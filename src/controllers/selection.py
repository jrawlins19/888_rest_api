from flask import request
from src.db import *
from src.app import app
from src.check_parent import check_parent_active


@app.route("/selection/", methods=['GET'])
@app.route("/selection", methods=['GET'])
def fetch_all_selections():
    try:
        # get filters from query params
        query_string = request.args.to_dict(False)
        if query_string and query_string['filters'] and len(query_string['filters']) > 0:
            filters = query_string['filters']
        else:
            # if no filters in the query params, set filters to None
            filters = None
        # build the query
        query = build_select_query('selections', filters)
        # run the query and return the items fetched from the DB
        items = run_query(query)
        # return items
        return items, 200
    except Exception as e:
        return "Could not get selections:" + str(e), 500


@app.route("/selection/", methods=['POST'])
def create_selections():
    try:
        # get params from json body
        body = request.get_json()
        values = []

        # get the values to insert from the json body
        for item in body['values']:
            values.append((item['name'], item['event'], item['price'], item['active'], item['outcome']))

        # run the insert query
        with con:
            con.executemany("""
                INSERT INTO selections ('name', 'event', 'price', 'active', 'outcome') VALUES(?, ?, ?, ?, ?)
            """, values)

        return "", 200
    except Exception as e:
        return "Could not create selection:" + str(e), 500


@app.route("/selection/", methods=['PUT'])
def update_selection():
    try:
        # get params from json body
        body = request.json
        # if missing values to update and filters to decide what rows to apply them on, fail
        if not body['values'] or len(body['values']) == 0:
            return "Missing updates object", 400
        if not body['filters'] or len(body['filters']) == 0:
            return "Missing updates object", 400

        # build the update query using the filters and values
        query = build_update_query('selections', body['values'], body['filters'])

        # run the query, returning the updated rows
        items = run_query(query)

        # if we updated the active status, then we need to check whether the parent (sports) also needs to be made
        # inactive/active
        if 'active' in body['values']:
            # index 2 on the selection item will be the event id
            check_parent_active("selections", "events", "event", items[0][2])

        return items, 200
    except Exception as e:
        return "Could not update selections: " + str(e), 500


@app.route("/selection/<selection_id>", methods=['GET'])
def fetch_single_selection(selection_id: int):
    try:
        # get the event using the id provided in the url
        filters = [{'label': 'id', 'type': '=', 'value': selection_id}]
        query = build_select_query('selections', filters)
        # run the query and return the items fetched from the DB
        items = run_query(query)
        return items, 200
    except Exception as e:
        return "Could not get selections: " + str(e), 500


@app.route("/selection/<selection_id>", methods=['PUT'])
def update_selections(selection_id: int):
    try:
        # get params from json body
        body = request.json
        # if missing values to update, fail
        if not body['values'] or len(body['values']) == 0:
            return "Missing updates object", 400

        # build the update query using the values and the event id from the url
        query = build_update_query('selections', body['values'], ["id == {0}".format(selection_id)])

        # run the query and return the items fetched from the DB
        items = run_query(query)

        # if we updated the active status, then we need to check whether the parent (sports) also needs to be made
        # inactive/active
        if 'active' in body['values']:
            # index 2 on the selection item will be the event id
            check_parent_active("selections", "events", "event", items[0][2])

        return items, 200
    except Exception as e:
        return "Could not update selection: " + str(e), 500
