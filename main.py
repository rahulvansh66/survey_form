from flask import Flask, jsonify
from flask import Flask, render_template, request, url_for, redirect
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("main.html") #jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
