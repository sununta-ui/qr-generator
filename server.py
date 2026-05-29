from flask import Flask, redirect, request, jsonify
import json
import os

app = Flask(__name__)

DB_FILE = "links.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_links():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_links(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

@app.route("/add", methods=["POST"])
def add_link():

    data = request.json

    code = data["code"]
    url = data["url"]

    links = load_links()

    links[code] = url

    save_links(links)

    return jsonify({
        "status": "success"
    })

@app.route("/<code>")
def short_link(code):

    links = load_links()

    if code in links:
        return redirect(links[code])

    return "Link not found"

@app.route("/")
def home():
    return "QR Generator Server Online"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )