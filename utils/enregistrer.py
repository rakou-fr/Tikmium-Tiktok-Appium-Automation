from utils import click
from utils import loadJson
from utils import log
from selenium.common.exceptions import NoSuchElementException


def enregistrer(driver):
    """
    Fonction pour enregistrer une vidéo TikTok avec fallback X/Y.
    """

    config = loadJson.load_json()
    x = config["enregistrer"]["x"]
    y = config["enregistrer"]["y"]

    try:
        try:
            btn = driver.find_element(
                "xpath",
                '//android.widget.ImageView[@resource-id="com.zhiliaoapp.musically:id/hdn"]'
            )
            btn.click()
            log.log_in_json("💾 Enregistrer via XPath")
            return
        except NoSuchElementException:
            pass

        try:
            btn = driver.find_element(
                "id",
                "com.zhiliaoapp.musically:id/hdn"
            )
            btn.click()
            log.log_in_json("💾 Enregistrer via ID")
            return
        except NoSuchElementException:
            pass

        click.tap_xy(driver, x, y)
        log.log_in_json("💾 Enregistrer via X/Y fallback")

    except Exception as e:
        log.log_in_json(f"❌ Erreur enregistrer: {str(e)}")
        raise