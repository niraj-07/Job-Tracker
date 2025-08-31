
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yo password kasaile guess garna sakdaina'
database_uri = os.environ.get('DATABASE_URL')
if not database_uri:
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    database_uri = 'sqlite:///' + os.path.join(instance_path, 'job_tracker.db')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable = False, unique= True)
    password_hash = db.Column(db.String(100), nullable= False)
    jobs = db.relationship('JobApplication', backref='applicant', lazy=True)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    date_applied = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Applied')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<JobApplication {self.company_name} - {self.job_title}>'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists.', 'warning')
            return redirect(url_for('register'))

        new_user = User(
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    all_jobs = JobApplication.query.filter_by(user_id=current_user.id).order_by(JobApplication.date_applied.desc()).all()
    return render_template('home.html', jobs=all_jobs)

@app.route('/add', methods=['GET', 'POST'])
@login_required
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
            status=status,
            applicant= current_user
        )

 
        db.session.add(new_application)
        db.session.commit()

        flash('Job added successfully!', 'success')
        return redirect(url_for('home'))
    

    return render_template('add_job.html')

@app.route('/update/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    job_to_update = JobApplication.query.get_or_404(job_id)
    if job_to_update.applicant != current_user:
        abort(403)
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
    if job_to_delete.applicant != current_user:
        abort(403)

    try:
        db.session.delete(job_to_delete)
        db.session.commit()
        flash('Job deleted successfully.', 'info')
        return redirect(url_for('home'))
    except:
        flash('There was a problem deleting that job.', 'danger')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)