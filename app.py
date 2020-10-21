from flask import Flask, render_template, url_for, request, session, redirect, g
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xb3h4\xacmR7!F\xa7\xcc\x00\x04Jh b\xd3\xb55\xa2\xf1f\x02'

@app.teardown_appcontext
def close_db(error):

    if hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur.close()

    if hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn.close()

def get_current_session_user():

    user_result = None

    if 'user' in session:
        user = session['user']

        db = get_db()
        db.execute('SELECT id, username, password, admin FROM users WHERE username = %s', (user, ))
        user_result = db.fetchone()
    
    return user_result

@app.route('/')
def index():

    user = get_current_session_user()


    return render_template('index.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():

    user = get_current_session_user()

    if request.method == 'POST':

        db = get_db()
        
        # Check for existing user
        db.execute('SELECT id FROM users WHERE username = %s', (request.form['username'], ))
        existing_user = db.fetchone()

        # If existing user exists return to register page with error message
        if existing_user:
            return render_template('register.html', user=user, error='Username is already taken!')
        
        # If user doesn't exist

        hashed_password = generate_password_hash(request.form['password'], 'sha256')
        db.execute('INSERT INTO users(username, password, admin) VALUES(%s, %s, %s)', (request.form['username'], hashed_password, '0'))

        session['user'] = request.form['username']

        return redirect(url_for('index'))

    return render_template('register.html', user=user)



@app.route('/login', methods=['GET', 'POST'])
def login():

    user = get_current_session_user()

    error = None

    if request.method == 'POST':

        db = get_db()
        
        username = request.form['username']
        password = request.form['password']

        db.execute('SELECT id, username, password FROM users WHERE username = %s', (username, ))
        user_result = db.fetchone()

        if user_result and check_password_hash(user_result['password'], password):
            session['user'] = user_result['username']
            return redirect(url_for('index'))
        
        error = 'Username or password is wrong!'

    return render_template('login.html', user=user, error=error)

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect(url_for('index'))