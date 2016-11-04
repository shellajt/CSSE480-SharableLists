import logging

from google.appengine.ext import ndb

from models import Task, List


# TODO: Implement
def get_parent_key_for_email(email):
    """ Gets the parent key (the key that is the parent to all Datastore data for this user) from the user's email. """
    return ndb.Key("Entity", email.lower())

def get_query_for_all_tasks_for_email(email):
    """ Returns a query for all Task objects for this user. """
    parent_key = get_parent_key_for_email(email)
    return Task.query(ancestor=parent_key).order(Task.last_touch_date_time)

def get_query_for_all_private_lists_for_email(email):
    """ Returns a query for all List objects for this user. """
    parent_key = get_parent_key_for_email(email)
    return List.query(ancestor=parent_key).order(List.name)

def get_query_for_all_shared_lists_for_email(email):
    """ Returns a query for all List objects for this user. """
    shared_key = get_parent_key_for_email(email)
    return List.query(List.shared_keys == shared_key).order(List.name)

def get_query_for_all_task_for_list_key(list_key):
    """ Returns a query for all Task objects for this List. """
    return Task.query(ancestor=list_key).order(Task.last_touch_date_time)
