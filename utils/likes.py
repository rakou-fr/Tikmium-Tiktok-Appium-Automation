from utils import click
from utils import loadJson
from utils import log
from selenium.common.exceptions import NoSuchElementException


def like(driver):
    """
    Fonction pour liker une vidéo TikTok avec fallback X/Y.
    """

    config = loadJson.load_json()
    like_button_x = config["like"]["x"]
    like_button_y = config["like"]["y"]

    try:
        try:
            like_btn = driver.find_element(
                "xpath",
                '//android.widget.ImageView[@content-desc="J\'aime"]'
            )
            like_btn.click()
            log.log_in_json("Like via XPath")
            return
        except NoSuchElementException:
            pass

        try:
            like_btn = driver.find_element(
                "accessibility id",
                "J'aime"
            )
            like_btn.click()
            log.log_in_json("Like via accessibility id")
            return
        except NoSuchElementException:
            pass

        click.tap_xy(driver, like_button_x, like_button_y)
        log.log_in_json("Like via X/Y fallback")

    except Exception as e:
        log.log_in_json(f"❌ Erreur like: {str(e)}")
        raise