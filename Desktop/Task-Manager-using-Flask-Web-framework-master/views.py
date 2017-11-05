import sqlite3

from functools import wraps
from forms import AddTaskForm,RegisterForm,LoginForm
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
	session.pop('logged_in',None)
	flash('Good Bye..')
	return redirect(url_for('login'))
@app.route('/',methods=['POST','GET'])
def login():
	error=None
	form = LoginForm(request.form)
	if request.method=='POST':
		username=request.form['username']
		password=request.form['password']
		if not username or not password:
			flash('Invalid credentials')
			return redirect(url_for('login'))
		else:
			g.db=connect_db()
			for row in g.db.execute('select * from users where name=?',[username]):
				password1=row[3]
			
			

				if  password1==password:
					session['logged_in']=True
					flash('Welcome')
					return redirect(url_for('tasks'))
				else:
					error='Invalid Username or Password'

	return render_template('login.html',form=form,error=error)
		


@app.route('/tasks/')
@login_required
def tasks():
	g.db=connect_db()
	
	cursor=g.db.execute('select name,due_date,priority,task_id from tasks where status=1')
	
	open_tasks	= [
	dict(name=row[0], due_date=row[1], priority=row[2],
	task_id=row[3]) for row in cursor.fetchall()
	]
	cursor = g.db.execute(
	'select name, due_date, priority, task_id from tasks where status=0'
	)
	closed_tasks = [
	dict(name=row[0], due_date=row[1], priority=row[2],
	task_id=row[3]) for row in cursor.fetchall()
        ]
	return render_template('tasks.html',form=AddTaskForm(request.form),open_tasks=open_tasks,closed_tasks=closed_tasks)

@app.route('/add/',methods=['POST'])
@login_required
def new_task():
        
	g.db=connect_db()
	name=request.form['name']
	date=request.form['due_date']
	priority=request.form['priority']
	if not name or not date or not priority:
		flash('All Fields are required')
		return redirect(url_for('tasks'))
	else:
		g.db.execute('insert into tasks(name,due_date,priority,status) values(?,?,?,1)',[request.form['name'],request.form['due_date'],request.form['priority']])
		g.db.commit()
		g.db.close()
		flash('New Entry Successfully posted.Thanks.')
		return redirect(url_for('tasks'))
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	g.db=connect_db()
	g.db.execute(
        'update tasks set status = 0 where task_id='+str(task_id)
    )	
	g.db.commit()
	g.db.close()
	flash('The task was marked as complete.')
	return redirect(url_for('tasks'))
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    g.db = connect_db()
    g.db.execute(
        'insert into deleted_tasks select * from tasks where task_id='+str(task_id)
    )
    g.db.execute('delete from tasks where task_id='+str(task_id))
    g.db.commit()
    g.db.close()
    flash('The task was marked as complete.')
    return redirect(url_for('tasks'))

@app.route('/register/',methods=['GET','POST'])
def register():
	error=None
	form =RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			g.db=connect_db()
			g.db.execute('insert into users(name,email,password) values(?,?,?)',[request.form['name'],request.form['email'],request.form['password']])
			g.db.commit()
			g.db.close()
			flash('Thanks for registering. Please Login')
			return redirect(url_for('login'))
		else:
			flash('Please provide valid credentials')
	return render_template('register.html',form=form,error=error)
