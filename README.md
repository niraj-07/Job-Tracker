**Job Application Tracker**
A simple web app for managing your job applications. I originally built this to track my own internship applications instead of using messy spreadsheets.


**Live Demo:** [Link to your deployed application]

**Features**
**User Accounts:** Secure registration and login to keep your list private.

**Manage Applications:** Add, view, edit, and delete your job entries.

**Simple Dashboard:** See all your applications in a clean, organized table.

**Tech Stack**
Backend: Python, Flask, SQLAlchemy

Frontend: HTML, Bootstrap 5

**Running Locally**
To run this project on your own machine:

Clone the repository and set up the environment:

git clone https://github.com/niraj-07/Job-Tracker.git
cd Job_Tracker
python -m venv venv
Windows:source venv/Scripts/activate  
macOS/Linux: source venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Create the database and run the app:

Start the Python interpreter:
python
Run these commands:
from app import app, db
with app.app_context():
    db.create_all()
exit()

Launch the application:

flask run

The app will be running at http://127.0.0.1:5000.
