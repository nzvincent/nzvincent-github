
## SiteDo

SiteDo is simple one page Python Selenium script to Do most of the browser tasks
Currently tested on Python 2.7 and above Linux OS, and should also be working on Windows OS.


**Download and Run**

```
wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/siteDo.py \
     -O siteDo.py

python siteDo.py

```


#### Example

**Instantiate**
* surf = SiteDo()

**Set screenshot to true or false**
* surf.screenshot="True"
* surf.screenshot="False"

**Modify variables**
* showloginconsole="False" # Do not display log in console
* 


**Do navigation methods**
* surf.do('goto','https://www.ebay.com') # go to url
* surf.do('form', '/html/form//input#user_id','john') # enter john to form input
* surf.do('return','/html/form//input#user_id') # return key
* surf.do('click','/html/form//input#user_id') # perform click via xpath
* surf.do('link','Log me out') # click on Log me out hyperlink 

**Javascript**
* surf.history('-2') # go to history 
* surf.javascript("alert('bingo')") # execute javascript

**Browser teardown**
* surf.wait(2) # wait 2 seconds
* surf.close() # close browser


