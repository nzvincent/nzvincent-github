
## SiteDo

siteDo is simple one page Python Selenium class to perform "Do" most of the browser's tasks.
This project is not to replace test frameworks such as cucumber and other test tools.
As most of the operation tasks are short-lived and and requires rapid changes, 
I created this siteDo class to deal with repetitive automation tasks for day to day activities.
The purpose for this was to make changes easier and quicker without involving enormous coding efforts.

All you need is download single page of python class file to run the common browser auotation activities.

*@Author: nzvincent@gmail.com | Vincent Pang*

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


