"""Stand-alone check that Selenium + Chrome work (Week 07). Run: python check_selenium.py  (not named test*.py so `manage.py test` does not auto-run it)"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "/usr/bin/google-chrome"      # use the path from `which google-chrome`
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

browser = webdriver.Chrome(options=options)
browser.get("https://example.com")
assert browser.page_source.find("Example Domain") != -1, "ERROR - page not found"
print("Selenium working as expected")
browser.quit()
