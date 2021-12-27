from flask import Flask, g, jsonify, Response, request, render_template
from flask.views import MethodView
import os
import sqlite3
import booking_db
import requests
import sys


# Flask APP Initialization
app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'db.sqlite')
db = booking_db.BookingDB('db.sqlite')


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    conn = get_db()
    conn.commit()
    db.create_tables()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


class RequestError(Exception):
    """
    This custom exception class is for easily handling errors in requests,
    such as when the user provides an ID that does not exist or omits a
    required field.
    """

    def __init__(self, status_code, error_message):
        # Call the parent class's constructor. Unlike in C++, this does not
        # happen automatically in Python.
        Exception.__init__(self)

        self.status_code = str(status_code)
        self.error_message = error_message

    def to_response(self):
        """
        Create a Response object containing the error message as JSON.

        :return: the response
        """

        response = jsonify({'error': self.error_message})
        response.status = self.status_code
        return response


@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    """
    Returns a JSON response built from a RequestError.

    :param error: the RequestError
    :return: a resonse containing the error message
    """
    return error.to_response()


class EventView(MethodView):

    def get(self, event_id):
        if event_id is None:
            all_events = db.get_all_events()
            return jsonify(all_events)
        else:
            event = db.get_event_by_id(event_id)

            if event is not None:
                response = jsonify(event)
            else:
                raise RequestError(404, 'race not found')

            return event

    def post(self):
        """
        Handles a POST request to insert a new type of class.
        Returns a JSON response representing the new type
        of class.

        The class name must be provided in the requests's form data.

        :return: a response containing the JSON representation of
        the type of class.
        """
        if 'person_id' not in request.form:
            raise RequestError(422, 'person_id required')
        if 'activity_id' not in request.form:
            raise RequestError(422, 'activity_id required')
        if 'date' not in request.form:
            raise RequestError(422, 'date required')
        if 'amount' not in request.form:
            raise RequestError(422, 'amount required')
        else:
            response = jsonify(db.insert_event(
                request.form['person_id'],
                request.form['activity_id'],
                request.form['date'],
                request.form['amount']
            ))

        return response

    def delete(self, event_id):
        """
        Implements DELETE /class

        Requires the form parameter 'class_id'

        :return: JSON response representing the deleted class
        """

        # request.form is a dictionary of the form data contained
        # in the request
        if 'event_id' not in request.form:
            raise RequestError(422, 'event_id required')
        else:
            deleted_event = db.get_event_by_id(
                request.form['event_id'])
            db.delete_event(request.form['event_id'])
        return jsonify(deleted_event)


class ActivityView(MethodView):
    """
    This view handles all the activity requests.
    """
    def __init__(self):
        self._db = booking_db.BookingDB('db.sqlite')

    def get(self, activity_id):
        """
        Handle GET requests.

        Returns JSON representing all of the league if class_id is None,
        or one type of league if class_id is not None.

        :param class_id: id of the league, or None for all the leagues
        :return: JSON response
        """
        if activity_id is None:
            all_activities = self._db.get_all_activities()
            return jsonify(all_activities)
        else:
            activity = self._db.get_activity_by_id(activity_id)

            if activity is not None:
                response = jsonify(activity)
            else:
                raise RequestError(404, 'activity not found')

            return response

    def post(self):
        """
        Handles a POST request to insert a new type of class.
        Returns a JSON response representing the new type
        of class.

        The class name must be provided in the requests's form data.

        :return: a response containing the JSON representation of
        the type of class.
        """
        if 'name' not in request.form:
            raise RequestError(422, 'activity name required')
        else:
            response = jsonify(self._db.insert_activity(
                request.form['name']
            ))

        return response

    def delete(self):
        """
        Implements DELETE /class

        Requires the form parameter 'class_id'

        :return: JSON response representing the deleted class
        """

        # request.form is a dictionary of the form data contained
        # in the request
        if 'activity_id' not in request.form:
            raise RequestError(422, 'activity_id required')
        else:
            deleted_activity = self._db.get_activity_by_id(
                request.form['activity_id'])
            self._db.delete_activity(request.form['activity_id'])
        return jsonify(deleted_activity)


