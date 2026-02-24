import mysql.connector

def make_connection():
	DB = mysql.connector.connect(
		host="127.0.0.1",
		port="3306",
		user="testuser",
		password="password",
		database = "DB"
	)
	return DB
