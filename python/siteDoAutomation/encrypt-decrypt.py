from cryptography.fernet import Fernet

keyfile="./keyfile.txt"

def genkey():
	global keyfile
	key = Fernet.generate_key()
	print(key)
	writefile(key)
	
	
def writefile(key):
	global keyfile
	try:
		fp = open( keyfile , 'w+' )
		fp.write(key)
		fp.close() 
	except IOError:
		print("exception")
		#self.log("Could not write to cookie file :" + self.__cookieFile , "CRITICAL")

def readfile(key):
	global keyfile
	try:
		fp = open( keyfile , 'r' )
		out = fp.read()
		print("Token secret key is:" + out)
		fp.close() 
		return out
	except IOError:
		print("exception")
		return False
		

def encrypt(password):
	global keyfile
	key = readfile(keyfile)
	f = Fernet(key)
	return f.encrypt(password)
	
def decrypt(enc_password):
	global keyfile
	key = readfile(keyfile)
	f = Fernet(key)
	return f.decrypt(enc_password)
	

#genkey()

enc = encrypt("this-is-password")
print("Encrypted password: " + enc)

dec = decrypt(enc)
print("Decrypted password: " + dec)
