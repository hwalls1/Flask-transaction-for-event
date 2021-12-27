import pytest
import tempfile
import json
import os
import main_api


@pytest.fixture
def test_client():

    db_fd, main_api.app.config['DATABASE'] = tempfile.mkstemp()

    main_api.app.testing = True

    test_client = main_api.app.test_client()

    with main_api.app.app_context():
        main_api.init_db()

    yield test_client

    os.close(db_fd)
    os.unlink(main_api.app.config['DATABASE'])


def test_no_events(test_client):
    """
    Tests the GET method of event when no events exist
    """
    response = test_client.get('/api/event/')
    assert response.status_code == 200

    response_json = json.loads(response.data)
    assert response_json == []


def test_no_persons(test_client):
    """
    Tests the GET method of person when no persons exist
    """
    response = test_client.get('/api/person/')
    assert response.status_code == 200

    response_json = json.loads(response.data)
    assert response_json == []


def test_no_activity(test_client):
    """     
    Tests the GET method of activity when no activities exist
    """
    response = test_client.get('/api/activity/')
    assert response.status_code == 200

    response_json = json.loads(response.data)
    assert response_json == []


def test_post_person(test_client):
    """
    Tests the POST method of person
    """
    person = {
        'name': 'Mrs. Smith',
    }
    response = test_client.post('/api/person/', data=person)
    assert response.status_code == 200
    response_json = json.loads(response.data)

    expected_keys = ('person_id', 'name')
    for key in expected_keys:
        assert key in response_json

    expected_values = {
        'person_id': 1,
        'name': 'Mrs. Smith',
    }

    for key, value in expected_values.items():
        assert response_json[key] == value


def test_get_persons(test_client):
    """
    Tests the GET method of person
    """
    person = {
        'name': 'Carl',
    }
    response = test_client.post('/api/person/', data=person)
    assert response.status_code == 200

    response = test_client.get('/api/person/', data=person)
    assert response.status_code == 200
    response_json = json.loads(response.data)

    expected_values = {
        'person_id': 1,
        'name': 'Carl',
    }
    expected_values_array = [expected_values]

    assert response_json == expected_values_array


def test_post_activity(test_client):
    """
    Tests the POST method of activity
    """
    activity = {
        'name': 'Birthday'
    }

    response = test_client.post('/api/activity/', data=activity)
    assert response.status_code == 200
    response_json = json.loads(response.data)

    expected_keys = ('activity_id', 'name')
    for key in expected_keys:
        assert key in response_json

    expected_values = {
        'name': 'Birthday'
    }

    for key, value in expected_values.items():
        assert response_json[key] == value


def test_get_activity(test_client):
    """
    Tests the GET method of activity
    """
    activity = {
        'name': 'Wedding'
    }

    response = test_client.get('/api/activity/', data=activity)
    assert response.status_code == 200
    response_json = json.loads(response.data)

    expected_keys = ('activity_id', 'name')
    for key in expected_keys:
        assert key in response_json

    expected_values = {
        'name': 'Wedding'
    }

    for key, value in expected_values.items():
        assert response_json[key] == value


def test_new_event(test_client):
    """
    Tests the POST method of event
    """
    person = 'Carl'
    activity = 'Birthday'
    event = {
        'person': 'Carl',
        'activity': 'Birthday',
        'date': 'Aug-14-2004',
        'amount': 400.00,
    }

    response = test_client.post('/api/person/', data=person)
    assert response.status_code == 200

    response = test_client.post('/api/activity/', data=activity)
    assert response.status_code == 200

    response = test_client.post('/api/event/', data=event)
    assert response.status_code == 200
    response_json = json.loads(response.data)

    expected_keys = ('event_id', 'person', 'activity', 'date', 'amount')
    for key in expected_keys:
        assert key in response_json

    expected_values = {
        'event_id': 1,
        'person': 'Carl',
        'activity': 'Birthday',
        'date': 'Aug-14-2004',
        'amount': 400.00,
    }

    for key, value in expected_values.items():
        assert response_json[key] == value


