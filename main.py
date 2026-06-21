import time
from core.driver import create_driver
from utils.scroll_tiktok import scroll_tiktok

def wait_for_tiktok_loaded(driver, timeout=15):
    print("Attente du chargement de TikTok...")
    time.sleep(timeout)
    print(f"Package actuel : {driver.current_package}")
    print("TikTok chargé !")


driver = create_driver()

wait_for_tiktok_loaded(driver, timeout=15)
scroll_tiktok(driver, nb_scrolls=10, pause=3)

input("Appuyez sur Entrée pour quitter...")
driver.quit()