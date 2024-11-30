from flask import Flask, render_template, request, redirect, url_for, session, flash
import re
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Temporary data storage
users = {}
sessions = {}

# University email regex for tutors
UNIVERSITY_EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@edu\.pe$"

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['user'] = email
            session['role'] = users[email]['role']
            return redirect(url_for('dashboard'))
        return "Invalid credentials, try again!"
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    role = request.args.get('role', None)  # Capture role from query parameter
    if request.method == 'POST':
        # Capture form data
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', None)

        # Ensure email, password, and role are provided
        if not email or not password or not role:
            flash('Email, password, and role are required.')
            return render_template('register.html', role=role)

        # Check if the email is already registered
        if email in users:
            flash('Email is already registered.')
            return render_template('register.html', role=role)

        if role == 'tutor':
            # Validate and capture tutor-specific fields
            courses = request.form.get('courses', '').strip()
            availability_day = request.form.get('availability_day', '').strip()
            availability_start = request.form.get('availability_start', '').strip()
            availability_end = request.form.get('availability_end', '').strip()

            if not courses or not availability_day or not availability_start or not availability_end:
                flash('All tutor fields are required.')
                return render_template('register.html', role=role)

            # Save tutor data
            users[email] = {
                'password': password,
                'role': role,
                'courses': courses.split(','),
                'availability': {
                    'day': availability_day,
                    'start_time': availability_start,
                    'end_time': availability_end,
                },
            }
        elif role == 'student':
            # Save student data
            users[email] = {
                'password': password,
                'role': role,
            }
        else:
            flash('Invalid role selected.')
            return render_template('register.html', role=role)

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html', role=role)





@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    today = datetime.now().date()
    user_sessions = sessions.get(user, [])

    upcoming_sessions = [
        s for s in user_sessions if s['day'] and s['start_time'] and s['end_time']
    ]
    past_sessions = []  # Adjust as necessary if you need to track past sessions by date

    return render_template('dashboard.html', user=user, upcoming_sessions=upcoming_sessions, past_sessions=past_sessions)



@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject = request.form['subject']
        city = request.form['city']

        # Initialize the tutors list based on registered users
        tutors = []
        for email, info in users.items():
            if info['role'] == 'tutor' and city == city and subject in info['courses']:
                tutors.append({
                    'name': email.split('@')[0].replace('.', ' ').title(),
                    'subject': subject,
                    'city': city,
                    'email': email,
                    'courses': info['courses'],
                    'availability': info['availability']
                })

        return render_template('search.html', tutors=tutors)
    return render_template('search.html', tutors=[])




@app.route('/schedule/<tutor_email>', methods=['POST'])
def schedule(tutor_email):
    if 'user' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))

    student_email = session['user']
    subject = request.form['subject']

    # Split day and time, adding checks
    date_time = request.form['date'].split(" ", 1)
    if len(date_time) < 2:
        return "Invalid date format. Please select a valid day and time range."

    day = date_time[0]  # e.g., "Lunes"
    time_range = date_time[1].split("-")

    # Check if start and end times are provided
    if len(time_range) < 2:
        return "Invalid time range. Please provide both start and end times."

    start_time = time_range[0].strip()
    end_time = time_range[1].strip()

    # Append session details
    if tutor_email not in sessions:
        sessions[tutor_email] = []
    sessions[tutor_email].append({'student': student_email, 'subject': subject, 'day': day, 'start_time': start_time, 'end_time': end_time})

    if student_email not in sessions:
        sessions[student_email] = []
    sessions[student_email].append({'tutor': tutor_email, 'subject': subject, 'day': day, 'start_time': start_time, 'end_time': end_time})

    return redirect(url_for('dashboard') + "?message=Session scheduled successfully")




@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

