from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# Firefox options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# Fernet encryption 
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pprint import pprint
# request headers
import requests
import time
import datetime
import os
import logging
# regular expression
import re
import json

# siteDo is simple one page Python Selenium class to perform "Do" most of the browser's tasks
# This project is not to replace test frameworks such as cucumber and other test tools.
# As most of the operation tasks are short-lived and and requires rapid changes, 
# I created this siteDo class to deal with repetitive automation tasks for day to day activities.
# The purpose for this was to make changes easier and quicker without involving enormous coding efforts.
# @Author: nzvincent@gmail.com | Vincent Pang
#
# Features:
# - Firefox browser
# - Take screenshots
# - Assertion test
# - Proxy configuration
# - Multi level colour coded logging
# - Cookie modification
# - Execute custom Javascript
# ToDo wish list:
# - Reports 
# - Headers add / delete / edit
# - Content add / delete / edit
# - Password encryption
# - Multiple tabs and windows
# - Other browsers support
# References:
# - Assert https://selenium-python.readthedocs.io/getting-started.html
# - Cookie https://selenium-python-zh.readthedocs.io/en/latest/api.html
# - Color code https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
# - Windows installation https://www.liquidweb.com/kb/install-pip-windows/
# - Specifications: https://selenium-python.readthedocs.io/api.html

