from utils import click
from utils import loadJson
from utils import log
from selenium.common.exceptions import NoSuchElementException


def commentaires(driver):
    """
    Ouvre les commentaires TikTok avec fallback X/Y.
    """

    config = loadJson.load_json()
    x = config["commentaires"]["x"]
    y = config["commentaires"]["y"]

    try:
        try:
            btn = driver.find_element(
                "id",
                "com.zhiliaoapp.musically:id/e51"
            )
            btn.click()
            log.log_in_json("💬 Commentaires via ID")
            return
        except NoSuchElementException:
            pass

        try:
            btn = driver.find_element(
                "xpath",
                '//android.widget.ImageView[@resource-id="com.zhiliaoapp.musically:id/e51"]'
            )
            btn.click()
            log.log_in_json("💬 Commentaires via XPath")
            return
        except NoSuchElementException:
            pass

        click.tap_xy(driver, x, y)
        log.log_in_json("💬 Commentaires via X/Y fallback")

    except Exception as e:
        log.log_in_json(f"❌ Erreur commentaires: {str(e)}")
        raise