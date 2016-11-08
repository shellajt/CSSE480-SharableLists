from google.appengine.ext import ndb

class List(ndb.Model):
    """ Information about an individual list """
    name = ndb.StringProperty()
    access_keys = ndb.KeyProperty(repeated=True)
    url = ndb.StringProperty()
    shared = ndb.BooleanProperty()
    owner = ndb.KeyProperty()

class Task(ndb.Model):
    """ Information about a task within a list """
    name = ndb.StringProperty()
    due_date_time = ndb.DateTimeProperty()
    note = ndb.StringProperty()
    is_complete = ndb.BooleanProperty(default=False)
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)
    comments = ndb.StringProperty(repeated=True)
    access_keys = ndb.KeyProperty(repeated=True)
