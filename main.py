import datetime
import json
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
        values['private_list_query'] = utils.get_query_for_all_private_lists_for_email(email)
        values['shared_list_query'] = utils.get_query_for_all_shared_lists_for_email(email)

        if values['listKey']:
            values['tasks_query'] = utils.get_query_for_all_task_for_list_key(values['listKey'])
            list_key = ndb.Key(urlsafe=values['listKey'])
            list_obj = list_key.get();
            values['list_name'] = list_obj.name;
            values['list_emails'] = utils.get_access_key_email_string_for_list(list_obj)
        else:
            values['tasks_query'] = utils.get_query_for_all_tasks_for_email(email)
            values['list_name'] = "All Tasks";


    def get_template(self):
        return "templates/lists.html"

class InsertTaskAction(BaseAction):
    def handle_post(self, email):
        if self.request.get("entity_key"):
            task_key = ndb.Key(urlsafe=self.request.get("entity_key"))
            task = task_key.get()
        else:
            if self.request.get("listKey"):
                key = ndb.Key(urlsafe=self.request.get("listKey"))
                task = Task(parent=key)
                task.access_keys = key.get().access_keys
            else:
                task = Task(parent=utils.get_parent_key_for_email(email))
                task.access_keys = [utils.get_parent_key_for_email(email)]

        task.name = self.request.get("name")
        task.due_date_time = datetime.datetime.strptime( self.request.get("due_date_time"), "%Y-%m-%dT%H:%M" )
        task.note = self.request.get("note")
        is_complete = self.request.get("is_complete")
        if is_complete:
            task.is_complete = True
        elif not is_complete:
            task.is_complete = False
        else:
            raise Exception("Cannot read is_complete value!")
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
            list.owner = utils.get_parent_key_for_email(email)

        list.name = self.request.get("name")
        list_key = list.put()
        list.url = "/lists?listKey=" + list_key.urlsafe()

        shared_emails = self.request.get("shared").split(", ")
        access_keys = []
        for current_email in shared_emails:
            if not (current_email == ""):
                access_keys.append(utils.get_parent_key_for_email(current_email))
        access_keys.append(list.owner)
        list.access_keys = access_keys
        utils.update_access_keys_for_all_tasks_in_list(list.key.urlsafe(), access_keys)

        if len(access_keys) > 1:
            list.shared = True
        else:
            list.shared = False

        list.put()
        if (email.lower() in shared_emails):
            self.redirect(list.url)
        else:
            self.redirect("/#")

class DeleteListAction(BaseAction):
    def handle_post(self, email):
        list_key = ndb.Key(urlsafe=self.request.get("entity_key"))

        tasks = utils.get_query_for_all_task_for_list_key(self.request.get("entity_key"))

        for task in tasks:
            task.key.delete()

        list_key.delete()
        self.redirect('/')

class ToggleCompleteAction(webapp2.RequestHandler):
    def post(self):
        index = self.request.get("index")
        task_key = ndb.Key(urlsafe=self.request.get("entityKey"))
        task = task_key.get()

        task.is_complete = not task.is_complete
        task.put()

        self.response.headers["Content-Type"] = "application/json"
        response = {"index": index, "is_complete": task.is_complete}
        self.response.out.write(json.dumps(response))

class InsertCommentAction(webapp2.RequestHandler):
    def post(self):
        new_comment = self.request.get("comment")
        user = users.get_current_user()
        new_comment = user.email().lower() + ": " + new_comment
        task_key = ndb.Key(urlsafe=self.request.get("task-key"))
        task = task_key.get()

        current_comments = task.comments

        if current_comments is not None:
            current_comments.append(new_comment)
            task.comments = current_comments
        else:
            task.comments = [new_comment]
        task.put()

        self.redirect(self.request.referer)

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/lists', ListsPage),
    ('/inserttask', InsertTaskAction),
    ('/deletetask', DeleteTaskAction),
    ('/insertlist', InsertListAction),
    ('/deletelist', DeleteListAction),
    ('/togglecomplete', ToggleCompleteAction),
    ('/postcomment', InsertCommentAction)
], debug=True)
