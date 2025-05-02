from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    date_applied = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    link = db.Column(db.String(255))