class siteDo:

	# Switch log level
	__log_level="DEBUG"
	
	# Turn screenshot on / off 
	screenshot="True"
	
	# Turn on / off console output
	showloginconsole="True"
	
	# Export your siteDoKey environment variable or add to your ~/.bashrc script
	# Add Export siteDoKey="your-secret-key"
	try:
		__decryption_key = os.environ['siteDoKey']
	except:
		print("Error!!! Please export siteDoKey to your OS environment variable")
		exit()

	# File location
	# Please ensure Python can write files to this folder 
	__logFile="logfile.txt"
	__reportFile="report.html"
	__cookieFile="__cookieFile.txt"
	__jsFile="./js-injection.js"
	__screenshot_path="./screenshots"

	# Increment number of label
	__step = 0
	
	# Default label name
	__static_label = "Step one" # use obj.label("New step name") to modify __static_label

	proxy="False"
	proxyhost="myproxy"
	proxyport=3128

	profile = webdriver.FirefoxProfile()
	# Browser manual proxy setting
	profile.set_preference("network.proxy.type", 1);
	profile.set_preference("network.proxy.http", proxyhost);
	profile.set_preference("network.proxy.http_port",  proxyport);
	profile.set_preference("network.proxy.ftp", proxyhost);
	profile.set_preference("network.proxy.ftp_port",  proxyport);
	profile.set_preference("network.proxy.ssl", proxyhost);
	profile.set_preference("network.proxy.ssl_port",  proxyport);
	profile.set_preference("network.proxy.socks", proxyhost );
	profile.set_preference("network.proxy.socks_port",  proxyport);
	
	profile = ""
	
	# Firefox headless
	options = FirefoxOptions()
	options.add_argument("--headless")
	
	option = ""
	
  
	if __log_level == "INFO":
		logging.basicConfig(filename=__logFile, filemode='w', level=logging.INFO )
	elif __log_level == "DEBUG":
		logging.basicConfig(filename=__logFile, filemode='w', level=logging.DEBUG )
	elif __log_level == "WARNING":
		logging.basicConfig(filename=__logFile, filemode='w', level=logging.WARNING )
	elif __log_level == "CRITICAL":	
		logging.basicConfig(filename=__logFile, filemode='w', level=logging.ERROR )	
	elif __log_level == "ERROR":
		logging.basicConfig(filename=__logFile, filemode='w', level=logging.ERROR )	
	else:
		logging.basicConfig(filename=__logFile, filemode='w')
		
		
		
	# Constructor
	def __init__(self):
		#self.ff = webdriver.Firefox(profile ) if self.proxy == "True" else webdriver.Firefox()
		self.ff = webdriver.Firefox( self.profile , options=self.options ) if self.proxy == "True" else webdriver.Firefox(options=options)
		self.log(vars(siteDo.profile), "DEBUG")

	# Find , Add , delete and delete all cookies
	# aciton = VIEW|ADD|DELETE|DELETE_ALL_COOKIES
	# https://selenium-python-zh.readthedocs.io/en/latest/api.html
	def __findCookie(self, cookieName, action="none", find="none", replace="none"):
		# ToDo... use regex
		cookies_list = self.ff.get_cookies()
		cookies_dict = {}
		for cookie in cookies_list:
			cookies_dict[cookie['name']] = cookie['value']
			self.log( "Site cookie: [" + cookie['name'] + "=" + cookie['value'] + " ]" , "DEBUG" )

		found_cookie = cookies_dict.get(cookieName)
		
		if action == "ADD" :
			cookieValue = find
			cookie = {'name' : cookieName , 'value' : cookieValue }
			self.ff.add_cookie(cookie)
			self.log( "Added cookie: [ " +  cookieName + "=" + cookieValue + " ]" , "INFO" )
		
		if not found_cookie:
			self.log("Cookie not found: [ " + cookieName + " ]", "WARNING" ) 
		  	# siteTest.close()
		else:
			#self.log("Original cookie: " + cookieName + "=" + found_cookie )
			self.writeCookie( "Found search cookie: [ " +  cookieName + "=" + found_cookie + " ]" )
			if action == "EDIT" :
				# Modify cookie with regular expression
				# eg. re.sub("\sPok.*\s", " new_hostname ", str )
				# self.log( "String substitution: " + find +":"+ replace +":"+  found_cookie )
				#newCookie = re.sub( find , replace , found_cookie )
				newCookie =  self.replace( find , replace , found_cookie )
				cookie = {'name' : cookieName , 'value' : newCookie }
				self.ff.add_cookie(cookie)
				self.log( "Modified cookie: [ " +  cookieName + "=" + newCookie + " ]" , "INFO" )
			if action == "DELETE" :
				self.ff.delete_cookie(cookieName)
				self.log( "Deleted cookie: [ " +  cookieName + " ]" , "INFO" )
			elif action == "DELETE_ALL_COOKIES" :
				self.ff.delete_all_cookies()


	def writeCookie(self, cookie = "none" ):
		self.log("writeCookie() Method: [" + cookie + " ] to file [ " + self.__cookieFile + " ]", "DEBUG" )
		try:
			fp = open( self.__cookieFile, 'a+')
			fp.write(cookie + "\n")
			fp.close() 
		except IOError:
			self.log("Could not write to cookie file :" + self.__cookieFile , "CRITICAL")

	def takescreenshot(self): 
		if ( self.screenshot == "True" ):
			# Delay 3 seconds before taking screenshot
			# Note: If function takes less than 3 seconds to write image file to I/O
			time.sleep(3)
			ts = time.time()
			fileName = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S') + ".png"
			saveFile = self.__screenshot_path + "/" + fileName 
			self.ff.save_screenshot(saveFile) 
			self.log("Save screenshot to [ " + fileName + " ]", "DEBUG" )
		
	def label(self, label_name="Default Label"):
		self.__step = self.__step + 1
		self.log("Label() Method: ["  + label_name + " ]", "DEBUG")
		CSTART = '\033[101m'
		CEND = '\033[0m'
		print(CSTART + "[ LABEL ]" + CEND  + " (#"  + str(self.__step) + ") " + label_name )
		try:
			fp = open( self.__logFile, 'a+')
			fp.write("[ LABEL ]"  + " (#"  + str(self.__step) + ") " +  label_name + "\n")
			fp.close()
		except IOError:
			self.log("Could not write to logfile :" + self.__logFile , "CRITICAL")
	
	def close(self):
		try:
			self.log("Close() Method ", "DEBUG" )
			self.ff.close()
		except:
			self.log("Close() Method unknown exception", "ERROR" )

	def history(self, steps ):
		try:
			self.log("History() Method " + steps , "DEBUG" )
			self.ff.execute_script("window.history.go(" + str(steps) + ")")
		except:
			self.log("History() Method unknown exception", "ERROR")
			
	def javascript(self, script ):
		try:
			self.log("Execute javascript " + script , "INFO" )
			self.ff.execute_script(script)
		except:
			self.log("Javascript() Method unknown exception", "ERROR")

	def size_position(self, width="200", height="200", xpos="0", ypos="0"):
		try:
			self.log("Execute Size_position() Method [ " + width + " , " + height + " , " + xpos + " , " +  ypos + " ]", "INFO" )
			self.ff.set_window_size( width , height)
			self.ff.set_window_position(xpos , xpos)
		except:
			self.log("Size_position() Method unknown exception", "ERROR")
			
	def wait(self, second):
		try:
			self.log("Wait() Method [ " + str(second) + " ] ", "INFO" )
			time.sleep(second)
		except:
			self.log("Wait() Method ) Method unknown exception", "ERROR")
			

	# key value pair search, use find()
	# content/xpath search , use lookup()
	def find(self, type="CONTENT" , action="VIEW", search_key="none", replace_word="none", search_value="none" ):
		self.log("Find() Method: [ " + type + " , " + action + " , " + search_key + " , " + replace_word + "," + search_value + " ]" , "INFO")
		try:
			if type == "COOKIE" :
				cookieName = search_key
				if action == "VIEW":
					self.__findCookie( search_key )
				elif action == "EDIT" :
					find = search_value
					# __findCookie(self, cookieName, action="none", find="none", replace="none"):
					self.__findCookie( cookieName , "EDIT", find , replace_word )
				elif action == "ADD" :
					cookieValue=replace_word
					self.__findCookie( cookieName , "ADD", cookieValue )
				elif action == "DELETE" or  action == "DELETE_ALL_COOKIES" :
					self.__findCookie( cookieName , action )
			elif type == "HEADER" :
				self.log("header")
				# find http header
			else:
				self.log("nothing")
		except NoSuchElementException:
			self.log("No able to find " + keyword + " in " + type , "CRITICAL" )

	# String substitution with regular expression support
	#eg.  replace( "\:.*\.com\s" , ": my-website.com", "server name is : example.com" )
	def replace(self, replace_with , find , input ):
		# ToDo.. implement error handling
		self.log("Replace String" , "DEBUG" )
		self.log("Input String : [ " + input + " ]" , "DEBUG" )
		self.log("Find String: [" + find + "]" , "DEBUG" )
		self.log("Replace with: [ " + replace_with + " ]" , "DEBUG" )
		newString = re.sub( find , replace_with , input )
		self.log("New replaced String: [ " + newString + " ]" , "DEBUG" )
		return newString	
	
	# cookie consists of key value pair
	#def check_cookie(self, keyword, content) :
	#	return re.search(keyword, content )
	def __re_search( self, keyword, content ):
		if re.search(keyword, content ):
			return keyword
		else:
			return False
		
	def log(self, input , level="INFO") :
		ts = time.time()
		logtime = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
		msg = '[' + level + '] ' + logtime + ' - ' + json.dumps(input)
		CSTART = '\033[0m'
		if level == "DEBUG":
			CSTART = '\033[32m'
			logging.debug(msg)
		elif level == "INFO":
			CSTART = '\033[40m'
			logging.info(msg)
		elif level == "WARNING":
			CSTART = '\033[33m'
			logging.warn(msg)   
		elif level == "ERROR":
			CSTART = '\033[6m'
			logging.error(msg)
		elif level == "CRITICAL":
			CSTART = '\033[101m'
			logging.critical(msg)
		else:
			logging(msg)
		if self.showloginconsole == "True" :
			CEND = '\033[0m'
			print(CSTART + msg + CEND )
	
	# Test console output colours
	def testColor(self):
		self.log("INFO","INFO")
		self.log("DEBUG","DEBUG")
		self.log("WARNING","WARNING")
		self.log("CRITICAL","CRITICAL")
		self.log("ERROR","ERROR")
		self.log("EMPTY")
			
	def do(self, action , xpath="none", input="none" ):
		# Handle ENCRYPTED CONTENT
		INPUT=input
		if input.startswith('ENC_PASS:') :
			INPUT="*******"
			input = self.decrypt(input)
			
		self.log("Do() Method: LABEL: [ " + self.__static_label + " ] PARAMETERS: [ '" + action + " ',' " + xpath  + " ',' " + INPUT + "']", "INFO")		
		
		try:
			if action == "goto" or action == "go" :
				url = xpath
				self.ff.get(url)
			elif action == "form" :
				self.ff.find_element_by_xpath(xpath).send_keys(input)		
			elif action == "click" :
				self.ff.find_element_by_xpath(xpath).click()	
			elif action == "link" or action == "text_link" or action == "hyperlink_text" :
				link_text = xpath
				self.ff.find_element_by_link_text(link_text).click()	
			elif action == "return" :
				self.ff.find_element_by_xpath(xpath).send_keys(Keys.RETURN)
			else :
				self.log("No action parsed to do function", "WARNING")
		except NoSuchElementException:
			self.log("NoSuchElementException exception caught in do function", "WARNING" )
		self.takescreenshot()
		self.log("Current url [ " + self.ff.current_url + " ] ", "INFO")

		
	# type SOURCE|XPATH|??? IN|NOT_IN or NOTIN
	def lookup(self,  search_keyword, condition="IN" , type="SOURCE" , xpath="" ):
		self.log("Current URL: " + self.ff.current_url , "DEBUG")
		if type == "SOURCE":
			try:
				content = self.ff.page_source
			except:
				content = ""
				self.log("Cannot find page source", "WARNING" )
				#self.log("Status code [ " + self.ff.status + " ] ", "WARNING" )
		elif type == "XPATH":
			try:
				content = self.ff.find_element_by_xpath(xpath).text
			except:
				content = ""
				self.status(self.ff.current_url)
				self.log("Invalid xpath or cannot find elements [ " + xpath + " ] ", "WARNING" )
				
		if condition == "IN":
			if search_keyword in content:
				self.log("[TRUE] " + search_keyword + " in " + type , "INFO")
				return True
			else:
				self.log("[FALSE] " + search_keyword + "  in " + type , "WARNING")
				return False
		elif condition == "NOT_IN" or condition == "NOTIN" :
			if search_keyword not in content:
				self.log("[TRUE] " + search_keyword + " not in "  + type, "INFO")
				return "OK"
			else:
				self.log("[FALSE] " + search_keyword + " not in "  + type, "WARNING")
				return False

	# Selenium lack of request and response headers support
	# This function requires requests library.
	# Another sophisticate way is to use HAR such as Chrome browser to 
	def status(self, url ):
		self.log("Request url [ " + url + " ]", "INFO")
		try:
			r = requests.head(url)
			self.log("Request response status [ " + str(r) + " ]", "INFO")
		except:
			self.log("HTTP request status unknown exception", "ERROR")
			
	def encrypt(self, password):
		try:
			f = Fernet(self.__decryption_key)
			return "ENC_PASS:" + f.encrypt(password)
		except:
			self.log("Encryption caught exception [ " + self.__decryption_key + " , ******  ]", "CRITICAL")
			return False
	
	def decrypt(self, enc_password ):
		enc_password=enc_password[8:]
		try:
			f = Fernet(self.__decryption_key)
			return f.decrypt(enc_password)
		except:
			self.log("Decryption caught exception [ " + self.__decryption_key + " , " + str(enc_password) + "]", "CRITICAL")
			return False


