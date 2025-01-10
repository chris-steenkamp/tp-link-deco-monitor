import os
from contextlib import contextmanager
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

# def sleep(n): ...


def get_named_element(driver, class_name, element_name):
    element = [
        i
        for i in list(driver.find_elements(By.CLASS_NAME, class_name))
        if i.text == element_name
    ][0]

    return element


@contextmanager
def create_driver(headless):
    print("Starting browser...")
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    print("Browser started")

    try:
        yield driver
    finally:
        driver.quit()


def perform_reboot(url, password, headless: bool = True):
    with create_driver(headless) as driver:
        print("Navigating to login page...")
        driver.get(url)
        sleep(3)

        # Set password
        password_field = driver.find_element(By.CLASS_NAME, "password-hidden")
        sleep(1)
        password_field.send_keys(password)
        sleep(1)

        # Login
        print("Logging in...")
        login = get_named_element(driver, "button-button", "LOG IN")
        sleep(1)
        login.click()
        sleep(5)
        print("Logged in")

        # Navigate to reboot page
        print("Loading device list...")
        driver.get(f"{url}#reboot")
        sleep(30)

        # Click reboot
        print("Rebooting...")
        reboot_button = get_named_element(driver, "button-button", "REBOOT ALL")
        reboot_button.click()
        sleep(5)

        # Confirm reboot
        reboot_button = get_named_element(driver, "button-button", "Reboot")
        reboot_button.click()
        sleep(60)


if __name__ == "__main__":
    load_dotenv()

    password = os.environ.get("PASSWORD")
    url = os.environ.get("BASE_URL")

    perform_reboot(url, password)