class PersonView(MethodView):
    """
    This view handles all the activity requests.
    """
    def __init__(self):
        self._db = booking_db.BookingDB('db.sqlite')

    def get(self, person_id):
        """
        Handle GET requests.

        Returns JSON representing all of the league if class_id is None,
        or one type of league if class_id is not None.

        :param class_id: id of the league, or None for all the leagues
        :return: JSON response
        """
        if person_id is None:
            all_people = self._db.get_all_people()
            return jsonify(all_people)
        else:
            person = self._db.get_person_by_id(person_id)

            if person is not None:
                response = jsonify(person)
            else:
                raise RequestError(404, 'person not found')

            return response

    def post(self):
        """
        Handles a POST request to insert a new type of class.
        Returns a JSON response representing the new type
        of class.

        The class name must be provided in the requests's form data.

        :return: a response containing the JSON representation of
        the type of class.
        """
        if 'name' not in request.form:
            raise RequestError(422, 'person name required')
        else:
            response = jsonify(self._db.insert_person(
                request.form['name']
            ))

        return response

    def delete(self):
        """
        Implements DELETE /class

        Requires the form parameter 'class_id'

        :return: JSON response representing the deleted class
        """

        # request.form is a dictionary of the form data contained
        # in the request
        if 'person_id' not in request.form:
            raise RequestError(422, 'person_id required')
        else:
            deleted_person = self._db.get_person_by_id(
                request.form['person_id'])
            self._db.delete_person(request.form['person_id'])
        return jsonify(deleted_person)


# Register LeagueView as the handler for all the /event/ requests.
event_view = EventView.as_view('event_view')
app.add_url_rule('/api/event/', defaults={'event_id': None},
                 view_func=event_view, methods=['GET'])
app.add_url_rule('/api/event/', view_func=event_view, methods=['POST'])
app.add_url_rule('/api/event/<int:event_id>/', view_func=event_view,
                 methods=['GET'])
app.add_url_rule('/api/event/', view_func=event_view,
                 methods=['DELETE'])

# Register LeagueView as the handler for all the /activity/ requests.
activity_view = ActivityView.as_view('activity_view')
app.add_url_rule('/api/activity/', defaults={'activity_id': None},
                 view_func=activity_view, methods=['GET'])
app.add_url_rule('/api/activity/', view_func=activity_view, methods=['POST'])
app.add_url_rule('/api/activity/<int:activity_id>', view_func=activity_view,
                 methods=['GET'])
app.add_url_rule('/api/activity/', view_func=activity_view,
                 methods=['DELETE'])

# Register LeagueView as the handler for all the /person/ requests.
person_view = PersonView.as_view('person_view')
app.add_url_rule('/api/person/', defaults={'person_id': None},
                 view_func=person_view, methods=['GET'])
app.add_url_rule('/api/person/', view_func=person_view, methods=['POST'])
app.add_url_rule('/api/person/<int:person_id>', view_func=person_view,
                 methods=['GET'])
app.add_url_rule('/api/person/', view_func=person_view,
                 methods=['DELETE'])


@app.route('/')
def home():
    """
    Serves a main page.
    """

    return render_template('home.html')


@app.route('/event')
def event():
    """
    Serves a main page.
    """

    print(booking_db.BookingDB('db.sqlite').overview())

    return render_template(
        'event.html', events=db.overview())


@app.route('/activity')
def activity():
    """
    Serves an activity page.
    """

    return render_template(
        'activity.html',
        activities=booking_db.BookingDB('db.sqlite').get_all_activities())


@app.route('/person')
def person_and_payment():
    """
    Serves a person_and_payment page.
    """

    return render_template(
        'person.html',
        people=booking_db.BookingDB('db.sqlite').get_all_people())
