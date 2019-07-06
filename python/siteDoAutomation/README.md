
## SiteDo is simple one page Python Selenium script to Do most of the browser tasks

**Download and Run**

```
wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/siteDo.py \
     -O siteDo.py

python siteDo.py

```

**Customise**

* Instantiate
  * surf = SiteDo()
surf.screenshot="False"
surf.do('goto','https://www.ebay.com')
surf.screenshot="True"
surf.do('goto','https://www.google.com')
surf.find('cookie', 'VIEW' , 'COOKIENAME' )
surf.screenshot="False"
surf.history('-2')
surf.wait(2)
surf.close()


