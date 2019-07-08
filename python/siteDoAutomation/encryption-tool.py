import base64
import os
import pprint
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass

keyfile="./keyfile2.txt"

def genkey():
	global keyfile
	key = Fernet.generate_key()
	print(key)
	writefile(key)
	
def genkey2(passphrase):
	print("=============================")
	print("Pass phrase is: " + passphrase )
	salt = os.urandom(16)
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
		)
	key = base64.urlsafe_b64encode(kdf.derive(passphrase))
	print ("KEY::")
	print(key)
	
	f = Fernet(key)
	
	print("Entered plain password: letmein")
	enc_pass = f.encrypt(b"letmein")
	print("Encrypted password is: " + enc_pass )
	dec_pass=f.decrypt(enc_pass)
	print("Decrypted password is: " + dec_pass )
	print("=============================")

	
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
		#print("Token secret key is:" + out)
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

ans = raw_input("Do you want to generate new key?\n")

if ans == "yes" :
	print("Generate new key...")
	genkey()
else:
	print("Skip task")

print("Your token key is located at " + keyfile )

#password = raw_input("Enter password\n")
password = getpass.getpass("Enter your password: ")


if password != "" :
	print(readfile(keyfile))
	enc = encrypt(password)
	print("Encrypted password: " + enc )
	dec = decrypt(enc)
	stars = dec[1:-1]
	dec = dec[0:1] + ( "*" * len(stars)) + dec[-1:]
	print("Decrypted password: " + dec)
else:
	print("No password entered, skip")
