from  selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

service = Service("/opt/homebrew/bin/geckodriver")
driver = webdriver.Firefox(service=service)

driver.get("https://the-internet.herokuapp.com/javascript_alerts")
driver.maximize_window()

try:
    driver.find_element(By.XPATH, "//button[@onclick='jsPrompt()']").click()
    calert = driver.switch_to.alert
    print("Alert text:", calert.text)
    calert.send_keys("Alert")
    calert.accept()

    #confirm the result
    result = driver.find_element(By.ID,"result")
    print("result text:", result.text)

finally:
    driver.quit()