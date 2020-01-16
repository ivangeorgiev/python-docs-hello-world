from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/print")
def print_route():
  print("Handling request to home page.")
  return "Hello Azure!"
