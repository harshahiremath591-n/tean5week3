from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------- USER ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))


# ---------------- ELECTRICIAN ----------------
class Electrician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    time = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- JOB ----------------
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    location = db.Column(db.String(100))
    deadline = db.Column(db.String(50))

    electrician_id = db.Column(db.Integer, db.ForeignKey('electrician.id'))
    electrician = db.relationship('Electrician')

    time = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- TASK ----------------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))

    status = db.Column(db.String(50))  # Pending/In Progress/Completed

    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    electrician_id = db.Column(db.Integer, db.ForeignKey('electrician.id'))

    job = db.relationship('Job')
    electrician = db.relationship('Electrician')

    time = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- MATERIAL ----------------
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    time = db.Column(db.DateTime, default=datetime.utcnow)