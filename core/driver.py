from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

def create_driver():
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android"
    options.udid = "90f43524"

    options.no_reset = True

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    driver.terminate_app("com.zhiliaoapp.musically")
    time.sleep(2)
    driver.activate_app("com.zhiliaoapp.musically")

    time.sleep(5)

    return driver