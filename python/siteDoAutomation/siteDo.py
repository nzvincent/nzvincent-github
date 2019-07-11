from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
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

# siteDo is simple one page Python Selenium class to perform "Do" most of the browser's tasks.
# Purpose for this is to make modification of Selenium test cases simple.
# @Author: nzvincent@gmail.com | Vincent Pang

# siteDo class covers most of the basic browser features for my day to day operation work:
# - Automate Firefox browser tests
# - Easy customise test case. eg. to input data into form, use siteDo.do("form","XPATH","your user id")
# - Encryption - eg. o input password into form, use siteDo.do("form","XPATH","ENC_PASS:=enctypted_string=")
# - screenshots on / off
# - Assertion test. eg. Find specific text contains in HTML, use siteDo.lookup("find me string","IN","CONTENT")
# - Cookie modification. eg. siteDo.find("COOKIE", "EDIT", "JSSSIONS", "find-in-regular-expression-match","replacing world")
# - Proxy on / off
# - Colour coded logging
# - Execute custom Javascript
# - Reports 
# ToDo wish list:
# - Headers add / delete / edit
# - Content add / delete / edit
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
	
	# Use proxy 
	__proxy="False"
	
	# Firefox headless
	__headless="True"
	
	# Please ensure Python can write files to this folder 
	__logFile="logfile.txt"

	__cookieFile="cookieFile.txt"
	__jsFile="./js-injection.js"
	__screenshot_path="./screenshots"
	
	# Turn screenshot on / off 
	screenshot="True"
	# Set delay before taking screenshot
	screenshot_delay=5
	
	# wait for page element loaded
	waitPageLoaded="True"
	waitPageLoadedDelay=3
	# Accept ID only
	waitPageLoadeElement="footer"
	
	# Turn report on / off
	report="True"
	__reportFile="report.html"
	
	# Load Javascript before sceenshot
	loadJavascript="False"
	loadJavascriptFile="custom-javascript.js"
	
	# Turn on / off console output
	showloginconsole="True"
	
	# Export your siteDoKey environment variable or add to your ~/.bashrc script
	# Add Export siteDoKey="your-secret-key"
	try:
		__decryption_key = os.environ['siteDoKey']
	except:
		print("Error!!! Please export siteDoKey to your OS environment variable")
		exit()
	
	# Start time
	ts = time.time()
	__start_datetime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
	__start_year_month_day_path = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d/%H%M%S')
	
	# Increment number of label
	__step = 0
	
	# Measure Do() method page load time
	__DoPageLoadTime=0
	
	# Default label name
	__default_label = "Step one" # use obj.label("New step name") to modify __static_label
	
	proxyhost="myproxy"
	proxyport=3128
	
	profile = webdriver.FirefoxProfile()
	# Browser manual proxy setting
	if __proxy == "True" :
		profile.set_preference("network.proxy.type", 1);
		profile.set_preference("network.proxy.http", proxyhost);
		profile.set_preference("network.proxy.http_port",  proxyport);
		profile.set_preference("network.proxy.ftp", proxyhost);
		profile.set_preference("network.proxy.ftp_port",  proxyport);
		profile.set_preference("network.proxy.ssl", proxyhost);
		profile.set_preference("network.proxy.ssl_port",  proxyport);
		profile.set_preference("network.proxy.socks", proxyhost );
		profile.set_preference("network.proxy.socks_port",  proxyport);
	
	# Firefox headless
	options = FirefoxOptions()
	if __headless == "True" :
		options.add_argument("--headless")
		
	# Loading log level 
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
		self.ff = webdriver.Firefox( self.profile , options=self.options )
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
	
	
	def __writeToFile(self, content = "" , fileaname = "" ):
		self.log("__writeToFile Method: [" + content + " ] to file [ " + fileaname + " ]", "DEBUG" )
		try:
			fp = open( fileaname , 'a+')
			fp.write(content + "\n")
			fp.close() 
		except IOError:
			self.log("Could not write to content to file :" + fileaname , "CRITICAL")
	
	# take screenshot and produce HTML report
	# Parse string to extra to produce report
	def takescreenshot(self, extra=""): 
		if self.screenshot == "True" :
			ts = time.time()
			fileName = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S') + ".png"
			date_time = datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
			# Create new directory is it does not exist
			# fileDir = self.__screenshot_path + "/" + self.__start_datetime
			fileDir = self.__screenshot_path + "/" + self.__start_year_month_day_path
			writeToReportFile = fileDir + "/" + self.__reportFile
			try:
				os.stat(fileDir)
			except:
				os.makedirs(fileDir)
				#os.mkdir(fileDir)
			saveFile = fileDir + "/" + fileName
			self.ff.save_screenshot(saveFile)
			self.log("Save screenshot to [ " + fileName + " ]", "DEBUG" )
			
			if self.report == "True" :
				content = "<div style='display: table-row; width=95%'><div>" + date_time + "</div> \
				<div style='display: table-cell;'>" + self.__default_label + "</div> \
				<div style='display: table-cell;'> \
				<a href='" + fileName + "'><img src='" + fileName + "' style='width:200px; height:200px;'></a> \
				</div> \
				<div>" + str(self.__DoPageLoadTime) + " sec</div> \
				<div>" + str(extra) + "</div> \
				</div>"
				self.__writeToFile( content, writeToReportFile )
	
	
	def label(self, label_name="Default Label"):
		self.__step = self.__step + 1
		self.log("Label() Method: [ "  + label_name + " ]", "DEBUG")
		CSTART = '\033[101m'
		CEND = '\033[0m'
		print(CSTART + "[ LABEL ]" + CEND  + " (#"  + str(self.__step) + ") " + label_name )
		self.__default_label = label_name
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
                        if os.path.isfile(script) :
                                self.ff.execute_script(open(script).read())
                        else:
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
	
	# wait until page element loaded
	# use siteDo.waitPageLoadeElement to set the expect element ID
	def __waitPageLoaded(self):
		self.log("Wait for element to load! [ " + self.waitPageLoadeElement + " ]" ,"DEBUG")
		waitDelay = self.waitPageLoadedDelay
		start = time.time()
		try:
			# self.waitPageLoadedDelay
			waitElem = WebDriverWait( self.ff , waitDelay ).until(EC.presence_of_element_located((By.ID, self.waitPageLoadeElement )))
			self.log("Page is ready!","DEBUG")
		except TimeoutException:
			self.log("Loading took too much time or element not found!","WARNING")
		done = time.time()
		self.__DoPageLoadTime = done - start
		self.log("Page take " + str(self.__DoPageLoadTime) + " sec to load","INFO")
	
	def do(self, action , xpath="none", input="none" ):
		# Handle ENCRYPTED CONTENT
		INPUT=input
		if input.startswith('ENC_PASS:') :
			INPUT="*******"
			input = self.decrypt(input)
			
		self.log("Do() Method: LABEL: [ " + self.__default_label + " ] PARAMETERS: [ '" + action + " ',' " + xpath  + " ',' " + INPUT + "']", "INFO")		
		
		try:
			if action == "goto" or action == "go" :
				url = xpath
				self.ff.get(url)
			elif action == "form" or action == "input" :
				self.ff.find_element_by_xpath(xpath).send_keys(input)
			elif action == "click" :
				self.ff.find_element_by_xpath(xpath).click()	
			elif action == "click_id" :
				id = xpath
				self.ff.find_element_id(xpath).click()					
			elif action == "link" or action == "text_link" or action == "hyperlink_text" :
				link_text = xpath
				self.ff.find_element_by_link_text(link_text).click()	
			elif action == "partial_link" or action == "partial_link_text" or action == "partial_hyperlink_text" :
				link_text = xpath
				self.ff.find_element_by_partial_link_text(link_text).click()	
			elif action == "return" :
				self.ff.find_element_by_xpath(xpath).send_keys(Keys.RETURN)
			else :
				self.log("No action parsed to do function", "WARNING")
		except NoSuchElementException:
			self.log("NoSuchElementException exception caught in do function", "WARNING" )
	
		# wait for page element to be loaded
		if self.waitPageLoaded == "True" :
			self.__waitPageLoaded()
	
		# Load javascript before screeshot taken
		if self.loadJavascript == "True":
			if os.path.exists(self.loadJavascriptFile) :
				self.javascript(open(self.loadJavascriptFile).read())
			else:
				self.javascript(self.loadJavascriptFile)
		
		time.sleep(self.screenshot_delay)
		self.takescreenshot()
		self.log("Current url [ " + self.ff.current_url + " ] ", "INFO")
		
		
	# type SOURCE|XPATH|??? IN|NOT_IN or NOTIN
	def lookup(self,  search_keyword, condition="IN" , type="SOURCE" , xpath="" ):
		self.log("Current URL: " + self.ff.current_url , "DEBUG")
		if type == "SOURCE" :
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
				assert_status = "SUCCESS"
			else:
				self.log("[FALSE] " + search_keyword + "  in " + type , "WARNING")
				assert_status = "FAIL"
		elif condition == "NOT_IN" or condition == "NOTIN" :
			if search_keyword not in content:
				self.log("[TRUE] " + search_keyword + " not in "  + type, "INFO")
				assert_status = "SUCCESS"
			else:
				self.log("[FALSE] " + search_keyword + " not in "  + type, "WARNING")
				assert_status = "FAIL"
		if self.screenshot == "True" :
			# ToDO swap assertinreport self.__reportFile = 
			self.takescreenshot(assert_status)
				
				
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



