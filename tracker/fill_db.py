#!venv/bin/python
"""fill_db.py - Fill the database.

This script fills the database with dummy data, which makes it easier to test
the system.

"""
from app import db
from app.models import *
from app.controllers.job import JobController
from app.controllers.matrix import MatrixController
from werkzeug.security import generate_password_hash

#Main account
admin = Account('root', 'n3tb0t')
db.session.add(admin)
db.session.commit()

peer1 = Peer('77.249.206.212')
db.session.add(peer1)
db.session.commit()

matrixA = "sample_matrices/A20"
matrixB = "sample_matrices/B20"
job = JobController.create(matrixA, matrixB)
# job = JobController.create(matrixA, matrixB)
# job = JobController.create(matrixA, matrixB)
