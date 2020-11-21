from flask import Flask, render_template, url_for, request, session, redirect, g
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from short_url import encode
import re


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xb3h4\xacmR7!F\xa7\xcc\x00\x04Jh b\xd3\xb55\xa2\xf1f\x02'

@app.teardown_appcontext
def close_db(error):

	if hasattr(g, 'postgres_db_cur'):
		g.sqlite_db.close()

def get_current_session_user():

	user_result = None

	if 'user' in session:
		user = session['user']

		db = get_db()
		user_cur = db.execute('SELECT id, username, password, admin FROM users WHERE username = ?', [user])
		user_result = user_cur.fetchone()
	
	return user_result


# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('404.html'), 404

@app.route('/<short_url>')
def redirect_short_url(short_url):

	db = get_db()


	long_url_cur = db.execute('SELECT long_url FROM urls WHERE short_url = ?', [short_url])
	long_url = long_url_cur.fetchone()

	if long_url:
		return render_template('redirect.html', long_url=long_url)
	else:
		return 'URL not found'

@app.route('/', methods=['GET', 'POST'])
def index():

	user = get_current_session_user()
	db = get_db()
	error = None
	user_urls = None
	base_url = request.base_url

	if user:

		if request.method == 'POST':

			long_url =request.form['long-url']
			url_name = request.form['url-name']
			custom_url = request.form['custom-url']

			if long_url == '':

				error = 'Please enter URL before submitting!'

			else:

				# Check if long url is already used by this user
				url_cur = db.execute('SELECT url_name FROM urls WHERE long_url = ? AND user_id = ?', [request.form['long-url'], user['id']])
				if (url_cur.fetchone()):

					error = 'You\'ve already shorten this URL!'

				elif not check_valid_url(long_url):

					error = 'URL you\'ve entered is not valid!'

				# Check if user have entered custom_url
				elif custom_url != '':
					
					if len(custom_url) < 3:
						
						error = 'Length of custom url must be at least 3 characters!'
					
					elif db.execute('SELECT id FROM urls WHERE short_url = ?', [custom_url]).fetchone():

						error = 'Your custom URL is already taken!'
					
					elif not error:
						
						if url_name == "":
							db.execute('INSERT INTO urls (long_url, short_url, user_id) values (?, ?, ?)', [long_url, custom_url, user['id']])
							db.commit()
						else:
							db.execute('INSERT INTO urls (long_url, short_url, user_id, url_name) values (?, ?, ?, ?)', [long_url, custom_url, user['id'], url_name])
							db.commit()

				else:

					short_url = encode(long_url)
					
					if url_name == "":
						db.execute('INSERT INTO urls (long_url, short_url, user_id) values (?, ?, ?)', [long_url, short_url, user['id']])
						db.commit()
					else:
						db.execute('INSERT INTO urls (long_url, short_url, user_id, url_name) values (?, ?, ?, ?)', [long_url, short_url, user['id'], url_name])
						db.commit()
						
		

		user_urls_cur = db.execute('SELECT url_name, id, long_url, short_url FROM urls WHERE user_id = ?', [user['id']])
		user_urls = user_urls_cur.fetchall()
	
	return render_template('index.html', user=user, urls=user_urls, error=error, base_url=base_url)

@app.route('/register', methods=['GET', 'POST'])
def register():

	user = get_current_session_user()

	if request.method == 'POST':

		db = get_db()
		
		# Check for existing user
		existing_user_cur = db.execute('SELECT id FROM users WHERE username = ?', [request.form['username']])
		existing_user = existing_user_cur.fetchone()

		# If existing user exists return to register page with error message
		if existing_user:
			return render_template('register.html', user=user, error='Username is already taken!')
		
		# If user doesn't exist
		hashed_password = generate_password_hash(request.form['password'], 'sha256')
		db.execute('INSERT INTO users(username, password, admin) VALUES (?, ?, ?)', [request.form['username'], hashed_password, '0'])
		db.commit()

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

		user_result_cur = db.execute('SELECT id, username, password FROM users WHERE username = ?', [username])
		user_result = user_result_cur.fetchone()

		if user_result and check_password_hash(user_result['password'], password):
			session['user'] = user_result['username']
			return redirect(url_for('index'))
		
		error = 'Username or password is wrong!'

	return render_template('login.html', user=user, error=error)

@app.route('/logout')
def logout():

	session.pop('user', None)

	return redirect(url_for('index'))

@app.route('/delete_entry/<url_id>')
def delete_entry(url_id):

	user = get_current_session_user()
	db = get_db()
	base_url = request.base_url

	print('----------------', url_id)
	db.execute('DELETE FROM urls WHERE id = ?', [url_id])
	db.commit()

	user_urls_cur = db.execute('''SELECT url_name,
					id, 
					long_url, 
					short_url 
					FROM urls WHERE user_id = ?''', [user['id']])
	user_urls = user_urls_cur.fetchall()
	
	return render_template('index.html', user=user, urls=user_urls, base_url=base_url)



def check_valid_url(url):
	regex = re.compile(
			r'^(?:http|ftp)s?://' # http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
			r'localhost|' #localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
			r'(?::\d+)?' # optional port
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	
	return re.match(regex, url) is not None