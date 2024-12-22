import time
from struct import unpack_from

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service("/Users/user/Downloads/geckodriver")
driver = webdriver.Firefox(service=service)

driver.get("https://the-internet.herokuapp.com/dynamic_loading")
driver.maximize_window()

driver.find_element(By.LINK_TEXT,"Example 2: Element rendered after the fact").click()

wait = WebDriverWait(driver,10)

startbtn = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Start']")))
startbtn.click()

driver.save_screenshot("ss1.png")

hidden_text = wait.until(EC.visibility_of_element_located((By.ID, "finish")))
print(hidden_text.text)

driver.quit()



