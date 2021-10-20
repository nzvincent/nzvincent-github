from siteDo import siteDo

surf = siteDo()
surf.screenshot="True"

surf.label("Login to ebay.com and take screenshot")
surf.do("go", "https://www.ebay.com")

#surf.do("form","user-id-input-xpath", user-id )
#surf.do("forom","password-input-xpath", encrypted-password )
