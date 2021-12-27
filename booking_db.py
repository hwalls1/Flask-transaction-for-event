import os
import sqlite3
from collections import OrderedDict


class BookingDB:
    """
    Provides an interface for interacting with the database
    """
    def __init__(self, filename):
        """
        Initializes the database. Creates the tables if the file doesn't exist
        :param filename: name of the file
        """
        self._conn = sqlite3.connect(filename)
        self._conn.row_factory = sqlite3.Row
        print('BookingDB is called.')

    def create_tables(self):
        """
        Creates all of the tables in the database
        """

        cur = self._conn.cursor()

        cur.execute('DROP TABLE IF EXISTS person')
        cur.execute('DROP TABLE IF EXISTS activity')
        cur.execute('DROP TABLE IF EXISTS event')
        cur.execute('CREATE TABLE person(person_id INTEGER PRIMARY KEY, name '
                    'TEXT)')
        cur.execute('CREATE TABLE activity(activity_id INTEGER PRIMARY KEY, '
                    'name TEXT)')
        cur.execute('CREATE TABLE event(event_id INTEGER PRIMARY KEY, '
                    'person_id INTEGER, activity_id INTEGER, date TEXT, '
                    'amount FLOAT, '
                    'FOREIGN KEY (person_id) REFERENCES person(person_id), '
                    'FOREIGN KEY (activity_id) REFERENCES '
                    'activity(activity_id))')
        self._conn.commit()
        print('Schema is called.')

    def overview(self):
        """
         Returns a list of overviews
         :return: list of pverviews
         """
        cur = self._conn.cursor()
        query = '''
            SELECT event.event_id as id, person.name as person, 
            activity.name as activity, event.date as date, 
            event.amount as amount FROM event, activity, person
            WHERE event.person_id = person.person_id
            AND event.activity_id = activity.activity_id; 
        '''
        cur.execute(query)
        results = []
        for row in cur.fetchall():
            results.append(dict(row))

        return results

    def get_all_people(self):
        """
        Returns a list of all elements in the person table
        :return: list of people
        """
        cur = self._conn.cursor()
        cur.execute('SELECT * FROM person')
        people = []
        for row in cur.fetchall():
            people.append(dict(row))

        return people

    def get_all_activities(self):
        """
        Gets a list of all elements in the activity table
        :return: list of activities
        """
        cur = self._conn.cursor()
        cur.execute('SELECT * FROM activity')
        activities = []
        for row in cur.fetchall():
            activities.append(dict(row))

        return activities

    def get_all_events(self):
        """
        Gets a list of all elements in the event table
        :return: list of events
        """
        cur = self._conn.cursor()
        cur.execute('SELECT * FROM event')
        events = []
        for row in cur.fetchall():
            events.append(dict(row))

        return events

    def get_person_by_id(self, person_id):
        """
        Gets a person from the person table by id
        :param person_id: id of the person
        :return: person associated with id
        """
        cur = self._conn.cursor()
        query = '''SELECT * FROM person WHERE person.person_id = ?'''
        cur.execute(query, (person_id,))

        return dict(cur.fetchone())

    def get_activity_by_id(self, activity_id):
        """
        Gets an activity from the activity table by id
        :param activity_id: id of the person
        :return: acitivity associated with id
        """
        cur = self._conn.cursor()
        query = '''SELECT * FROM activity WHERE activity.activity_id = ?'''
        cur.execute(query, (activity_id,))

        return dict(cur.fetchone())

    def get_event_by_id(self, event_id):
        """
        Gets an event from the event table by id
        :param event_id: id of the event
        :return: event associated with id
        """
        cur = self._conn.cursor()
        query = '''SELECT * FROM event WHERE event.event_id = ?'''
        cur.execute(query, (event_id,))

        return dict(cur.fetchone())

    def get_event_by_person(self, person_id):
        """
        Gets all events from the event table by the person hosting it
        :param person_id: id of the activity
        :return: list of all events for a person
        """
        cur = self._conn.cursor()
        query = '''SELECT * FROM event WHERE event.person_id = ?'''
        cur.execute(query, (person_id,))
        events = []
        for row in cur.fetchall():
            events.append(dict(row))

        return events

    def get_event_by_activity(self, activity_id):
        """
        Gets all events from the event table by the activity
        :param activity_id: id of the activity
        :return: list of all events for an activity
        """
        cur = self._conn.cursor()
        query = '''SELECT * FROM event WHERE event.activity_id = ?'''
        cur.execute(query, (activity_id,))
        events = []
        for row in cur.fetchall():
            events.append(row)


        return events

    def get_event_by_date(self, date):
        """
        Gets all events from the event table by the date its scheduled
        :param date: id of the activity
        :return: list of all events for a date
        """
        cur = self._conn.cursor()
        query = '''SELECT * FROM event WHERE event.date = ?'''
        cur.execute(query, (date,))
        events = []
        for row in cur.fetchall():
            events.append(row)

        return events

    def insert_person(self, name):
        """
        Posts a new person into the person table.
        :param name: name of person
        """
        cur = self._conn.cursor()
        cur.execute('INSERT INTO person(name) VALUES(?)',
                    (name,))
        self._conn.commit()

    def insert_activity(self, name):
        """
        Posts a new activity into the activity table
        :param name: name of the activity
        """
        cur = self._conn.cursor()
        cur.execute('INSERT INTO activity(name) VALUES(?)', (name,))
        self._conn.commit()

    def insert_event(self, person_id, activity_id, date, amount):
        """
        Posts a new event into the event table. Currently requires person and
        activity to be in their respective tables
        :param person: person hosting the event
        :param activity: type of activity of the event
        :param date: date of the event
        :param amount: amount of money the event costs
        """
        cur = self._conn.cursor()

        cur.execute('INSERT INTO event(person_id, activity_id, date, amount) '
                    'VALUES(?,?,?,?)',
                    (person_id, activity_id, date, amount,))

        self._conn.commit()

    def delete_person(self, person_id):
        """
        Deletes a person from the person table
        :param person_id: id of the person to delete
        """
        cur = self._conn.cursor()
        query = '''DELETE FROM person WHERE person.person_id = ?'''
        cur.execute(query, (person_id,))

    def delete_activity(self, activity_id):
        """
        Deletes an activity from the activity table
        :param activity_id: id of the person to delete
        """
        cur = self._conn.cursor()
        query = '''DELETE FROM activity WHERE activity.activity_id = ?'''
        cur.execute(query, (activity_id,))

    def delete_event(self, event_id):
        """
        Deletes an event from the event table
        :param event_id: id of the event to delete
        """
        cur = self._conn.cursor()
        query = '''DELETE FROM event WHERE event.event_id = ?'''
        cur.execute(query, (event_id,))
