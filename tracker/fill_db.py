#!venv/bin/python
"""fill_db.py - Fill the database.

This script fills the database with dummy data, which makes it easier to test
the system.

"""
from app import db
from app.models import *

#Main account
admin = Account('root', 'n3tb0t')
db.session.add(admin)
db.session.commit()

peer1 = Peer('77.249.206.212')
db.session.add(peer1)
db.session.commit()

matrixA = "sample_matrices/TestA"
matrixB = "sample_matrices/TestB"

mA = MatrixController.createFromFile(matrixA)
mB = MatrixController.createFromFile(matrixB)

job = JobController.create(mA, mB)
job = JobController.create(mA, mB)
job = JobController.create(mA, mB)
