from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# Startup stuff
app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

# Register blueprints
from app.api import *
from app.views.views import views_blueprint
from app.views.login import login_blueprint

app.register_blueprint(views_blueprint)
app.register_blueprint(login_blueprint)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.htm'), 404

# Add methods and modules to jinja environment
from app.utils import serialize_sqla
import json
app.jinja_env.globals.update(json=json)
app.jinja_env.globals.update(serialize_sqla=serialize_sqla)
