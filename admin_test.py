import time

import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains,Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

@pytest.mark.parametrize("username,password,confirm_password,expected_error", [
    #positive test case: valid input
    ("lilili","admin123","admin123",[]),
    #negative test case
    ("lili","password123","password123",["Should be at least 5 characters"]),
    ("lilili","","password123","Should have at least 7 characters"),
    ("lilili","password123","pa@@word123","Passwords do not match"),
    ("","password123","password123","Required")
])

def test_addAdmin(setup_login,username,password,confirm_password,expected_error):
    #click admin menu
    driver = setup_login
    WebDriverWait(driver,30).until(
        EC.visibility_of_element_located((By.LINK_TEXT,"Admin"))).click()

    #click add button
    WebDriverWait(driver,30).until(
        EC.visibility_of_element_located((By.XPATH,"//button[normalize-space()='Add']"))).click()

    #user role
    userRole = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='oxd-grid-2 orangehrm-full-width-grid']//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]")))
    action = ActionChains(driver)
    action.move_to_element(userRole).click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    #employee name
    empName = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']")))
    empName.click()
    empName.send_keys("c")
    time.sleep(10)
    actionEmp = ActionChains(driver)
    actionEmp.move_to_element(empName).click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    #status
    status = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//label[text()='Status']/following::div")))
    actionStatus = ActionChains(driver)
    actionStatus.move_to_element(status).click().send_keys(Keys.ARROW_DOWN).send_keys(
        Keys.ENTER).perform()

    #username
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//label[text()='Username']/following::div[1]//input"))).send_keys(username)

    #password
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//label[text()='Password']/following::div[1]//input"))).send_keys(password)
    #confirm password
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//label[text()='Confirm Password']/following::div[1]//input"))).send_keys(confirm_password)
    #save button
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

    #if there are expected error, verify validation message
    if expected_error:
        for error in expected_error:
            error_message = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//form/div[1]/div/div[4]/div/span")))
            assert error_message.is_displayed(), f"Expected error message '{error}' not display"

    else:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME,"oxd-table")))

        searchbox = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//form/div[1]/div/div[1]/div/div[2]/input")))

        searchAction = ActionChains(driver)
        searchAction.move_to_element(searchbox).click().send_keys(username).send_keys(Keys.ENTER).perform()

        name = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(),'{username}')"))).text

        assert len(name)>0, "system user is not added successfully.."



