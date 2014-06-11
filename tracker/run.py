#!venv/bin/python
"""run.py - Run the application.

Flask-Failsafe ensures that when the application crashes, it can still restart
(if in debug mode).

"""
from flask_failsafe import failsafe


@failsafe
def create_app():
    from app import app

    return app

if __name__ == '__main__':
    create_app().run()
