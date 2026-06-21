import time
import random

def scroll_tiktok(driver, nb_scrolls=10, pause=3):
    screen_size = driver.get_window_size()
    width = screen_size['width']
    height = screen_size['height']

    start_x = width // 2
    start_y = int(height * 0.8)
    end_y = int(height * 0.2)

    print(f"Début du scroll ({nb_scrolls} vidéos)...")

    for i in range(nb_scrolls):
        print(f"  Vidéo suivante ({i + 1}/{nb_scrolls})")
        driver.swipe(start_x, start_y, start_x, end_y, 500)
        time.sleep(pause)