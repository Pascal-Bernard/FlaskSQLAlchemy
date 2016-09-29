# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api

# initialize flask and flask restful
app = Flask(__name__)
app.config['SECRET_KEY'] = "bmcp-plugin-lenovo"
app.debug = True

api = Api(app)

from views import init_routes

init_routes()
