import time
from core.driver import create_driver
from utils.commentaires import commentaire
from utils.enregistrer import enregistrer
from utils.scroll_tiktok import scroll_tiktok
from utils.likes import like
from utils.posterVideo import poster_video
from utils.log import log_in_json
from utils.choisirCommentaire import construire_commentaire
import time

log_in_json(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Démarrage du script TikTok Automation")

def wait_for_tiktok_loaded(driver, timeout=15):
    print("Attente du chargement de TikTok...")
    time.sleep(timeout)
    print("Package actuel :", driver.current_package)

    if driver.current_package != "com.zhiliaoapp.musically":
        raise Exception(
            f"TikTok n'est pas ouvert : {driver.current_package}"
        )
    print("TikTok chargé !")

driver = create_driver()

wait_for_tiktok_loaded(driver, timeout=15)
# like(driver)
time.sleep(2)
poster_video(driver, description="Test TikTok Automation", hashtags="#test #automation")
# commentaire(driver, construire_commentaire())
# enregistrer(driver)
# scroll_tiktok(driver, nb_scrolls=10, pause=3)

input("Appuyez sur Entrée pour quitter...")
driver.quit()