
## SiteDo

siteDo is simple one page Python Selenium class to perform "Do" most of the browser's tasks.
This project is not to replace test frameworks such as cucumber and other test tools.
As most of the operation tasks are short-lived and and requires rapid changes, 
I created this siteDo class to deal with repetitive automation tasks for day to day activities.
The purpose for this was to make changes easier and quicker without involving enormous coding efforts.

All you need is download single page of python class file to run the common browser auotation activities.

*@Author: nzvincent@gmail.com | Vincent Pang*

**Features**
* Firefox browser
* Take screenshots
* Assertion test
* Proxy configuration
* Multi level colour coded logging
* Cookie modification
* Execute custom Javascript


**To download**

```
wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/siteDo.py \
     -O siteDo.py
```


#### Usage:

**Instantiate class**
* surf = SiteDo()

**Set screenshot to true or false**
* surf.screenshot="True"
* surf.screenshot="False"

**Modify variables**
* showloginconsole="False"
* showloginconsole="True"

**Do navigation methods**
* surf.do('goto','https://www.ebay.com') # go to url
* surf.do('form', '/html/form//input#user_id','john') # enter john to form input
* surf.do('return','/html/form//input#user_id') # return key
* surf.do('click','/html/form//input#user_id') # perform click via xpath
* surf.do('link','Log me out') # click on Log me out hyperlink 

**Lable**
* surf.label("Label name")

**Find and replace**
* surf.find("COOKIE","VIEW","cookie-name")
* surf.find("COOKIE","EDIT","cookie-name","new-value","search-regular-expression-word-to-be-replace")
* surf.find("COOKIE","ADD","cookie-name","new-cookie-value")
* surf.find("COOKIE","DELETE","cookie-name")
* surf.find("COOKIE","DELETE_ALL_COOKIE")

**Lookup**
* surf.lookup("fashion" , "IN", "SOURCE" ) # return TRUE when fashing found in page source
* surf.lookup("xfashion" , "NOT_IN", "SOURCE" ) # return TRUE when xfashion not found in page source
* surf.lookup('eBay' , 'IN', 'XPATH' , '//*[@id="destinations_list1"]/div/div/div/h2' ) # return TRUE when eBay found in xpath element text 


**Javascript**
* surf.history('-2') # go to history 
* surf.javascript("alert('bingo')") # execute javascript

**Browser teardown**
* surf.wait(2) # wait 2 seconds
* surf.close() # close browser


