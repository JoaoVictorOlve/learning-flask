from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/about')
def about():
    return 'The about page'

@app.route('/about/<int:number>')
def about(number):
    return f'The about {number}'
