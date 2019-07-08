
## siteDo

siteDo is simple one page Python Selenium class to perform "Do" most of the browser automation tasks.
This project is not to replace test frameworks such as cucumber and other test tools.
As most of the operation tasks are short-lived and and requires rapid changes, 
I created this siteDo class to deal with repetitive automation tasks for day to day activities.
The purpose for this was to make changes easier and quicker without involving enormous coding efforts.

All you need is to download single page of python file and to run the common browser automation activities.

*@Author: nzvincent@gmail.com | Vincent Pang*

**Features**
* Firefox browser
* Take screenshots
* Assertion test
* Proxy configuration
* Colour coded logging
* password encryption / decryption
* Cookie modification
* Execute custom Javascript

**To download**

```
wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/siteDo.py \
     -O siteDo.py
```

**Python dependency pakages**
* pip install selenium requests encryption pprint

## Usage:

**Export siteDoKey to OS environment variable**
* Export enviroment variable or add it to you ~/.bashrc script
* export siteDoKey="what-ever-key-you-may-be-generated"

**Modify variables inside the siteDo.py file**
* \__log_level="INFO|DEBUG|WARNING|CRITICAL|ERROR"
* showloginconsole="False|True"
* screenshot="False|True"

**Instantiate class within siteDo.py file**
* surf = siteDo()

**Instantiate class from another Python script**
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
* surf.label("Label name")

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

**Browser teardown**
* surf.wait(2) # wait 2 seconds
* surf.close() # close browser


