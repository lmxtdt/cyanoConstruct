#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:32:02 2020

@author: liathomson
"""

#__init__.py

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from cyanoConstruct.config import Config



app = Flask(__name__)
#login = LoginManager(app)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from cyanoConstruct import CyanoConstructMod
from cyanoConstruct import Component
from cyanoConstruct import SessionUsers
from cyanoConstruct import CCDatabase

__version__ = "0.2"