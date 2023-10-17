import time
from app import app

app.testing = True
test_event_response = [
        1,
        'test event',
        'test-event',
        1,
        1,
        1,
        1,
        '2023-01-01 12:00',
        '2023-01-10 12:00'
    ]


def test_fetch_events():
    response = app.test_client().get('/event/')
    events = response.json
    assert response.status_code == 200
    assert events[0] == test_event_response
    assert len(events) > 1


def test_fetch_filtered_events():
    params = {"filters": [
        {"label": "name", "value": "test event", "type": "LIKE"},
        {"label": "id", "value": 1, "type": "="}
    ]}
    response = app.test_client().get('/event', query_string=params)
    assert response.status_code == 200
    assert response.json == [test_event_response]
    assert len(response.json) == 1


def test_fetch_filtered_events_find_none():
    params = {"filters": [{"label": "id", "value": 99999999, "type": "="}]}
    response = app.test_client().get('/event', query_string=params)
    assert response.status_code == 200
    assert response.json == []


def test_fetch_filtered_events_no_filters():
    params = {"filters": []}
    response = app.test_client().get('/event', query_string=params)
    events = response.json
    assert response.status_code == 200
    assert events[0] == test_event_response
    assert len(events) > 1


def test_fetch_filtered_events_fails_bad_param():
    params = {"wrong_name": "test"}
    response = app.test_client().get('/event', query_string=params)
    assert response.status_code == 500


def test_fetch_single_event():
    response = app.test_client().get('/event/1')
    assert response.status_code == 200
    assert response.json == [test_event_response]
    assert len(response.json) == 1


def test_fetch_single_event_id_mismatch():
    response = app.test_client().get('/event/9999999')
    assert response.status_code == 200
    assert response.json == []


def test_fetch_single_event_id_wrong_type():
    response = app.test_client().get('/event/test')
    assert response.status_code == 500


def test_create_events():
    test_value = {
        "name": "test event {0}".format(time.time()),
        "active": 1,
        "type": 1,
        "sport": 1,
        "status": 1,
        "scheduled_start": "2023-01-01 12:00",
        "started_at": "2023-01-10 12:00"
    }
    response = app.test_client().post('/event/', json={"values": [test_value]})
    assert response.status_code == 200
    params = {"filters": [
        {"label": "name", "value": test_value['name'], "type": "LIKE"}
    ]}
    response = app.test_client().get("/event", query_string=params)
    filtered_event = response.json[0]
    assert filtered_event[1] == test_value['name']


def test_create_events_fails():
    test_value = {"active": 1}
    response = app.test_client().post('/event/', json={"values": [test_value]})
    assert response.status_code == 500


def test_update_events():
    test_values = {"name": "'test event {0}'".format(time.time())}
    test_filters = ["id = 2"]
    response = app.test_client().put('/event/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 200
    return_event = response.json[0]
    assert return_event[0] == 2
    assert "'{0}'".format(return_event[1]) == '{0}'.format(test_values['name'])


def test_update_events_empty_filters():
    test_values = {"name": "'test event {0}'".format(time.time())}
    test_filters = []
    response = app.test_client().put('/event/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 400


def test_update_events_no_filters():
    test_values = {"name": "'test event {0}'".format(time.time())}
    response = app.test_client().put('/event/', json={"values": test_values})
    assert response.status_code == 500


def test_update_events_empty_values():
    test_values = {}
    test_filters = ["id = 2"]
    response = app.test_client().put('/event/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 400


def test_update_events_no_values():
    test_filters = ["id = 2"]
    response = app.test_client().put('/event/', json={"filters": test_filters})
    assert response.status_code == 500


def test_update_single_event():
    test_values = {"name": "'test event {0}'".format(time.time())}
    response = app.test_client().put('/event/2', json={"values": test_values})
    assert response.status_code == 200
    return_event = response.json[0]
    assert return_event[0] == 2
    assert "'{0}'".format(return_event[1]) == '{0}'.format(test_values['name'])


def test_update_single_event_no_values():
    response = app.test_client().put('/event/2', json={})
    assert response.status_code == 500


def test_update_single_event_empty_values():
    response = app.test_client().put('/event/2', json={"values": {}})
    assert response.status_code == 400


def test_update_single_event_no_json():
    response = app.test_client().put('/event/2')
    assert response.status_code == 500


def test_update_single_event_parent_inactive():
    test_values = {"active": 0}
    response = app.test_client().put('/event/3', json={"values": test_values})
    assert response.status_code == 200
    response = app.test_client().get("/sport/2")
    parent_event = response.json[0]
    assert parent_event[3] == 0


def test_update_single_event_parent_active():
    test_values = {"active": 1}
    response = app.test_client().put('/event/3', json={"values": test_values})
    assert response.status_code == 200
    response = app.test_client().get("/sport/2")
    parent_event = response.json[0]
    assert parent_event[3] == 1


def test_update_event_parent_inactive():
    test_values = {"active": 0}
    test_filters = ["id = 3"]
    response = app.test_client().put('/event/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 200
    response = app.test_client().get("/sport/2")
    parent_event = response.json[0]
    assert parent_event[3] == 0


def test_update_event_parent_active():
    test_values = {"active": 1}
    test_filters = ["id = 3"]
    response = app.test_client().put('/event/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 200
    response = app.test_client().get("/sport/2")
    parent_event = response.json[0]
    assert parent_event[3] == 1
