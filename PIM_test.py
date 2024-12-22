import os.path
import time

import pytest
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from  selenium.webdriver.support import expected_conditions as EC

from window_handle import driver

def test_add_employee(setup_login):
    #go to PIM module
    driver = setup_login
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.LINK_TEXT, "PIM"))).click()

    #click add button
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Add']"))).click()

    #first name
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.NAME, "firstName"))).send_keys("Myint")

    #middle name
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.NAME, "middleName"))).send_keys("Khaing")

    #last name
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.NAME, "lastName"))).send_keys("Zin")

   #upload picture
    #1.find >> type='file'
    #2.abspath >>os.path.abspath("file location")
    #3.send_keys

    upload_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//input[@class='oxd-file-input']")))

    img_source = os.path.abspath("./resources/1.jpeg")
    upload_input.send_keys(img_source)

    #confirm image is uploaded successfully
    uploaded_pic = driver.find_element(By.CLASS_NAME, "employee-image").get_attribute("src")
    assert "/web/images/default-photo.png" not in uploaded_pic, "image upload not successful"

    #save button
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))).click()

    time.sleep(10)
    #confirm save
    url = driver.current_url
    assert "viewPersonalDetails" in url,"employee not added"

def test_edit_employee(setup_login):
    driver = setup_login
    driver.find_element(By.LINK_TEXT, "PIM").click()

    action = ActionChains(driver)
    username_search = driver.find_element(By.XPATH, "//label[text()='Employee Name']/following::div")
    action.move_to_element(username_search).click().send_keys("khaing").send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    #searchbtn
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    #comfirm whether user is added in the table
    driver.find_elements(By.XPATH, "//a[contains(text(), 'Khaing')]")

    driver.find_element(By.XPATH,"//i[@class='oxd-icon bi-pencil-fill']").click()

    assert "viewPersonalDetails" in driver.current_url, "user not exist"

    # driver license no
    driver.find_element(By.XPATH, "//form[1]/div[2]/div[2]/div[1]/div[1]/div[2]/input[1]").send_keys("1100201")

    # license expire date
    lincesExp = driver.find_element(By.XPATH, "//form/div[2]/div[2]/div[2]/div/div[2]/div/div/input")
    lincesExp.click()
    lincesExp.send_keys("2024-16-12")

    # nationality
    dropdown = driver.find_element(By.XPATH, "//label[text()='Nationality']/following::div")
    dropdown.click()
    option_xpath = "//span[text()='Japanese']"
    option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, option_xpath))
    )
    option.click()

    print("Nationality Japanese selected successfully.")

    # marital status
    marital_status = driver.find_element(By.XPATH, "//label[text()='Marital Status']/following::div")
    marital_action = ActionChains(driver)
    marital_action.move_to_element(marital_status).click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    # date of birth
    dob = driver.find_element(By.XPATH, "//form/div[3]/div[2]/div[1]/div/div[2]/div/div/input")
    dob.click()
    dob.send_keys("1994-09-21")

    # gender
    male_radio = driver.find_element(By.XPATH, "//label[normalize-space()='Male']")
    female_radio = driver.find_element(By.XPATH, "//label[normalize-space()='Female']")
    if not male_radio.is_selected():
        male_radio.click()
    if not female_radio.is_selected():
        female_radio.click()

    # save button
    driver.find_element(By.XPATH,
                        "//div[@class='orangehrm-horizontal-padding orangehrm-vertical-padding']//button[@type='submit'][normalize-space()='Save']").click()

    success_message = driver.find_element(By.XPATH, "//div[@class='oxd-toast oxd-toast--success oxd-toast-container--toast']")
    assert success_message.is_displayed(), "edit employee fail"

def test_bulk_delete_em(setup_login):
    driver = setup_login
    driver.find_element(By.LINK_TEXT, "PIM").click()

    multi_select = driver.find_element(By.XPATH, "//div[@role='columnheader']//i[@class='oxd-icon bi-check oxd-checkbox-input-icon']")
    multi_select.click()

    delete_but = driver.find_element(By.XPATH, "//button[normalize-space()='Delete Selected']")
    delete_but.click()

    time.sleep(4)
    confirm_msg = driver.find_element(By.XPATH, "//*[@id='app']/div[3]/div/div/div")
    assert confirm_msg.is_displayed(), "deleted confirm message not display"

    time.sleep(4)
    con_del = driver.find_element(By.XPATH, "//button[normalize-space()='Yes, Delete']")
    con_del.click()

    success_msg = driver.find_element(By.XPATH, "//div[@class='oxd-toast-content oxd-toast-content--success']")
    assert success_msg.is_displayed(), "Delete Failed"
