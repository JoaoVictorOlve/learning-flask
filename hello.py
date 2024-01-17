from flask import Flask, url_for, request, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('layout.html', name=name)
    