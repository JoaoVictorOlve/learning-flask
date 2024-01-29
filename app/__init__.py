from flask import Flask
from configparser import ConfigParser
import os

app = Flask(__name__)

config = ConfigParser()
config.read('.env')
app.config["ENV"] = config["environment"]["FLASK_ENV"]

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

print(app.config["ENV"])

from app import views
from app import admin_views