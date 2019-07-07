from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pprint import pprint
import time
import datetime
import os
import logging
import re
import json

# SiteDo is simple one page Python Selenium script to Do most of the browser tasks
# @Author: nzvincent@gmail.com
# Features:
# - Firefox browser
# - Easy to run. Eg. python siteDo.py
# - Take screenshots
# - Proxy configuration
# - Logging
# To be completed:
# - Find/Add/delete/Edit content , header , cookie
# ToDo wish list:
# - Test assertion and reports 
# - Multiple windows

class siteDo:
    
	' Define constant variables '
	logFile="logfile.txt"
	reportFile="report.html"
	cookieFile="cookieFile.txt"
	jsFile="./js-injection.js"
	
	screenshot="True"
	# Make sure folder exists
	path="./screenshots"
	
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
    
	showloginconsole="True"

	#logging.basicConfig(filename=logFile, filemode='w', level=logging.INFO)
	logging.basicConfig(filename=logFile, filemode='w' )
	
	# Constructor
	def __init__(self):
		self.ff = webdriver.Firefox(profile) if self.proxy == "True" else webdriver.Firefox()
		self.log(vars(siteDo.profile), "DEBUG")

	
	# Find , Add , delete and delete all cookies
	# aciton = VIEW|ADD|DELETE|DELETE_ALL_COOKIES
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
			self.log( "Added cookie: [ " +  cookieName + "=" + cookieValue + " ]" , "DEBUG" )
		
		if not found_cookie:
			self.log("Cannot find cookie name [ " + cookieName + " ]", "WARNING" ) 
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
				self.log( "Modified cookie: [ " +  cookieName + "=" + newCookie + " ]" , "DEBUG" )
			if action == "DELETE" :
				self.ff.delete_cookie(cookieName)
			elif action == "DELETE_ALL_COOKIES" :
				self.ff.delete_all_cookies()

		
		## host_id = session_id[-12:]
		## print("Host cookie found:" + host_id )


		#if host_id in open( self.cookieFile).read():
		#    print("Host cookie exists: " + host_id + " close browser and skip warm up...")
		#    siteTest.closeMe()
		#else:
		#    print("Continue to warm up...")

		
	def writeCookie(self, cookie = "none" ):
		self.log("writeCookie() Method: [" + cookie + " ] to file [ " + self.cookieFile + " ]", "DEBUG" )	
		fp = open( self.cookieFile, 'a+')
		fp.write(cookie + "\n")
		fp.close() 

	def takescreenshot(self): 
		if ( self.screenshot == "True" ):
			# Delay 3 seconds before taking screenshot
			# Note: If function takes less than 3 seconds to write image file to I/O
			time.sleep(3)
			ts = time.time()
			fileName = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S') + ".png"
			saveFile = self.path + "/" + fileName 
			self.ff.save_screenshot(saveFile) 
			self.log("Save screenshot to [ " + fileName + " ]", "DEBUG" )
		
	def label(self, label_name="Default Label"):
		#self.log("Label() Method: ["  + label_name + " ]", "DEBUG")
		CSTART = '\033[101m'
		CEND = '\033[0m'
		print("[ LABEL ] " + CSTART + label_name + CEND )


	def close(self):
		self.log("Close() Method ", "DEBUG" )
		self.ff.close()

	def wait(self, second):
		self.log("Wait() Method [ " + str(second) + " ] ", "DEBUG" )
		time.sleep(second)
		
	# String substitution with regular expression support
	#eg.  replace( "\:.*\.com\s" , ": my-website.com", "server name is : example.com" )
	def replace(self, find , replace_with, input ):
		# ToDo.. implement error handling
		self.log( "Info - Input string: [ " + input + " ]" , "DEBUG" )
		self.log( "Info - Find: [" + find + "]" , "DEBUG" )
		self.log( "Info - Replace with: [ " + replace_with + " ]" , "DEBUG" )
		newString = re.sub( find , replace_with , input )
		return newString


	
	# Implemented cookie find
	def find(self, type="CONTENT" , action="VIEW", search_key="none", replace_word="none", search_value="none" ):
		self.log("Find() Method: [ " + type + " , " + action + " , " + search_key + " , " + replace_word + " ] " , "INFO")
		try:
			if type == "CONTENT" :
				# to find content
				self.log("content")
			elif type == "COOKIE" :
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
	

	# To modify content / header or cookie
	def modify(self, keyword , type="content" ):
		try:
			if type == "content" :
				# to find content
				self.log("content")
			elif type == "cookie" :
				self.log("cookie")
				self.findCookie(keyword)
			elif type == "header" :
				self.log("header")
				# find http header
			else:
				self.log("nothing")
			self.log("modify function inputs " + keyword + " in " + type )
		except NoSuchElementException:
			self.log("No able to modify " + keyword + " in " + type , "CRITICAL" )
	
	# to check content / header of cookie
	def __check (self, type="content", condition="contain", keyword="none" ):
		try:
			if type == "content" :
				self.log("check content")
				output = self.check_content(keyword, content )
			elif type == "cookie" :
				self.log("cookie")
				output = self.findCookie(keyword)
			elif type == "header" :
				self.log("header")
				# find http header
			else:
				self.log("nothing")
			self.log("modify function inputs " + keyword + " in " + type )	
		except NoSuchElementException:
			self.log("No able to modify " + keyword + " in " + type , "WARNING" )

	# return True when xpath element found 
	def check_element(self, xpath):		
		try:
			return self.ff.find_element_by_xpath(xpath)
			self.log("OK - Found element: " + xpath )
		except NoSuchElementException:
			self.log("Failed to find element: " + xpath , "WARNING" )
			return False
		
	def check_content(self, keyword, content) :
		return  re.search(keyword, content )
	
	# header consists of key value pair
	def check_header(self, keyword, content) :
		return re.search(keyword, content )
	
	# cookie consists of key value pair
	def check_cookie(self, keyword, content) :
		return re.search(keyword, content )
		
	def re_search( self, keyword, content ):
		return re.search(keyword, content )
		
	def history(self, steps ):
		self.log("Go history " + steps , "DEBUG" )
		self.ff.execute_script("window.history.go(" + str(steps) + ")")
	
	def javascript(self, script ):
		self.log("Execute javascript " + script , "DEBUG" )
		self.ff.execute_script(" + script + ")
	
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
		self.log("Do() Method: [ '" + action + " ',' " + xpath  + " ',' " + input + "']", "INFO")
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


