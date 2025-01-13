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
    print("Starting browser... ", end="")
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    print("Success!", flush=True)

    try:
        yield driver
    finally:
        driver.quit()


def navigate_to_page(driver, url, wait):
    print(f"Navigating to {url}", flush=True)
    driver.get(url)
    sleep(wait)


def perform_reboot(headless: bool = True):
    load_dotenv()

    password = os.environ.get("PASSWORD")
    url = os.environ.get("BASE_URL")

    with create_driver(headless) as driver:
        navigate_to_page(driver, url, 3)

        # Set password
        password_field = driver.find_element(By.CLASS_NAME, "password-hidden")
        password_field.send_keys(password)

        # Login
        print("Logging in... ", end="")
        login = get_named_element(driver, "button-button", "LOG IN")
        login.click()
        sleep(5)
        print("Success!", flush=True)

        # Navigate to reboot page
        navigate_to_page(driver, f"{url}#reboot", 30)

        # Click reboot
        print("Rebooting... ", end="")
        reboot_button = get_named_element(driver, "button-button", "REBOOT ALL")
        reboot_button.click()
        sleep(5)

        # Confirm reboot
        reboot_button = get_named_element(driver, "button-button", "Reboot")
        reboot_button.click()
        sleep(300)
        print("Success!", flush=True)


if __name__ == "__main__":
    perform_reboot()
