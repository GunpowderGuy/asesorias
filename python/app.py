from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Temporary storage (dictionary) for users and sessions
users = {}
sessions = {}

# Valid university email regex (e.g., emails ending with @edu.pe)
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
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        # Check if the role is tutor and validate university email
        if role == 'tutor' and not re.match(UNIVERSITY_EMAIL_REGEX, email):
            return "Tutors must register with a university email (e.g., @edu.pe)."
        
        users[email] = {'password': password, 'role': role}
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    user_sessions = sessions.get(user, [])
    return render_template('dashboard.html', user=user, sessions=user_sessions)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject = request.form['subject']
        city = request.form['city']
        
        tutors = [{'name': 'Juan Pérez', 'subject': 'Matemáticas', 'city': 'Lima', 'email': 'juan@edu.pe'},
                  {'name': 'María González', 'subject': 'Física', 'city': 'Arequipa', 'email': 'maria@edu.pe'}]
        matching_tutors = [t for t in tutors if t['subject'] == subject and t['city'] == city]
        return render_template('search.html', tutors=matching_tutors)
    return render_template('search.html', tutors=[])

@app.route('/schedule/<tutor_email>', methods=['POST'])
def schedule(tutor_email):
    if 'user' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    
    student_email = session['user']
    subject = request.form['subject']
    date = request.form['date']
    
    if tutor_email not in sessions:
        sessions[tutor_email] = []
    sessions[tutor_email].append({'student': student_email, 'subject': subject, 'date': date})
    
    if student_email not in sessions:
        sessions[student_email] = []
    sessions[student_email].append({'tutor': tutor_email, 'subject': subject, 'date': date})
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

