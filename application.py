from flask import Flask
from flask import request, jsonify
import requests

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

  headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'User-Agent': 'adal-python-sample',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
  response = requests.get(
      "https://graph.microsoft.com/v1.0/users/{}".format(principal_id),
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
