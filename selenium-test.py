from selenium import webdriver
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=opts)
driver.get("https://example.com")
print("TITLE:", driver.title)
driver.quit()