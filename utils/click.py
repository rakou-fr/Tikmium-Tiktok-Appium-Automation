def tap_xy(driver, x, y):
    driver.execute_script("mobile: clickGesture", {
        "x": x,
        "y": y
    })