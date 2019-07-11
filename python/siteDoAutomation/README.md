
## siteDo

siteDo is a simple one page Python Selenium class to perform "Do" most of the browser's tasks.
Purpose for this is to make Selenium test change as simple as possible.

I created this siteDo class to deal with repetitive automation tasks fo my day to day work and running it from my Linux desktop and Jenkins.

**Features**
* Firefox browser support GUI or headless
* Easy customise test case
* Encrypt password
* Take screenshots
* Assertion test and report
* xpath element selector
* Proxy support
* Colour coded logging
* Cookie modification
* Execute custom Javascript or Javascript file 
* Generate HTML report

*@Author: nzvincent@gmail.com | Vincent Pang*

**To download**


**Simple kickstart**
* Download wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/siteDo.py -O siteDo.py
* Create kickstart.py file
```
from siteDo import siteDo

surf = siteDo()
surf.screenshot="True"

surf.label("Login to ebay.com and take screenshot")
surf.do("go", "https://www.ebay.com")

#surf.do("form","user-id-input-xpath", user-id )
#surf.do("forom","password-input-xpath", encrypted-password )

```
* Run python kickstart.py

**Python dependency pakages**
* pip install selenium requests pprint os time
* pip install --no-cache-dir cryptography==2.1.4
* pip install cryptography ( depending on your distribution ) 


## Usage:

**Export siteDoKey to OS environment variable**
* Export enviroment variable or add it to you ~/.bashrc script
* export siteDoKey="what-ever-key-you-may-be-generated"
* To generate siteDokey token and encrypted password, use my other script *python encrypt.py*

**Modify variables inside the siteDo.py file**
* \__log_level="INFO|DEBUG|WARNING|CRITICAL|ERROR"
* showloginconsole="False|True"
* screenshot="False|True"

**Instantiate class**
```
from siteDo import siteDo

surf = siteDo()
...
```

**Set screenshot to true or false**
* surf.screenshot="True"
* surf.screenshot="False"

**Do navigation methods**
* surf.do('goto','https://www.ebay.com') # go to url
* surf.do('form', '/html/form//input#user_id','john') # enter john to form input
* surf.do('return','/html/form//input#user_id') # return key
* surf.do('click','/html/form//input#user_id') # perform click via xpath
* surf.do('link','Log me out') # click on Log me out hyperlink 

**Label**
* surf.label("Go to gmail and check messages.")

**Find and edit/replace cookies**
* surf.find("COOKIE","VIEW","cookie-name")
* surf.find("COOKIE","EDIT","cookie-name","new-value","search-regular-expression-word-to-be-replace")
* surf.find("COOKIE","ADD","cookie-name","new-cookie-value")
* surf.find("COOKIE","DELETE","cookie-name")
* surf.find("COOKIE","DELETE_ALL_COOKIE")

**Lookup and assertion test**
* surf.lookup("fashion" , "IN", "SOURCE" ) # return TRUE when fashing found in page source
* surf.lookup("xfashion" , "NOT_IN", "SOURCE" ) # return TRUE when xfashion not found in page source
* surf.lookup('eBay' , 'IN', 'XPATH' , '//*[@id="destinations_list1"]/div/div/div/h2' ) # return TRUE when eBay found in xpath element text 

**Generate encrypted password**
* your_password = "your-unencrypted-password"
* enc_password = surf.encrypt("your_password")
* surf.decrypt(enc_password)
* To generate token and encrypted password, use another script *python encrypt.py*

**Use encrypted password in form**
* ENC_PASSWORD = "ENC_PASS:gAAA3ABdIr4Fc9...mYoxjOhmvGGo_SxV_uti8xLFQcH4"
* surf.do('form','//*[@id="user_name"]', YOUR_USER_ID )
* surf.do('form','//*[@id="password"]', ENC_PASSWORD )

**Javascript**
* surf.history('-2') # go to history 
* surf.javascript("alert('bingo')") # execute javascript
* surf.javascript(javascript-file.js)

**Browser teardown**
* surf.wait(2) # wait 2 seconds
* surf.close() # close browser

**Troubleshotting**

```
ps -ef | grep firefox | awk '{print $3}' | xargs kill -9 &
ps -ef | grep firefox | awk '{print $2}' | xargs kill -9 &
ps -ef | grep geckodriver | awk '{print $3}' | xargs kill -9 &
ps -ef | grep geckodriver | awk '{print $2}' | xargs kill -9 &
```


