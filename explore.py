import requests
import os
import logging
import json
from cmd import Cmd

EP_USERS = "/users"
EP_USER = "/users/{id}"
EP_USER_MANAGER = "/users/{id}/manager"


def get_access_token(client_id, tenant_id, client_secret, scope='https://graph.microsoft.com/.default'):
  token_endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
  data = dict(
        client_id=client_id,
        scope=scope,
        client_secret=client_secret,
        grant_type='client_credentials'
      )
  response = requests.post(token_endpoint, 
      data=data,
      headers={
        'Content-Type': 'application/x-www-form-urlencoded'
      })
  access_token = response.json()['access_token']
  return access_token


class MyShell(Cmd):
  prompt = "shell> "
  intro = "Welcome! Type ? to list commands."
  access_token = None
  initialized = False
  api_url = "https://graph.microsoft.com"
  api_version = "v1.0"
  last_response = None

  @property
  def client_id(self):
    return os.environ.get("IG_CLIENT_ID")

  @property
  def tenant_id(self):
    return os.environ.get("IG_TENANT_ID")

  @property
  def client_secret(self):
    return os.environ.get("IG_CLIENT_SECRET")

  def do_exit(self, inp):
    """Exit shell"""
    print("Bye")
    return True

  def do_list_users(self, inp):
    """List users"""
    pass

  def do_init(self, inp):
    """Initialize"""

    self.access_token = get_access_token(self.client_id, self.tenant_id, self.client_secret)
    self.initialized = True


  def do_get(self, inp):
    """Get a property.

    Syntax:
      get {client_id | tenant_id | client_secret | access_token}
    """
    try:
      print(getattr(self, inp))
    except Exception as ex:
      print("ERROR: {}".format(ex))

  def _graph_query(self, endpoint, endpoint_vars={}):
    if not self.initialized:
      raise Exception("Not initialized. Try 'init' first.")
    headers = {
      "Authorization": "Bearer {}".format(self.access_token),
      "User-Agent": "Python Web App",
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    endpoint_url = "{}/{}{}".format(self.api_url, self.api_version,
              endpoint.format(**endpoint_vars))
    return requests.get(endpoint_url, headers=headers)


  def do_graph_query(self, inp):
    """Query graph API"""
    try:
      self.last_response = self._graph_query(inp)
      print(self.last_response.status_code)
    except Exception as ex:
      print(f"ERROR: {ex}")

  def do_users(self, inp):
    """Get user info
    
    Syntax:
       users [<user-id>]
    """
    if inp:
      endpoint = EP_USER.format(**dict(id=inp))
    else:
      endpoint = EP_USERS
    try:
      self.last_response = self._graph_query(endpoint)
      print(f"{self.last_response.status_code}")
    except Exception as ex:
      print(f"ERROR: {ex}")

  def do_manager(self, inp):
    """Get user manager
    
    Syntax: 
       manager <user-id>
    """
    try:
      self.last_response = self._graph_query(EP_USER_MANAGER, dict(id=inp))
      print(f"{self.last_response.status_code}")
    except Exception as ex:
      print(f"ERROR: {ex}")


  def do_response(self, inp):
    """Print response parts

    Syntax:
       response {code | text | json}
    """
    if self.last_response is None:
      print("ERROR: No saved last reponse")
      return
    try:
      if inp == "code":
        print(self.last_response.status_code)
      elif inp == "text":
        print(self.last_response.text)
      elif inp == "json":
        print(json.dumps(self.last_response.json(), indent=3))
      else:
        print("Nothing requested")
    except Exception as ex:
      print(f"ERROR: {ex}")



if __name__ == "__main__":
  MyShell().cmdloop()
