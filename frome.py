import time
from struct import unpack_from

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

service = Service("/Users/user/Downloads/geckodriver")
driver = webdriver.Firefox(service=service)

driver.get("https://the-internet.herokuapp.com/frames")
driver.maximize_window()

nframe = driver.find_element(By.LINK_TEXT,"Nested Frames")
nframe.click()

driver.switch_to.frame("frame-top")

driver.switch_to.frame("frame-left")

left_text = driver.find_element(By.TAG_NAME,"body")
print(left_text.text)

time.sleep(10)
driver.switch_to.default_content()

time.sleep(10)
driver.quit()