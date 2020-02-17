from flask import Flask
from flask import render_template, request, jsonify
import requests
import os

app = Flask(__name__)


def get_access_token(scope='https://graph.microsoft.com/.default'):
  client_id = os.environ.get("IG_CLIENT_ID")
  tenant_id = os.environ.get("IG_TENANT_ID")
  client_secret = os.environ.get("IG_CLIENT_SECRET")

  token_endpoint = "https://login.microsoftonline.com/{}/oauth2/v2.0/token".format(tenant_id)
  response = requests.post(token_endpoint, 
      data=dict(
        client_id=client_id,
        scope=scope,
        client_secret=client_secret,
        grant_type='client_credentials'
      ),
      headers={
        'Content-Type': 'application/x-www-form-urlencoded'
      })
  return response

def query_graph_users(access_token, user_id=""):
  endpoint_url = "https://graph.microsoft.com/v1.0/users/{}".format(user_id)
  headers = {
    "Authorization": "Bearer {}".format(access_token),
    "User-Agent": "Python Web App",
    "Accept": "application/json",
    "Content-Type": "application/json"
  }
  response = requests.get(endpoint_url, headers=headers)
  return response


@app.route("/")
def home():
    vars = dict(

    )
    return render_template('index.html', **vars)
    # """Hello World!<br><a href="/headers">Headers</a>"""

@app.route("/about")
def about():
    vars = dict(

    )
    return render_template('index.html', **vars)
    # """Hello World!<br><a href="/headers">Headers</a>"""

@app.route("/contact")
def contact():
    vars = dict(

    )
    return render_template('index.html', **vars)
    # """Hello World!<br><a href="/headers">Headers</a>"""




@app.route("/headers")
def show_headers():
  vars = dict(
    headers=dict(request.headers)
  )
  return render_template('headers.html', **vars) # jsonify(dict(request.headers))


@app.route("/apptoken")
def app_token():
  token_response = get_access_token()
  
  if token_response.status_code < 400:
    access_token = token_response.json().get('access_token', 'UNKNOWN')
    graph_query_response = query_graph_users(access_token)
  else:
    access_token = "ERROR"
    graph_query_response = "ERROR getting token"

  vars = dict(
    token_response=token_response,
    access_token=access_token,
    graph_query_response=graph_query_response
  )

  return render_template('app_token.html', **vars) # jsonify(dict(request.headers))

@app.route("/me")
def show_me():

  
  principal_id = request.headers['X-Ms-Client-Principal-Id']
  access_token = request.headers['X-Ms-Token-Aad-Access-Token']
  tenant_id = os.environ['IG_TENANT_ID']

  params = {
    'api-version': '1.6'
  }
  headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'User-Agent': 'adal-python-sample',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
  response = requests.get(
      "https://graph.windows.net/{}/users/{}".format(tenant_id, principal_id),
      params=params,
      headers = headers
    )
  json_response = response.json()
  return jsonify(dict(json_response))


@app.route("/print")
def print_route():
  print("Handling request to home page.")
  return "Hello Azure!"


if __name__ == "__main__":
  app.run(debug=True)
