

def sign_up(Fname, Lname, age, Email, Password, OrgName):
	DB = make_connection()
	cur = DB.cursor()

	cur.execute("SELECT * Email")

	for i in row:
		if Email == i:
			return "Email already exists"
			exit()

	Hpassword = hash(Password)

	cur.execute(f"INSERT INTO People VALUE({ID},{Fname},{Lname},{age})")
	cur.execute(f"INSERT INTO Password VALUE({ID},{Hpassword})")

	DB.commit()
	cur.close()
	DB.close()
	return 200
	


