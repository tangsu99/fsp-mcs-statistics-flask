import time
from datetime import datetime, timedelta, date

import psutil
from flask import Blueprint, jsonify, request
from sqlalchemy import desc

from app.db_model.statuslog import StatusLog
from mcs import get_online_player

api = Blueprint("api", __name__)
ADDRESS = 'dt.dawntown.cn:49001'


@api.route("/", methods=["GET", "POST"])
def index():
    return jsonify({
        "status": "ok",
        "msg": "Hello World!"
    })


@api.route("/sys")
def sys_info():
    cpu = psutil.cpu_percent(interval=2, percpu=False)
    mem = psutil.virtual_memory().percent
    return jsonify({
        "timestamp": int(time.time() * 1000),  # ms，用于 x 轴
        "cpu": cpu,
        "memory": mem
    })


@api.route('/online')
def online_player():
    return get_online_player(ADDRESS)


@api.route('/status')
def status():
    return jsonify({})


@api.route('/statuslog')
def status_log():
    range_ = request.args.get('range', '')
    size = int(request.args.get('size', 200))

    data = {'count': [], 'date': []}
    query = StatusLog.query

    if 'size' in request.args:
        results = query.order_by(desc(StatusLog.log_datetime)).limit(size).all()

    else:
        if range_:
            try:
                start_str, end_str = range_.split(',')
                start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_str, '%Y-%m-%d').date() + timedelta(days=1)
                query = query.filter(
                    StatusLog.log_datetime >= start_date,
                    StatusLog.log_datetime < end_date
                )
            except ValueError:
                return data

        else:
            print("没有参数")
            today = date.today()
            tomorrow = today + timedelta(days=1)
            query = query.filter(
                StatusLog.log_datetime >= today,
                StatusLog.log_datetime < tomorrow
            )

        # 执行查询
        results = query.order_by(desc(StatusLog.log_datetime)).all()

    results.reverse()

    for record in results:
        data['count'].append(record.player_count)
        data['date'].append(record.log_datetime.isoformat())

    return data