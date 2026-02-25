import hashlib
import mysql.connector

def sign_in(Email, password):
    hashedPW = hash(password)
    
    DB = make_connection()
    cur =DB.cursor()
    cur.execute(f"SELECT Password WHERE Email ={Email}")
    
    if row[0] == hashedPW:
        password_match = True
    else:
        password_match = False
    
    return password_match
