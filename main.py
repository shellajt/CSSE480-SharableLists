#<!-- TODO: Remove all traces of Kid Tracker source code -->


import os

from google.appengine.api import users
import jinja2
import webapp2

from handlers.base_handlers import BasePage


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
#     def update_values(self, email, values):
#         values['kids_query'] = utils.get_query_for_all_kids_for_email(email)
        
    def get_template(self):
        return "templates/lists.html"

app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/lists', ListsPage)
], debug=True)
