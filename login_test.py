
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

@pytest.mark.parametrize("username,password,expected", [
    ("Admin","admin123", True),
    ("invalid_user","admin123", True),
    ("Admin","invalid_pass", True),
    ("invalid_user","invalid_pass", False),
])
def test_login(username,password,expected):
    service = Service("/opt/homebrew/bin/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME,"username"))).send_keys(username)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME,"password"))).send_keys(password)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH,"//button[@type='submit']"))).click()

   # driver.find_element(By.NAME,"username").send_keys("Admin")
    #driver.find_element(By.NAME,"password").send_keys("admin123")
    #driver.find_element(By.XPATH,"//button[@type='submit']").click()
    if expected:
        assert "dashboard" in driver.current_url

    else:
        error_message = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='oxd-alert-content oxd-alert-content--error']"))).text
        assert "Invalid credentials" in error_message

    driver.quit()



 