from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import string

driver = webdriver.Chrome('./chromedriver')
sleep_time = 2
global_login = ''
global_password = ''

# helpers
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def login_should_pass():
    driver.get("http://localhost:9091/")
    print(driver.title)

    login = driver.find_element_by_id("login")
    password = driver.find_element_by_id("password")
    save_button_path = '//input[@type="submit" and @value="Login"]'
    save_button = driver.find_element_by_xpath(save_button_path)
    login.send_keys("admin")
    password.send_keys("ziemniak123")
    time.sleep(sleep_time)
    save_button.click()
    time.sleep(sleep_time)
    print ("Checking page title after redirection")
    assert "Posts" in driver.title

def navigate_to_post_form_and_send_empty_form():
    print(driver.title + "\n" + "Opening post creator...")
    nav_element = driver.find_element_by_xpath('//a[@href="/creator"]')
    nav_element.click()
    time.sleep(sleep_time)
    print(driver.title)
    save_button = driver.find_element_by_xpath('//input[@type="submit" and @value="Submit"]')
    save_button.click()
    time.sleep(sleep_time)
    print(driver.title)
    assert "Error" in driver.title
    bodyText = driver.find_element(By.TAG_NAME, 'body').text
    assert "Ooops! something went wrong :(" in bodyText


def navigate_to_user_panel_from_error_page():
    print ("Go back home from error page...")
    nav_back_element = driver.find_element_by_xpath('//a[@href="/user/panel/1"]')
    nav_back_element.click()
    time.sleep(sleep_time)
    print(driver.title)
    assert "User" in driver.title
    assert "Success" in driver.find_element_by_class_name('border-success').text
    assert "Look out" in driver.find_element_by_class_name('border-danger').text
    assert "Informations" in driver.find_element_by_class_name('border-info').text

def navigate_to_post_and_send_valid_form():
    print(driver.title + "\n" + "Opening post creator...")
    nav_element = driver.find_element_by_xpath('//a[@href="/creator"]')
    nav_element.click()
    time.sleep(sleep_time)
    print(driver.title)
    assert "Post Form" in driver.title
    title = driver.find_element_by_id("postTitle")
    content = driver.find_element_by_id("postContent")
    title.send_keys(get_random_string(5))
    content.send_keys(get_random_string(23))
    time.sleep(sleep_time)
    save_button = driver.find_element_by_xpath('//input[@type="submit" and @value="Submit"]')
    save_button.click()
    assert "Tags Form" in driver.title

def create_post_tags_should_redirect_to_post_details():
    print ("Adding tags....")
    time.sleep(sleep_time)
    title = driver.find_element_by_id("tagsContent")
    title.send_keys(get_random_string(3) + " " + get_random_string(2))
    save_button = driver.find_element_by_xpath('//input[@type="submit" and @value="Submit"]')
    time.sleep(sleep_time)
    save_button.click()
    assert "Posts" in driver.title
    assert "Add comment" in driver.find_element_by_class_name('btn-primary').text
    assert "admin" in driver.find_element_by_class_name('justify-content-center').text

def logout_should_redirect_to_home():
    print("Log out!")
    time.sleep(sleep_time)
    nav_element = driver.find_element_by_xpath('//a[@href="/logout"]')
    nav_element.click()
    time.sleep(sleep_time)
    assert "Home" in driver.title

def after_logout_go_back_should_redirect_to_home():
    print("Go back from browser")
    driver.back()
    time.sleep(sleep_time)
    assert "Home" in driver.title

def empty_login_form_should_redirect_to_home():
    print("Sending empty login form")
    save_button_path = '//input[@type="submit" and @value="Login"]'
    save_button = driver.find_element_by_xpath(save_button_path)
    save_button.click()
    time.sleep(sleep_time)
    assert "Home" in driver.title

def go_to_register_and_send_empty_form_should_display_validation_messages():
    print("Sending empty registration form")
    nav_element = driver.find_element_by_xpath('//a[@href="/registration"]')
    nav_element.click()
    time.sleep(sleep_time)
    save_button = driver.find_element_by_xpath('//input[@type="submit" and @value="REGISTER"]')
    save_button.click()
    bodyText = driver.find_element(By.TAG_NAME, 'body').text
    assert "size must be between 5 and 25" in bodyText
    assert "must not be empty" in bodyText

def send_valid_register_form_and_redirect():
    print("Sending valid registration form")
    login = driver.find_element_by_id("nick")
    email = driver.find_element_by_id("email")
    password = driver.find_element_by_id("password")
    password_confirmation = driver.find_element_by_id("password2")
    global global_login
    global global_password 
    global_login = get_random_string(7)
    global_password = get_random_string(13)

    login.send_keys(global_login)
    email.send_keys(get_random_string(7) + '@test_domain.com')
    password.send_keys(global_password)
    password_confirmation.send_keys(global_password)
    time.sleep(sleep_time)
    save_button = driver.find_element_by_xpath('//input[@type="submit" and @value="REGISTER"]')
    save_button.click()
    time.sleep(sleep_time)
    assert "Success" in driver.title
    nav_element = driver.find_element_by_xpath('//a[@href="/login"]')
    nav_element.click()
    time.sleep(sleep_time)
    assert "Home" in driver.title

def login_with_new_user():
    login = driver.find_element_by_id("login")
    password = driver.find_element_by_id("password")
    save_button_path = '//input[@type="submit" and @value="Login"]'
    save_button = driver.find_element_by_xpath(save_button_path)
    login.send_keys(global_login)
    password.send_keys(global_password)
    time.sleep(sleep_time)
    save_button.click()
    time.sleep(sleep_time)
    print ("Checking page title after redirection")
    assert "Posts" in driver.title

login_should_pass()
navigate_to_post_form_and_send_empty_form()
navigate_to_user_panel_from_error_page()
navigate_to_post_and_send_valid_form()
create_post_tags_should_redirect_to_post_details()
logout_should_redirect_to_home()
after_logout_go_back_should_redirect_to_home()
empty_login_form_should_redirect_to_home()
go_to_register_and_send_empty_form_should_display_validation_messages()
send_valid_register_form_and_redirect()
login_with_new_user()

driver.close()