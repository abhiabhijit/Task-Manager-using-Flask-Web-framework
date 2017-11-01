import sqlite3
from _config import DATABASE_PATH
with sqlite3.connect(DATABASE_PATH) as connection:
	#first create object to execute sql commands 
	c=connection.cursor()
	c.execute("""create table tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		due_date TEXT NOT NULL,
		priority INTEGER NOT NULL,
		status INTEGER NOT NULL)
		""")
	c.execute("INSERT INTO tasks(name,due_date,priority,status) VALUES('checking insertion into db','01-11-2017',10,1)")
	


