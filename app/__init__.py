import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
import time

cors = CORS()

db: SQLAlchemy = SQLAlchemy()
scheduler = APScheduler()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")  # 测试数据库

    app.template_folder = "../templates"
    app.static_folder = "../static"

    cors.init_app(app)
    db.init_app(app)

    from app import db_model
    with app.app_context():
        db.create_all()

    scheduler.init_app(app)

    @scheduler.task('interval', id='mcstatus', seconds=600, misfire_grace_time=900)
    def job1():
        time_ = time.localtime()
        print(time_)
        # database.insert(ADDRESS, get_status(ADDRESS), time.strftime(format_, time_))

    scheduler.start()


    from app.api import api

    # 注册蓝图
    app.register_blueprint(api, url_prefix="/api")

    @app.route('/')
    def hello_world():  # put application's code here
        return 'Hello World!'

    return app


