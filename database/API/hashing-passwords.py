import hashlib

def hash():
	HashedPassword = password + salt
	hashed = hashlib.sha256(password.encode)
	return HashedPassword.hexdigest()
