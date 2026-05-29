from flask import Flask, redirect
import json
import os

app = Flask(__name__)

# -------------------------
# DATABASE FILE
# -------------------------

DB_FILE = "links.json"

# -------------------------
# CREATE FILE
# -------------------------

if not os.path.exists(DB_FILE):

    with open(DB_FILE, "w") as f:

        json.dump({}, f)

# -------------------------
# LOAD LINKS
# -------------------------

def load_links():

    with open(DB_FILE, "r") as f:

        return json.load(f)

# -------------------------
# REDIRECT
# -------------------------

@app.route("/<code>")

def short_link(code):

    links = load_links()

    if code in links:

        return redirect(
            links[code]
        )

    return "Link not found"

# -------------------------
# RUN
# -------------------------

app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)