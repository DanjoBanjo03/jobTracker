from flask import Flask, render_template, redirect, url_for, request
from jobTracker.models import db, JobApplication
from jobTracker.forms import JobForm
from datetime import date
import os

app = Flask(__name__)
# Use absolute path to ensure database is created in project directory
basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, "instance")
os.makedirs(instance_dir, exist_ok=True)  # Create instance directory if it doesn't exist
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_dir, "jobs.db")}'
app.config['SECRET_KEY'] = 'magic-key'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.context_processor
def inject_job_count():
    """Make job count available to all templates"""
    total_jobs = JobApplication.query.count()
    return dict(total_jobs=total_jobs)

@app.route('/')
def index():
    q = request.args.get('q','')
    sort = request.args.get('sort', 'date_desc')

    # Base query
    query = JobApplication.query

    # Apply search filter if provided
    if q:
        query = query.filter(JobApplication.company.ilike(f'%{q}%'))

    # Apply sorting
    if sort == 'date_asc':
        query = query.order_by(JobApplication.date_applied.asc())
    elif sort == 'company':
        query = query.order_by(JobApplication.company.asc())
    elif sort == 'status':
        query = query.order_by(JobApplication.status.asc())
    else:  # default to date_desc
        query = query.order_by(JobApplication.date_applied.desc())

    apps = query.all()
    return render_template('index.html', apps=apps, q=q, sort=sort)

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