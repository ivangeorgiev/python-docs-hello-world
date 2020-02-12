from flask import Flask
from flask import request, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return """Hello World!<br><a href="/headers">Headers</a>"""

@app.route("/headers")
def show_headers():
  return jsonify(dict(request.headers))



@app.route("/print")
def print_route():
  print("Handling request to home page.")
  return "Hello Azure!"
