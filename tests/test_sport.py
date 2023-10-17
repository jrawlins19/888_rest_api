import time
from app import app

app.testing = True
test_sport_response = [1, 'test sport', 'test-sport', 1]


def test_fetch_sports():
    response = app.test_client().get('/sport/')
    sports = response.json
    assert response.status_code == 200
    assert sports[0] == test_sport_response
    assert len(sports) > 1


def test_fetch_filtered_sports():
    params = {"filters": [
        {"label": "name", "value": "test sport", "type": "LIKE"},
        {"label": "id", "value": 1, "type": "="}
    ]}
    response = app.test_client().get('/sport', query_string=params)
    assert response.status_code == 200
    assert response.json == [test_sport_response]
    assert len(response.json) == 1


def test_fetch_filtered_sports_find_none():
    params = {"filters": [{"label": "id", "value": 99999999, "type": "="}]}
    response = app.test_client().get('/sport', query_string=params)
    assert response.status_code == 200
    assert response.json == []


def test_fetch_filtered_sports_no_filters():
    params = {"filters": []}
    response = app.test_client().get('/sport', query_string=params)
    sports = response.json
    assert response.status_code == 200
    assert sports[0] == test_sport_response
    assert len(sports) > 1


def test_fetch_filtered_sports_fails_bad_param():
    params = {"wrong_name": "test"}
    response = app.test_client().get('/sport', query_string=params)
    assert response.status_code == 500


def test_fetch_single_sport():
    response = app.test_client().get('/sport/1')
    assert response.status_code == 200
    assert response.json == [test_sport_response]
    assert len(response.json) == 1


def test_fetch_single_sport_id_mismatch():
    response = app.test_client().get('/sport/9999999')
    assert response.status_code == 200
    assert response.json == []


def test_fetch_single_sport_id_wrong_type():
    response = app.test_client().get('/sport/test')
    assert response.status_code == 500


def test_create_sports():
    test_value = {"name": "test sport {0}".format(time.time()), "active": 1}
    response = app.test_client().post('/sport/', json={"values": [test_value]})
    assert response.status_code == 200
    params = {"filters": [
        {"label": "name", "value": test_value['name'], "type": "LIKE"}
    ]}
    response = app.test_client().get("/sport", query_string=params)
    filtered_sport = response.json[0]
    assert filtered_sport[1] == test_value['name']


def test_create_sports_fails():
    test_value = {"active": 1}
    response = app.test_client().post('/sport/', json={"values": [test_value]})
    assert response.status_code == 500


def test_update_sports():
    test_values = {"name": "'test sport {0}'".format(time.time())}
    test_filters = ["id = 2"]
    response = app.test_client().put('/sport/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 200
    return_sport = response.json[0]
    assert return_sport[0] == 2
    assert "'{0}'".format(return_sport[1]) == '{0}'.format(test_values['name'])


def test_update_sports_empty_filters():
    test_values = {"name": "'test sport {0}'".format(time.time())}
    test_filters = []
    response = app.test_client().put('/sport/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 400


def test_update_sports_no_filters():
    test_values = {"name": "'test sport {0}'".format(time.time())}
    response = app.test_client().put('/sport/', json={"values": test_values})
    assert response.status_code == 500


def test_update_sports_empty_values():
    test_values = {}
    test_filters = ["id = 2"]
    response = app.test_client().put('/sport/', json={"values": test_values, "filters": test_filters})
    assert response.status_code == 400


def test_update_sports_no_values():
    test_filters = ["id = 2"]
    response = app.test_client().put('/sport/', json={"filters": test_filters})
    assert response.status_code == 500


def test_update_single_sport():
    test_values = {"name": "'test sport {0}'".format(time.time())}
    response = app.test_client().put('/sport/2', json={"values": test_values})
    assert response.status_code == 200
    return_sport = response.json[0]
    assert return_sport[0] == 2
    assert "'{0}'".format(return_sport[1]) == '{0}'.format(test_values['name'])


def test_update_single_sport_no_values():
    response = app.test_client().put('/sport/2', json={})
    assert response.status_code == 500


def test_update_single_sport_empty_values():
    response = app.test_client().put('/sport/2', json={"values": {}})
    assert response.status_code == 400


def test_update_single_sport_no_json():
    response = app.test_client().put('/sport/2')
    assert response.status_code == 500
