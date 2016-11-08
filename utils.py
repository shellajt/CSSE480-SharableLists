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
    return Task.query(ancestor=parent_key).order(Task.due_date_time)

def get_query_for_all_private_lists_for_email(email):
    """ Returns a query for all List objects for this user. """
    parent_key = get_parent_key_for_email(email)
    invalid_key = get_parent_key_for_email("invalid")
    return List.query(ancestor=parent_key).filter(List.shared_keys == invalid_key)

def get_query_for_all_shared_lists_for_sharee_email(email):
    """ Returns a query for all List objects for this user. """
    shared_key = get_parent_key_for_email(email)
    return List.query(List.shared_keys == shared_key).order(List.name)

def get_query_for_all_shared_lists_for_owner_email(email):
    """ Returns a query for all List objects for this user. """
    parent_key = get_parent_key_for_email(email)
    invalid_key = get_parent_key_for_email("invalid")
    query = List.query(ancestor=parent_key)
    return query.filter(List.shared_keys != invalid_key)

def get_query_for_all_task_for_list_key(list_key_urlsafe):
    """ Returns a query for all Task objects for this List. """
    list_key = ndb.Key(urlsafe=list_key_urlsafe)
    return Task.query(ancestor=list_key).order(Task.due_date_time)
