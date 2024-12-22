import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service

service = Service("/Users/user/Downloads/geckodriver")
driver = webdriver.Firefox(service=service)

driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")

driver.execute_script("window.open('https://the-internet.herokuapp.com/','_blank');")

handles = driver.window_handles
print(handles)

driver.switch_to.window(handles[1])
time.sleep(3)
print(driver.title)
time.sleep(3)

driver.switch_to.window(handles[0])
print(driver.title)
time.sleep(3)

driver.quit()