#####################
#      TO RUN       #
#####################          
surf = siteDo()
surf.testColor()
surf.label("Start Ebay")
surf.do('goto','https://www.ebay.com')
surf.find('COOKIE', 'VIEW', 'ebay')
surf.find('COOKIE', 'EDIT', 'ebay' , 'CHANGED_JS' ,'js')
surf.label("DELETE ebay Cookie")
surf.find('COOKIE', 'DELETE', 'ebay' )
surf.wait(2)
surf.find('COOKIE', 'DELETE_ALL_COOKIES' )
surf.wait(2)
surf.find('COOKIE', 'VIEW', 'ebay')
surf.do('go','https://www.google.com')
surf.do('goto','https://www.ebay.com')
surf.find('COOKIE', 'VIEW', 'ebay')

#surf.do('go','https://www.google.com')
#surf.find('COOKIE', 'VIEW' , 'ABC' )
#surf.check_element('//*[@id="content-wrap"]/h1')
#surf.do('form','/html/body/div/div[3]/form/div[2]/div/div[1]/div/div[1]/input','testing 1234 34333')
#surf.screenshot="True"
#surf.do('return','/html/body/div/div[3]/form/div[2]/div/div[1]/div/div[1]/input')
#surf.history('-2')
surf.wait(2)
surf.close()

