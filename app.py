from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from projects.job_tracker.models import db, JobApplication
from projects.job_tracker.forms import JobForm
from datetime import date
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
db = SQLAlchemy(app)

@app.route('/')
def index():
    q = request.args.get('q','')
    if q:
        apps = JobApplication.query.filter(
            JobApplication.company.ilike(f'%{q}%')
        ).all()
    else:
        apps = JobApplication.query.order_by(JobApplication.date_applied.desc()).all()
    return render_template('index.html', apps=apps, q=q)

@app.route('/add', methods=['GET','POST'])
def add():
    form = JobForm()
    if form.validate_on_submit():
        job = JobApplication(
            company=form.company.data,
            position=form.position.data,
            date_applied=form.date_applied.data,
            status=form.status.data,
            notes=form.notes.data,
            link=form.link.data
        )
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', form=form, action='Add')

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    job = JobApplication.query.get_or_404(id)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.populate_obj(job)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', form=form, action='Edit')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    job = JobApplication.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)