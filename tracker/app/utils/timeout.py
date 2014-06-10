import datetime as dt
from flask import session
from app import app

TIMEOUT = dt.timedelta(days=1)


def timein():
    session['user_timein'] = dt.datetime.now()


def refresh():

    # Check whether the user's session has expired.
    delta = dt.datetime.now() - session['user_timein']
    if (delta.total_seconds() > TIMEOUT.total_seconds()):
        return False

    # Refresh the session.
    timein()
    return True
