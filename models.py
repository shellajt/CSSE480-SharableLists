from google.appengine.ext import ndb

class List(ndb.Model):
    """ Information about an individual list """
    name = ndb.StringProperty()
    shared_keys = ndb.KeyProperty(repeated=True)
    url = ndb.StringProperty()

class Task(ndb.Model):
    """ Information about a task within a list """
    name = ndb.StringProperty()
    due_date_time = ndb.DateTimeProperty()
    note = ndb.StringProperty()
    is_complete = ndb.BooleanProperty(default=False)
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)
    comments = ndb.StringProperty(repeated=True)