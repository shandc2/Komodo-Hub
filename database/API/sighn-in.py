import hashlib
import mysql.connector

def Sighn-in(Email, password):

	hashedPW = hash(password)
	
	DB = make_connection()
	cur =DB.cursor()
	cur.execute("SELECT Password WHERE Email =", Email")
	
	if row[0] == hashedPW:
	//password matches
	else:
	//password dosent match
