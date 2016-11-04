from google.appengine.ext import ndb

class User(ndb.Model):
    """ Information about this user.  There is only 1 of these per user. """
    email = ndb.StringProperty()
    display_name = ndb.StringProperty()
    """ This property likely to change as we figure out what we need """
    preferences = ndb.StringProperty(repeated=True)
    
class Folder(ndb.Model):
    """ Information about a user's folder structure """
    name = ndb.StringProperty()
    
class List(ndb.Model):
    """ Information about an individual list """
    name = ndb.StringProperty()
    folder_key = ndb.KeyProperty(kind=Folder)
    shared_keys = ndb.KeyProperty(repeated=True)

class Task(ndb.Model):
    """ Information about a task within a list """
    name = ndb.StringProperty()
    due_date_time = ndb.DateTimeProperty()
    note = ndb.StringProperty()
    is_complete = ndb.BooleanProperty(default=False)
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)
    
class Comment(ndb.Model):
    """ Information about a comment on a task """
    creater_key = ndb.KeyProperty(kind=User)
    text = ndb.StringProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now=True)

    