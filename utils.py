import logging

from google.appengine.ext import ndb

from models import Task, List

MASTER_KEY = ndb.Key("Entity", "MASTER_KEY")

# TODO: Implement
def get_parent_key_for_email(email):
    """ Gets the parent key (the key that is the parent to all Datastore data for this user) from the user's email. """
    return ndb.Key("Entity", email.lower())

def get_query_for_all_tasks_for_email(email):
    """ Returns a query for all Task objects for this user. """
    email_key = get_parent_key_for_email(email)
    master_query = Task.query(ancestor=MASTER_KEY)
    return master_query.filter(Task.access_keys == email_key).order(Task.due_date_time)

def get_query_for_all_private_lists_for_email(email):
    """ Returns a query for all List objects for this user. """
    email_key = get_parent_key_for_email(email)
    master_query = List.query(ancestor=MASTER_KEY)
    return master_query.filter(ndb.AND(List.access_keys == email_key, List.shared == False)).order(List.name)

def get_query_for_all_shared_lists_for_email(email):
    """ Returns a query for all List objects for this user. """
    email_key = get_parent_key_for_email(email)
    master_query = List.query(ancestor=MASTER_KEY)
    return master_query.filter(ndb.AND(List.access_keys == email_key, List.shared == True)).order(List.name)

def get_query_for_all_task_for_list_key(list_key_urlsafe):
    """ Returns a query for all Task objects for this List. """
    list_key = ndb.Key(urlsafe=list_key_urlsafe)
    return Task.query(ancestor=list_key).order(Task.due_date_time)

def update_access_keys_for_all_tasks_in_list(list_key_urlsafe, access_keys):
    """ Updates access keys for all tasks belonging to this list. """
    for task in get_query_for_all_task_for_list_key(list_key_urlsafe):
        task.access_keys = access_keys
        task.put()

def get_access_key_email_string_for_list(listObj):
    emailString = ""
    ownerEmail = listObj.owner.id()
    for i in range (0, len(listObj.access_keys)):
        currentEmail = listObj.access_keys[i].id()
        if not (currentEmail == ownerEmail):
            if not (i == 0):
                emailString += ", "
            emailString += currentEmail
    return emailString
