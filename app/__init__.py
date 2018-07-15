# -*- coding:utf-8 -*-
__author__ = u'Jiang Wen'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler

# from flask_uploads import UploadSet, configure_uploads, DATA
import os

app = Flask ( __name__ )
app.config.from_object ( 'config' )
db = SQLAlchemy ( app )
lm = LoginManager ()
lm.init_app ( app )
DEBUGGING = False
CENTER_API_URL = 'http://127.0.0.1:8080/api'
# CENTER_API_URL = 'http://localhost/mytest/get_info_from_TSM.php'
# app.config.from_object ( Config () )
scheduler = APScheduler ()  # it is also possible to enable the API directly
# scheduler.api_enabled = True
scheduler.init_app ( app )
scheduler.start ()
from app import models, views
