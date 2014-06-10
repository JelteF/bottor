"""views.py - View for administration."""
from flask import render_template, Blueprint

views_blueprint = Blueprint('views', __name__, url_prefix='')


@views_blueprint.route('/home', methods=['GET'])
@views_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home.htm', data={})
