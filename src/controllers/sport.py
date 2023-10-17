from flask import request
from slugify import slugify
from src.db import *
from src.app import app


@app.route("/sport/", methods=['GET'])
@app.route("/sport", methods=['GET'])
def fetch_sports():
    try:
        # get filters from query params
        query_string = request.args.to_dict(False)
        if query_string and query_string['filters'] and len(query_string['filters']) > 0:
            filters = query_string['filters']
        else:
            # if no filters in the query params, set filters to None
            filters = None
        # build the query
        query = build_select_query('sports', filters)
        # run the query and return the items fetched from the DB
        items = run_query(query)
        # return items
        return items, 200
    except Exception as e:
        return "Could not get sports:" + str(e), 500


@app.route("/sport/", methods=['POST'])
def create_sports():
    try:
        # get params from json body
        body = request.get_json()
        values = []

        # get the values to insert from the json body
        for item in body['values']:
            slug = slugify(item['name'])
            values.append((item['name'], slug, item['active']))

        # run the insert query
        with con:
            con.executemany("INSERT INTO sports ('name', 'slug', 'active') VALUES(?, ?, ?)", values)

        return "", 200
    except Exception as e:
        return "Could not create sport:" + str(e), 500


@app.route("/sport/", methods=['PUT'])
def update_sport():
    try:
        # get params from json body
        body = request.json
        # if missing values to update and filters to decide what rows to apply them on, fail
        if not body['values'] or len(body['values']) == 0:
            return "Missing updates object", 400
        if not body['filters'] or len(body['filters']) == 0:
            return "Missing updates object", 400

        # build the update query using the filters and values
        query = build_update_query('sports', body['values'], body['filters'])

        # run the query, returning the updated rows
        items = run_query(query)

        return items, 200
    except Exception as e:
        return "Could not update sports: " + str(e), 500


@app.route("/sport/<sport_id>", methods=['GET'])
def fetch_single_sport(sport_id: int):
    try:
        # get the event using the id provided in the url
        filters = [{'label': 'id', 'type': '=', 'value': sport_id}]
        query = build_select_query('sports', filters)
        # run the query and return the items fetched from the DB
        items = run_query(query)
        return items, 200
    except Exception as e:
        return "Could not get sports: " + str(e), 500


@app.route("/sport/<sport_id>", methods=['PUT'])
def update_sports(sport_id: int):
    try:
        # get params from json body
        body = request.json
        # if missing values to update, fail
        if not body['values'] or len(body['values']) == 0:
            return "Missing updates object", 400

        # build the update query using the values and the event id from the url
        query = build_update_query('sports', body['values'], ["id == {0}".format(sport_id)])

        # run the query and return the items fetched from the DB
        items = run_query(query)

        return items, 200
    except Exception as e:
        return "Could not update sport: " + str(e), 500
