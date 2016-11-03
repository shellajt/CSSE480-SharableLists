import datetime
import os

from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2

from handlers.base_handlers import BasePage, BaseAction
from models import Task, List
import utils


# Jinja environment instance necessary to use Jinja templates.
def __init_jinja_env():
    jenv = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols", "jinja2.ext.with_"],
        autoescape=True)
    # Example of a Jinja filter (useful for formatting data sometimes)
    #   jenv.filters["time_and_date_format"] = date_utils.time_and_date_format
    return jenv

jinja_env = __init_jinja_env()


class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/lists')
            return

        template = jinja_env.get_template("templates/login.html")
        values = {"login_url": users.create_login_url('/lists')}
        self.response.write(template.render(values))

class ListsPage(BasePage):
    def update_values(self, email, values):
        values['tasks_query'] = utils.get_query_for_all_tasks_for_email(email)

    def get_template(self):
        return "templates/lists.html"

class InsertTaskAction(BaseAction):
    def handle_post(self, email):
        if self.request.get("entity_key"):
            task_key = ndb.Key(urlsafe=self.request.get("entity_key"))
            task = task_key.get()
        else:
            task = Task(parent=utils.get_parent_key_for_email(email))

        task.name = self.request.get("name")
        task.due_date_time = datetime.datetime.strptime( self.request.get("due_date_time"), "%Y-%m-%dT%H:%M" )
        task.note = self.request.get("note")
        is_complete = self.request.get("is_complete")
        if is_complete:
            task.is_complete = True
        else:
            task.is_complete = False
        task.put()
        self.redirect(self.request.referer)

class DeleteTaskAction(BaseAction):
    def handle_post(self, email):
        task_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        task_key.delete()
        self.redirect(self.request.referer)

class InsertListAction(BaseAction):
    def handle_post(self, email):
        if self.request.get("entity_key"):
            list_key = ndb.Key(urlsafe=self.request.get("entity_key"))
            list = list_key.get()
        else:
            list = List(parent=utils.get_parent_key_for_email(email))

        list.name = self.request.get("name")
        # TODO: Add fields for shared lists

        list.put()
        self.redirect(self.request.referer)

class DeleteListAction(BaseAction):
    def handle_post(self, email):
        task_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        task_key.delete()
        self.redirect(self.request.referer)

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/lists', ListsPage),
    ('/inserttask', InsertTaskAction),
    ('/deletetask', DeleteTaskAction),
    ('/insertlist', InsertListAction),
    ('/deletelist', DeleteListAction)
], debug=True)
