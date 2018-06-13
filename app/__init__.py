# -*- coding:utf-8 -*-
__author__ = u'Jiang Wen'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_uploads import UploadSet, configure_uploads, DATA
import os

app = Flask ( __name__ )
app.config.from_object ( 'config' )
db = SQLAlchemy ( app )
lm = LoginManager ()
lm.init_app ( app )
CENTER_API_URL = 'http://0.0.0.0:8080/api'
from app import models, views
