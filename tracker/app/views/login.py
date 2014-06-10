from flask import render_template, flash, Blueprint, request, session, \
    jsonify, redirect, url_for
from app.models import Account
from app.utils import timeout, serialize_sqla
from functools import wraps

login_blueprint = Blueprint('login', __name__, url_prefix='')


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login route."""

    # Form has been submitted, check credentials, set session and redirect
    # to the homepage
    if request.method == 'POST':
        if request.form:
            user = request.form
        if request.json:
            user = request.json

        try:
            name = user['name']
            password = user['password']

            session['user'] = check_login(name, password)
            timeout.timein()
            if request.json:
                return jsonify()
            flash('Je bent succesvol ingelogged.', 'success')

            if 'redirect_url' in session:
                url = session['redirect_url']
                session.pop('redirect_url', None)
                return redirect(url)
            return redirect(url_for('views.home'))

        except ValueError as e:
            if request.json:
                return jsonify(error=str(e)), 401
            flash(e, 'danger')

    # If it's a get request, return loginpage
    return render_template('login.htm')


@login_blueprint.route('/logout', methods=['GET'])
def logout():
    """Log the user out and remove him from the session."""
    session.pop('user', None)
    return redirect(url_for('views.home'))


def check_login(name, password):
    """Check if a username, password combination match."""
    user = Account.query.filter(Account.name == name).first()
    if user is None:
        raise ValueError("Gebruiker niet gevonden.")
    else:
        if user.check_password(password):
            return serialize_sqla(user)
        else:
            raise ValueError("Verkeerd wachtwoord.")


def login_redirect(fn):
    """Function decorator that checks if someone is logged in."""
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not request.json:
            session['redirect_url'] = request.url

        if 'user' not in session or not session['user']:
            if request.json:
                error = ('U bent niet ingelogd. '
                         'Kunt u laten weten dat dit gebeurd is? '
                         'Dit hoort namelijk niet te kunnen.')
                return jsonify(error=error), 401

            return redirect(url_for('login.login'))

        # Handle session timeouts
        if not timeout.refresh():
            session.pop('user', None)
            error = 'Door te lange inactiviteit bent u uitgelogd'
            if request.json:
                return jsonify(error=error), 401

            flash(error)
            return redirect(url_for('login.login'))

        return fn(*args, **kwargs)

    return wrapped
