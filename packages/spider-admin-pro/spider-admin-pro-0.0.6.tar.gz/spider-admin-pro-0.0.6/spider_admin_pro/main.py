# -*- coding: utf-8 -*-
from flask import request, make_response
from flask_cors import CORS

from spider_admin_pro.api.auth_api import auth_api
from spider_admin_pro.api.schedule_api import schedule_api
from spider_admin_pro.api.scrapyd_api import scrapyd_api
from spider_admin_pro.api.stats_collection_api import stats_collection_api
from spider_admin_pro.api.system_info_api import system_api
from spider_admin_pro.flask_app import FlaskApp
from spider_admin_pro.web.main import web

app = FlaskApp(__name__, static_folder=None)
CORS(app, supports_credentials=True)

app.register_blueprint(web, url_prefix="/")
app.register_blueprint(auth_api, url_prefix="/api/auth")
app.register_blueprint(scrapyd_api, url_prefix="/api/scrapyd")
app.register_blueprint(schedule_api, url_prefix="/api/schedule")
app.register_blueprint(system_api, url_prefix="/api/system")
app.register_blueprint(stats_collection_api, url_prefix="/api/statsCollection")


@app.before_request
def before_request():
    """跨域请求会出现options，直接返回即可"""
    if request.method == 'OPTIONS':
        return make_response()
