from flask import Flask, url_for, request, render_template, abort, redirect
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
