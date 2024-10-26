from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Temporary storage (dictionary) for users and sessions
users = {}
sessions = {}

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
            return redirect(url_for('dashboard'))
        return "Invalid credentials, try again!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
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
        # In a real app, you'd query the database here.
        tutors = [{'name': 'Juan Pérez', 'subject': 'Matemáticas', 'city': 'Lima'},
                  {'name': 'María González', 'subject': 'Física', 'city': 'Arequipa'}]
        matching_tutors = [t for t in tutors if t['subject'] == subject and t['city'] == city]
        return render_template('search.html', tutors=matching_tutors)
    return render_template('search.html', tutors=[])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
