
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_tracker.db'
app.config['SECRET_KEY'] = 'a super secret key no one should guess'
db = SQLAlchemy(app)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    date_applied = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Applied')

    def __repr__(self):
        return f'<JobApplication {self.company_name} - {self.job_title}>'

@app.route('/')
def home():
    all_jobs = JobApplication.query.order_by(JobApplication.date_applied.desc()).all()

    return render_template('home.html', jobs=all_jobs)


@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
       


        company = request.form['company_name']
        title = request.form['job_title']
        date_str = request.form['date_applied']
        status = request.form['status']
        
      
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

       
        new_application = JobApplication(
            company_name=company,
            job_title=title,
            date_applied=date_obj,
            status=status
        )

 
        db.session.add(new_application)
        db.session.commit()

        flash('Job added successfully!', 'success')
        return redirect(url_for('home'))
    

    return render_template('add_job.html')

@app.route('/update/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    job_to_update = JobApplication.query.get_or_404(job_id)
    
    if request.method == 'POST':
        job_to_update.company_name = request.form['company_name']
        job_to_update.job_title = request.form['job_title']
        job_to_update.date_applied = datetime.strptime(request.form['date_applied'], '%Y-%m-%d').date()
        job_to_update.status = request.form['status']
        
       
        try:
            db.session.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('home'))
        except:
            return "There was an issue updating that job."
    else:
        return render_template('update_job.html', job=job_to_update)
    
@app.route('/delete/<int:job_id>')
def delete_job(job_id):
    job_to_delete = JobApplication.query.get_or_404(job_id)

    try:
        db.session.delete(job_to_delete)
        db.session.commit()
        flash('Job deleted successfully.', 'info')
        return redirect(url_for('home'))
    except:
        return "There was a problem deleting that job."