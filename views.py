import sqlite3
from functools import wraps
from flask import Flask,render_template,request,url_for,g,redirect,session,flash
#configuration is setup 
app=Flask(__name__)	
app.config.from_object('_config')
#connecting to database
def connect_db():
	return sqlite3.connect(app.config['DATABASE_PATH'])
def login_required(test):
	@wraps(test)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return test(*args,**kwargs)
		else:
			flash('you are not logged in.Please login to continue')
			return redirect(url_for('login'))
		return wrap
@app.route('/logout')
def logout():
	sessions.pop('logged_in',none)
	flash('Good Bye..')
	return redirect(url_for('login'))
@app.route('/',methods=['POST','GET'])
def login():
	
	if request.method=='POST':
		
	    if request.form['username']!=app.config['USERNAME'] or request.form['password']!=app.config['PASSWORD']:
	    	error='INVALID CREDENTIALS. Please try again.'
	    	return render_template('login.html',error=error)
	    else:
	    	session['logged_in']=True
	    	flash('Welcome to Tasks Manager')
	    	return redirect(url_for('tasks'))
	return render_template('login.html')
	






