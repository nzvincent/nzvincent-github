
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

**Set take screenshot to false**  
* surf.screenshot="False"

**Do...Goto URL**
* surf.do('goto','https://www.ebay.com')

**Set take screenshot to true**  
* surf.screenshot="True"
* surf.do('goto','https://www.google.com')

**Do...click on hyperlink**
* surf.do('link','lin-text-name')

**Do...enter html form**
* surf.do('form','/html/body/div/div[3]/form/div[2]/div/div[1]/div/div[1]/input','google search')
* surf.do('return','/html/body/div/div[3]/form/div[2]/div/div[1]/div/div[1]/input')

**Javascript history**
* surf.history('-2')

**Browser teardown**
* surf.wait(2)
* surf.close()


