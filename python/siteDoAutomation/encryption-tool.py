import base64
import os
import pprint
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass
import re

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

CSTART = '\033[33m'
CEND = '\033[0m'	
	
ans = raw_input(CSTART + "Do you want to generate new token key? \n Warning!! your existing key will be overridden\n YES or enter to skip\n" + CEND)

#if ans == "yes" :
if re.match('yes', ans , re.IGNORECASE):
	print("Generate new key...")
	genkey()
else:
	print("Skip generating token key.")

print("Your token key is located at " + keyfile )

#password = raw_input("Enter password\n")
password = getpass.getpass( CSTART + "Enter your password: " + CEND )


if password != "" :

	print(CSTART)
	print""" 
	########################################################################################
	#  Export the token key to your environment variable and keep it secure, do not lost it.
	#  eg. export siteDoKey=\"your-token-key\" or add this to your ~/.bashrc file
	#  Use encrypted password in your siteDo automation.
	#  eg. browser.siteDo('form','xpath', 'ENC_PASS:gAgAAAAABd...........HY2CDgUZl' )
	########################################################################################
	"""
	print(CEND)
	
	print(CSTART + "\nToken key: " + CEND + readfile(keyfile) )

	enc = encrypt(password)
	print(CSTART + "Encrypted password: " + CEND + "ENC_PASS:" + enc )
	dec = decrypt(enc)
	stars = dec[1:-1]
	dec = dec[0:1] + ( "*" * len(stars)) + dec[-1:]
	print( CSTART + "Decrypted password: " +CEND + dec + "\n")
else:
	print("\nNo password entered, skip")
