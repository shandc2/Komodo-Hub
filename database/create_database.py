import mysql.connector

def makeDB():

	DB = CDB()
	f = open()
	cur = DB.cursor()
	cur.execute("CREATE DATABASE IF NOT EXISTS DB")
	if cur == None:
		f = open("../Db.sql")
		cur.execute(f.read())
		f.close()

makeDB()