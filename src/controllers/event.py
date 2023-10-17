from flask import request
from slugify import slugify
import db
from src.app import app
from src.check_parent import check_parent_active


@app.route("/event/", methods=['GET'])
@app.route("/event", methods=['GET'])
def fetch_events():
    try:
        # get filters from query params
        query_string = request.args.to_dict(False)
        if query_string and query_string['filters'] and len(query_string['filters']) > 0:
            filters = query_string['filters']
        else:
            # if no filters in the query params, set filters to None
            filters = None
        # build the query
        query = db.build_select_query('events', filters)
        # run the query and return the items fetched from the DB
        items = db.run_query(query)
        # return items
        return items, 200
    except Exception as e:
        return "Could not get events:" + str(e), 500


@app.route("/event/", methods=['POST'])
def create_events():
    try:
        # get params from json body
        body = request.get_json()
        values = []

        # get the values to insert from the json body
        for item in body['values']:
            slug = slugify(item['name'])
            values.append((item['name'],
                           slug,
                           item['active'],
                           item['type'],
                           item['sport'],
                           item['status'],
                           item['scheduled_start'],
                           item['started_at'])
                          )

        # run the insert query
        with db.con:
            db.con.executemany("""
                INSERT INTO events ('name','slug','active','type','sport','status','scheduled_start','started_at') 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            """, values)

        return "", 200
    except Exception as e:
        return "Could not create event:" + str(e), 500


@app.route("/event/", methods=['PUT'])
def update_event():
    try:
        # get params from json body
        body = request.json
        # if missing values to update and filters to decide what rows to apply them on, fail
        if not body['values'] or len(body['values']) == 0:
            return "Missing updates object", 400
        if not body['filters'] or len(body['filters']) == 0:
            return "Missing updates object", 400

        # build the update query using the filters and values
        query = db.build_update_query('events', body['values'], body['filters'])

        # run the query, returning the updated rows
        items = db.run_query(query)

        # if we updated the active status, then we need to check whether the parent (sports) also needs to be made
        # inactive/active
        if 'active' in body['values']:
            # index 5 on the event item will be the sport id
            check_parent_active("events", "sports", "sport", items[0][5])

        return items, 200
    except Exception as e:
        return "Could not update events: " + str(e), 500


@app.route("/event/<event_id>", methods=['GET'])
def fetch_single_event(event_id: int):
    try:
        # get the event using the id provided in the url
        filters = [{'label': 'id', 'type': '=', 'value': event_id}]
        query = db.build_select_query('events', filters)
        # run the query and return the items fetched from the DB
        items = db.run_query(query)
        return items, 200
    except Exception as e:
        return "Could not get events: " + str(e), 500


@app.route("/event/<event_id>", methods=['PUT'])
def update_events(event_id: int):
    try:
        # get params from json body
        body = request.json
        # if missing values to update, fail
        if not body['values'] or len(body['values']) == 0:
            return "Missing updates object", 400

        # build the update query using the values and the event id from the url
        query = db.build_update_query('events', body['values'], ["id == {0}".format(event_id)])

        # run the query and return the items fetched from the DB
        items = db.run_query(query)

        # if we updated the active status, then we need to check whether the parent (sports) also needs to be made
        # inactive/active
        if 'active' in body['values']:
            # index 5 on the event item will be the sport id
            check_parent_active("events", "sports", "sport", items[0][5])

        return items, 200
    except Exception as e:
        return "Could not update event: " + str(e), 500