def test_delete_event(test_client):
    """
    Tests the DELETE method of event
    """
    person = 'Mrs. Smith'
    activity = 'Wedding'
    event = {
        'person': 'Mrs. Smith',
        'activity': 'Wedding',
        'date': 'Jan-24-1999',
        'amount': 1600.00,
    }

    response = test_client.post('/api/person/', data=person)
    assert response.status_code == 200

    response = test_client.post('/api/activity/', data=activity)
    assert response.status_code == 200

    response = test_client.post('/api/event/', data=event)
    assert response.status_code == 200

    response = test_client.delete('/api/event/1/')
    assert response.status_code == 200
    response_json = json.loads(response.data)

    expected_keys = ('event_id', 'person', 'activity', 'date', 'amount')
    for key in expected_keys:
        assert key in response_json

    expected_values = {
        'event_id': 1,
        'person': 'Mrs. Smith',
        'activity': 'Wedding',
        'date': 'Jan-24-1999',
        'amount': 1600.00,
    }

    for key, value in expected_values.items():
        assert response_json[key] == value


def test_update_event(test_client):
    """
    Tests the PUT method of event
    """
    person = 'Carl'
    activity = 'Birthday'
    event = {
        'person': 'Carl',
        'activity': 'Birthday',
        'date': 'May-24-2019',
        'amount': 400.00,
    }
    response = test_client.post('/api/person/', data=person)
    assert response.status_code == 200

    response = test_client.post('/api/activity/', data=activity)
    assert response.status_code == 200

    response = test_client.post('/api/event/', data=event)
    assert response.status_code == 200

    new_event = {
        'person': 'Carl',
        'activity': 'Birthday',
        'date': 'May-24-2009',
        'amount': 400.00,
    }

    response = test_client.put('/api/event/1/', data=new_event)
    assert response.status_code == 200
    response_json = json.loads(response.data)

    expected_keys = ('event_id', 'person', 'activity', 'date', 'amount')
    for key in expected_keys:
        assert key in response_json

    expected_values = {
        'event_id': 1,
        'person': 'Carl',
        'activity': 'Birthday',
        'date': 'May-24-2009',
        'amount': 400.00,
    }

    for key, value in expected_values.items():
        assert response_json[key] == value


def test_get_one_event(test_client):
    """
    Tests the GET method of event by event_id
    """
    person = 'Mrs. Smith'
    activtiy = 'Wedding'
    event = {
        'person': 'Mrs. Smith',
        'activity': 'Wedding',
        'date': 'Nov-1-2007',
        'amount': 1600.00,
    }
    response = test_client.post('/api/person/', data=person)
    assert response.status_code == 200

    response = test_client.post('/api/activity/', data=activity)
    assert response.status_code == 200

    response = test_client.post('/api/event/', data=event)
    assert response.status_code == 200

    response = test_client.get('/api/event/1/')
    assert response.status_code == 200
    response_json = json.loads(response.data)

    expected_keys = ('date', 'person', 'activity', 'date', 'amount')
    for key in expected_keys:
        assert key in response_json

    expected_values = {
        'event_id': 1,
        'person': 'Mrs. Smith',
        'activity': 'Wedding',
        'date': 'Nov-1-2007',
        'amount': 1600.00,
        }

    for key, value in expected_values.items():
        assert response_json[key] == value


def test_same_day_error(test_client):
    """
    Tests the client receives an error when an user tries to post an event on a
    day that already has an event
    """
    person = 'Carl'
    activity = 'Birthday'
    event = {
        'person': 'Carl',
        'activity': 'Birthday',
        'date': 'Aug-14-2004',
        'amount': 400.00,
        }
    response = test_client.post('/api/person/', data=person)
    assert response.status_code == 200

    response = test_client.post('/api/activity/', data=activity)
    assert response.status_code == 200

    response = test_client.post('/api/event/', data=event)
    assert response.status_code == 200

    person = 'Mrs. Smith'
    activity = 'Wedding'
    event = {
        'person': 'Mrs. Smith',
        'activity': 'Wedding',
        'amount': 1600.00,
        'date': 'Aug-14-2004',
        }
    response = test_client.post('/api/person/', data=person)
    assert response.status_code == 200

    response = test_client.post('/api/activity/', data=activity)
    assert response.status_code == 200

    response = test_client.post('/api/event/', data=event)
    assert response.status_code == 409
