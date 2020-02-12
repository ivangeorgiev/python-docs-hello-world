from flask import Flask
from flask import request, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!<br>" + jsonify(request.headers)


@app.route("/print")
def print_route():
  print("Handling request to home page.")
  return "Hello Azure!"
