
from google.appengine.api import users
import webapp2

import main
import utils

# Potentially helpful (or not) superclass for *logged in* pages and actions (assumes app.yaml gaurds for login)

### Pages ###
class BasePage(webapp2.RequestHandler):
  """Page handlers should inherit from this one."""
  def get(self):
    user = users.get_current_user()
    if not user:
      raise Exception("Missing user!")
    email = user.email().lower()
    account_info = utils.get_account_info_for_email(email, create_if_none=True)
    values = {"user_email": email,
              "account_info": account_info,
              "logout_url": users.create_logout_url("/")}
    self.update_values(email, account_info, values)
    template = main.jinja_env.get_template(self.get_template())
    self.response.out.write(template.render(values))


  def update_values(self, email, account_info, values):
    # Subclasses should override this method to add additional data for the Jinja template.
    pass


  def get_template(self):
    # Subclasses must override this method to set the Jinja template.
    raise Exception("Subclass must implement handle_post!")



### Actions ###

class BaseAction(webapp2.RequestHandler):
  """ALL action handlers should inherit from this one."""
  def post(self):
    user = users.get_current_user()
    if not user:
      raise Exception("Missing user!")
    email = user.email().lower()
    account_info = utils.get_account_info_for_email(email)
    self.handle_post(email, account_info)


  def get(self):
    self.post()  # Action handlers should not use get requests.


  def handle_post(self, email, account_info):
    # Subclasses must override this method to handle the requeest.
    raise Exception("Subclass must implement handle_post!")
