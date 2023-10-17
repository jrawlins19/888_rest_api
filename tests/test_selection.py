import time
import json
from urllib.parse import urlencode
from app import app

app.testing = True
test_selection_response = [1, 'test selection', 1, 10.5, 1, 1]


def test_fetch_selections():
    response = app.test_client().get('/selection/')
    selections = response.json
    assert response.status_code == 200
    assert selections[0] == test_selection_response
    assert len(selections) > 1


def test_fetch_filtered_selections():
    params = {"filters": [
        {"label": "name", "value": "test selection", "type": "LIKE"},
        {"label": "id", "value": 1, "type": "="}
    ]}
    response = app.test_client().get('/selection', query_string=params)
    assert response.status_code == 200
    assert response.json == [test_selection_response]
    assert len(response.json) == 1


def test_fetch_filtered_selections_find_none():
    params = {"filters": [{"label": "id", "value": 99999999, "type": "="}]}
    response = app.test_client().get('/selection', query_string=params)
    assert response.status_code == 200
    assert response.json == []


def test_fetch_filtered_selections_no_filters():
    params = {"filters": []}
    response = app.test_client().get('/selection', query_string=params)
    selections = response.json
    assert response.status_code == 200
    assert selections[0] == test_selection_response
    assert len(selections) > 1


def test_fetch_filtered_selections_fails_bad_param():
    params = {"wrong_name": "test"}
    response = app.test_client().get('/selection', query_string=params)
    assert response.status_code == 500


def test_fetch_single_selection():
    response = app.test_client().get('/selection/1')
    assert response.status_code == 200
    assert response.json == [test_selection_response]
    assert len(response.json) == 1


def test_fetch_single_selection_id_mismatch():
    response = app.test_client().get('/selection/9999999')
    assert response.status_code == 200
    assert response.json == []


def test_fetch_single_selection_id_wrong_type():
    response = app.test_client().get('/selection/test')
    assert response.status_code == 500


def test_create_selections():
    test_value = {
        "name": "test selection {0}".format(time.time()),
        "event": 1,
        "price": 10.50,
        "active": 1,
        "outcome": 1
    }
    response = app.test_client().post('/selection/', json={"values": [test_value]})
    assert response.status_code == 200
    params = {"filters": [
        {"label": "name", "value": test_value['name'], "type": "LIKE"}
    ]}
    response = app.test_client().get("/selection/", query_string=params)
    filtered_selection = response.json[0]
    assert filtered_selection[1] == test_value['name']


def test_create_selections_fails():
    test_value = {"active": 1}
    response = app.test_client().post('/selection/', json={"values": [test_value]})
    assert response.status_code == 500


def test_update_selections():
    test_values = {"name": "'test selection {0}'".format(time.time())}
    test_filters = ["id = 2"]
    response = app.test_client().put('/selection/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 200
    return_selection = response.json[0]
    assert return_selection[0] == 2
    assert "'{0}'".format(return_selection[1]) == '{0}'.format(test_values['name'])


def test_update_selections_empty_filters():
    test_values = {"name": "'test selection {0}'".format(time.time())}
    test_filters = []
    response = app.test_client().put('/selection/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 400


def test_update_selections_no_filters():
    test_values = {"name": "'test selection {0}'".format(time.time())}
    response = app.test_client().put('/selection/', json={"values": test_values})
    assert response.status_code == 500


def test_update_selections_empty_values():
    test_values = {}
    test_filters = ["id = 2"]
    response = app.test_client().put('/selection/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 400


def test_update_selections_no_values():
    test_filters = ["id = 2"]
    response = app.test_client().put('/selection/', json={"filters": test_filters})
    assert response.status_code == 500


def test_update_single_selection():
    test_values = {"name": "'test selection {0}'".format(time.time())}
    response = app.test_client().put('/selection/2', json={"values": test_values})
    assert response.status_code == 200
    return_selection = response.json[0]
    assert return_selection[0] == 2
    assert "'{0}'".format(return_selection[1]) == '{0}'.format(test_values['name'])


def test_update_single_selection_no_values():
    response = app.test_client().put('/selection/2', json={})
    assert response.status_code == 500


def test_update_single_selection_empty_values():
    response = app.test_client().put('/selection/2', json={"values": {}})
    assert response.status_code == 400


def test_update_single_selection_no_json():
    response = app.test_client().put('/selection/2')
    assert response.status_code == 500


def test_update_single_selection_parent_inactive():
    test_values = {"active": 0}
    response = app.test_client().put('/selection/3', json={"values": test_values})
    assert response.status_code == 200
    response = app.test_client().get("/event/3")
    parent_event = response.json[0]
    assert parent_event[3] == 0


def test_update_single_selection_parent_active():
    test_values = {"active": 1}
    response = app.test_client().put('/selection/3', json={"values": test_values})
    assert response.status_code == 200
    response = app.test_client().get("/event/3")
    parent_event = response.json[0]
    assert parent_event[3] == 1


def test_update_selection_parent_inactive():
    test_values = {"active": 0}
    test_filters = ["id = 3"]
    response = app.test_client().put('/selection/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 200
    response = app.test_client().get("/event/3")
    parent_event = response.json[0]
    assert parent_event[3] == 0


def test_update_selection_parent_active():
    test_values = {"active": 1}
    test_filters = ["id = 3"]
    response = app.test_client().put('/selection/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 200
    response = app.test_client().get("/event/3")
    parent_event = response.json[0]
    assert parent_event[3] == 1
