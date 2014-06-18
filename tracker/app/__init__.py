from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# Startup stuff
app = Flask(__name__)
app.config.from_object('config')

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'static/matrix/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt'])
# code for clienthandshake
app.config['CLIENT_HANDSHAKE'] = 'ILIKETURTLES'
app.config['active_time'] = 120

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

# Register blueprints
from app.api import *
from app.api.task import task_api
from app.views.views import views_blueprint
from app.views.login import login_blueprint

app.register_blueprint(peer_api)
app.register_blueprint(views_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(task_api)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.htm'), 404

# Add methods and modules to jinja environment
from app.utils import serialize_sqla
import json
app.jinja_env.globals.update(json=json)
app.jinja_env.globals.update(serialize_sqla=serialize_sqla)
app.jinja_env.globals.update(len=len)

