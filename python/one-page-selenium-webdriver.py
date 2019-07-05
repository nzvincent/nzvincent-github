from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pprint import pprint
import time
import datetime
import os
import logging
import re

# @Author: nzvincent@gmail.com
# A Simple Python one page script to run Selenium
# TODO.. add encrytion / logging / find / modify (for header / cookie / header ) 

class siteAuto:
    
	' Define constant variables '
	logFile="logfile.txt"
	cookieFile="cookieFile.txt"
	jsFile="./js-injection.js"
	
	screenshot="TRUE"
	# Make sure folder exists
	path="./screenshots"
	
	proxy="FALSE"
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
    
	showloginconsole="TRUE"
	logging.basicConfig(filename=logFile, filemode='w', level=logging.INFO)
	
	# Constructor
	def __init__(self):
		# Print profile on start
		self.log(vars(siteAuto.profile))
		# if no proxy, use:
		self.ff = webdriver.Firefox(profile) if self.proxy == "TRUE" else webdriver.Firefox()
	
		
	def findCookie(self, cookieName, action="none", find="none", replace="none"):
		# ToDo... use regex
		cookies_list = self.ff.get_cookies()
		cookies_dict = {}
		for cookie in cookies_list:
			cookies_dict[cookie['name']] = cookie['value']
			self.log( cookie['name'] + "=" + cookie['value'] )

		found_cookie = cookies_dict.get(cookieName)

		if not found_cookie:
			self.log("Cookie " + cookieName + " not found")
		  	# siteTest.close()
		else:
			self.log("Original cookie: " + cookieName + "=" + found_cookie )
			self.writeCookie( "Original cookie: " +  cookieName + "=" + found_cookie )
			if action == "EDIT" :
				# Modify cookie with regular expression
				# eg. re.sub("\sPok.*\s", " new_hostname ", str )
				self.log( "String substitution: " + find +":"+ replace +":"+  found_cookie )
				#newCookie = re.sub( find , replace , found_cookie )
				newCookie =  self.replace( find , replace , found_cookie )
				cookie = {'name' : cookieName , 'value' : newCookie }
				self.ff.add_cookie(cookie)
				self.writeCookie( "Modified cookie: " +  cookieName + "=" + newCookie )
				
		
		## host_id = session_id[-12:]
		## print("Host cookie found:" + host_id )


		#if host_id in open( self.cookieFile).read():
		#    print("Host cookie exists: " + host_id + " close browser and skip warm up...")
		#    siteTest.closeMe()
		#else:
		#    print("Continue to warm up...")

		
	def writeCookie(self, cookie = "none" ):
		self.log("Writting Cookie value " + cookie + " to " + self.cookieFile )	
		fp = open( self.cookieFile, 'a+')
		fp.write(cookie + "\n")
		fp.close() 

	def takescreenshot(self): 
		if ( self.screenshot == "TRUE" ):
			# Delay 3 seconds before taking screenshot
			# Note: If function takes less than 3 seconds to write image file to I/O		     
			time.sleep(3)
			ts = time.time()
			fileName = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S') + ".png"
			saveFile = self.path + "/" + fileName 
			self.ff.save_screenshot(saveFile) 
			self.log("screenshot taken " + fileName )
				
	def close(self):
		self.ff.close()
	
	# String substitution with regular expression support
	#eg.  replace( "\:.*\.com\s" , ": my-website.com", "server name is : example.com" )
	def replace(self, find , replace_with, input ):
		# ToDo.. implement error handling
		self.log( "Input string: " + input )
		self.log( "Find: " + find )
		self.log( "Replace with: " + replace_with )
		newString = re.sub( find , replace_with , input )
		return newString

			
		
	def wait(self, second):
		time.sleep(second)
		
	def find(self, keyword , type="content" ):
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
			self.log("find function inputs " + keyword + " in " + type )	
		except NoSuchElementException:
			self.log("No able to find " + keyword + " in " + type )	
	

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
			self.log("No able to modify " + keyword + " in " + type )		

	def log(self, msg , leval="INFO") :
		logging.info(msg)
		if self.showloginconsole == "TRUE" :
			pprint(msg)

	
	# to check content / header of cookie
	def check (self, type="content", condition="contain", keyword="none" ):
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
			self.log("No able to modify " + keyword + " in " + type )		

	def check_content(self, keyword, content) :
		result re.search(keyword, content )
	
	# header consists of key value pair
	def check_header(self, keyword, content) :
		result re.search(keyword, content )
	
	# cookie consists of key value pair
	def check_cookie(self, keyword, content) :
		result re.search(keyword, content )
		
	def re_search( self, keyword, content ):
		result re.search(keyword, content )
		
	def history(self, steps ):
		self.ff.execute_script("window.history.go(" + str(steps) + ")")
	
	def log(self, msg , leval="INFO") :
		logging.info(msg)
		if self.showloginconsole == "TRUE" :
			pprint(msg)			
			
			
	def do(self, action , xpath="none", input="none" ):
		try:
			if action == "goto" :
				# xpath here is url
				self.ff.get(xpath)
			elif action == "form" :
				self.ff.find_element_by_xpath(xpath).send_keys(input)		
			elif action == "click" :
				self.ff.find_element_by_xpath(xpath).click()	
			elif action == "link" :
				# xpath here is hyperlink text
				self.ff.find_element_by_link_text(xpath).click()	
			elif action == "return" :
				self.ff.find_element_by_xpath(xpath).send_keys(Keys.RETURN)					
			else :
				self.log("Do nothing but taking screenshot")
			self.log("Do function inputs, Action: " + action + " - Input: " + input + " - Xpath: " + xpath )	
			self.takescreenshot()
		except NoSuchElementException:
			self.log("No Element found, Action: " + action + " - Input: " + input + " - Xpath: " + xpath )


			

#####################
#      TO RUN       #
#####################          
#surf = siteAuto()
#surf.do('goto','https://www.google.com')
#surf.screenshot="FALSE"
#surf.do('form','/html/body/div/div[3]/form/div[2]/div/div[1]/div/div[1]/input','testing 1234 34333')
#surf.screenshot="TRUE"
#surf.do('return','/html/body/div/div[3]/form/div[2]/div/div[1]/div/div[1]/input')
#surf.find('AID','cookie')
#surf.wait(5)
#surf.close()

