from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pprint import pprint
import time
import datetime
import os
import logging

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
	
		
	def findCookie(self, cookieName):
		# ToDo... use regex
		cookies_list = self.ff.get_cookies()
		cookies_dict = {}
		for cookie in cookies_list:
			cookies_dict[cookie['name']] = cookie['value']

		found_cookie = cookies_dict.get(cookieName)

		if not found_cookie:
			self.log("Cookie " + cookieName + " not found")
		  	# siteTest.close()
		else:
			self.log("Cookie found" + cookieName + "=" + found_cookie )
			self.writecookie( cookieName + "=" + found_cookie )
		
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
surf = siteAuto()
surf.do('goto','https://www.google.com')
surf.screenshot="FALSE"
surf.do('form','/html/body/div/div[3]/form/div[2]/div/div[1]/div/div[1]/input','testing 1234 34333')
surf.screenshot="TRUE"
surf.do('return','/html/body/div/div[3]/form/div[2]/div/div[1]/div/div[1]/input')
surf.find('AID','cookie')
surf.wait(5)
surf.close()

