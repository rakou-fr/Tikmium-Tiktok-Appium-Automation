from appium import webdriver
from appium.options.android import UiAutomator2Options

def create_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android"
    options.app_package = "com.zhiliaoapp.musically"
    options.app_activity = "com.ss.android.ugc.aweme.splash.SplashActivity"
    options.no_reset = True

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    return driver