from flask import Flask
from flask import request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return """Hello World!<br><a href="/headers">Headers</a>"""

@app.route("/headers")
def show_headers():
  return jsonify(dict(request.headers))


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