COMMENT="""		

########################################################
#     TO RUN HERE OR RUN FROM ANOTHER PYTHON SCRIPT    #
########################################################
# If to run from another script, add the following line at the beginning
# from siteDo import siteDo

surf = siteDo()

surf.label("Test console output colour")
surf.testColor()
surf.size_position("500","1080")

surf.label("Visit Ebay website")
surf.do('goto','https://www.ebay.com')

surf.label("Display Ebay website status")
surf.status('https://www.ebay.com')

surf.label("Go to Google website")
surf.do('goto','https://www.google.com')

surf.label("Back to Ebay website")
surf.do('goto','https://www.ebay.com')

surf.label("Find cookie on eBay website and modify")
surf.find('COOKIE', 'EDIT', 'ebay' , 'CHANGED_JS' ,'js')

surf.label("Delete a cookie on eBay website")
surf.find('COOKIE', 'DELETE', 'ebay' )

surf.label("Delete all cookies on eBay website")
surf.find('COOKIE', 'DELETE_ALL_COOKIES' )

surf.label("View cookie name ebay")
surf.find('COOKIE', 'VIEW', 'ebay')

surf.label("Go to Trademe website")
surf.do('goto','https://www.trademe.co.nz')

surf.label("Assertion test Ebay website")
surf.lookup("fashion" , "IN", "SOURCE" )
surf.lookup("xfashion" , "NOT_IN", "SOURCE" )
surf.lookup('eBay' , 'IN', 'XPATH' , '//*[@id="destinations_list1"]/div/div/div/h2' )

surf.label("Assertion test using invalid xpath")
surf.lookup('eBay' , 'IN', 'XPATH' , '//*[@id="destinations_list1"]/div/div/div3/h2' )

surf.label("Execute javascript on eBay website")
surf.javascript("alert('You can also inject javascript!!!');")

surf.label("Tearing down")
surf.wait(4)
surf.close()

"""



