import pytest
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#module = whole class
#function = test function
#session = chrome driver session

@pytest.fixture()
def setup_login():
    service = Service("/opt/homebrew/bin/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()

    driver.implicitly_wait(30)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "username"))).send_keys("Admin")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "password"))).send_keys("admin123")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

    yield driver


    driver.quit()
