from utils import click
from utils import loadJson
from utils import log
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def _log(msg):
    log.log_in_json(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}")


def _find_first(driver, locators, timeout=5):
    """
    Essaie une liste de locators (by, value) dans l'ordre et renvoie
    le premier élément trouvé. Lève NoSuchElementException si aucun
    ne fonctionne.
    """
    last_error = None
    for by, value in locators:
        try:
            el = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return el, (by, value)
        except TimeoutException as e:
            last_error = e
            continue
    raise NoSuchElementException(
        f"Aucun des locators fournis n'a fonctionné : {locators}"
    ) from last_error


def commentaire(driver, texte):
    """
    Ouvre les commentaires, écrit un commentaire puis l'envoie.
    Robustifié avec plusieurs stratégies de fallback car les
    resource-id de TikTok changent fréquemment entre versions.
    """
    config = loadJson.load_json()
    x = config["commentaires"]["x"]
    y = config["commentaires"]["y"]

    try:
        # =========================
        # OUVRIR COMMENTAIRES
        # =========================
        try:
            icone_commentaire, used = _find_first(
                driver,
                [
                    (AppiumBy.ID, "com.zhiliaoapp.musically:id/e51"),
                    (AppiumBy.XPATH,
                     '//android.widget.ImageView[@resource-id="com.zhiliaoapp.musically:id/e51"]'),
                ],
                timeout=4,
            )
            icone_commentaire.click()
            _log(f"Ouverture commentaires via {used}")
        except NoSuchElementException:
            click.tap_xy(driver, x, y)
            _log("Ouverture commentaires via coordonnées (fallback)")

        # =========================
        # OUVRIR / LOCALISER LE CHAMP TEXTE
        # =========================
        time.sleep(1.5)  # laisser le panneau de commentaires se charger

        champ_texte, used = _find_first(
            driver,
            [
                # EditText réel confirmé par inspection (texte tapé visible dedans)
                (AppiumBy.ID, "com.zhiliaoapp.musically:id/e7q"),
                (AppiumBy.XPATH,
                 '//android.widget.EditText[@resource-id="com.zhiliaoapp.musically:id/e7q"]'),
                # ID actuel confirmé par inspection (View "Ajouter un commentaire")
                (AppiumBy.ID, "com.zhiliaoapp.musically:id/cce"),
                (AppiumBy.XPATH,
                 '//android.view.View[@resource-id="com.zhiliaoapp.musically:id/cce"]'),
                # Ancien ID (au cas où il réapparaisse selon la version)
                (AppiumBy.ID, "com.zhiliaoapp.musically:id/c_6"),
                (AppiumBy.XPATH,
                 '//android.view.View[@resource-id="com.zhiliaoapp.musically:id/c_6"]'),
                # Fallback générique : un véritable champ de saisie EditText
                (AppiumBy.CLASS_NAME, "android.widget.EditText"),
                # Fallback via UiSelector si la classe exacte change
                (AppiumBy.ANDROID_UIAUTOMATOR,
                 'new UiSelector().className("android.widget.EditText")'),
                # Dernier recours : un texte d'invite générique TikTok (FR/EN)
                (AppiumBy.XPATH,
                 '//*[contains(@text,"commentaire") or contains(@text,"comment")]'),
            ],
            timeout=6,
        )

        # IMPORTANT : cet élément ("cce") a clickable=false dans l'arbre
        # d'accessibilité. .click() Appium peut donc échouer silencieusement
        # ou ne rien déclencher. On tape directement au centre de ses bounds
        # via ADB, ce qui simule un vrai tap physique indépendant de l'attribut
        # "clickable".
        try:
            rect = champ_texte.rect  # {'x':.., 'y':.., 'width':.., 'height':..}
            center_x = rect["x"] + rect["width"] // 2
            center_y = rect["y"] + rect["height"] // 2
            click.tap_xy(driver, center_x, center_y)
            _log(f"Champ commentaire ouvert via tap coordonnées ({used})")
        except Exception:
            # fallback ultime : tenter quand même .click() si tap_xy échoue
            champ_texte.click()
            _log(f"Champ commentaire ouvert via .click() fallback ({used})")

        # =========================
        # ECRIRE COMMENTAIRE
        # =========================
        # Délai plus long : le clavier TikTok met parfois plus d'une seconde
        # à devenir pleinement interactif après son ouverture. Taper trop tôt
        # peut faire perdre les premiers caractères (ou tous sauf le dernier).
        time.sleep(2)

        def _localiser_edittext():
            el, _ = _find_first(
                driver,
                [
                    (AppiumBy.ID, "com.zhiliaoapp.musically:id/e7q"),
                    (AppiumBy.XPATH,
                     '//android.widget.EditText[@resource-id="com.zhiliaoapp.musically:id/e7q"]'),
                    (AppiumBy.CLASS_NAME, "android.widget.EditText"),
                    (AppiumBy.ANDROID_UIAUTOMATOR,
                     'new UiSelector().className("android.widget.EditText")'),
                ],
                timeout=5,
            )
            return el

        max_tentatives = 3
        texte_saisi_ok = False

        for tentative in range(1, max_tentatives + 1):
            # On NE réutilise PAS la référence capturée avant le tap :
            # on relocalise l'EditText à chaque tentative pour éviter
            # tout problème de référence obsolète ("stale element").
            champ_actif = _localiser_edittext()

            # Sécurité : on vide le champ avant de taper, au cas où un
            # caractère résiduel (espace, etc.) s'y trouverait déjà.
            try:
                champ_actif.clear()
            except Exception:
                pass

            champ_actif.send_keys(texte)

            # Pause courte pour laisser l'UI TikTok rendre le texte avant
            # de vérifier.
            time.sleep(0.8)

            # Vérification : on relit l'attribut text de l'EditText pour
            # confirmer que la saisie a bien été prise en compte.
            try:
                champ_verif = _localiser_edittext()
                texte_actuel = champ_verif.get_attribute("text") or ""
            except Exception:
                texte_actuel = ""

            if texte_actuel.strip() == texte.strip():
                texte_saisi_ok = True
                champ_texte = champ_verif
                break
            else:
                _log(
                    f"Tentative {tentative}/{max_tentatives} : texte attendu "
                    f"'{texte}' mais champ contient '{texte_actuel}'. Nouvel essai."
                )
                time.sleep(1)

        if not texte_saisi_ok:
            _log(
                f"Échec de la saisie après {max_tentatives} tentatives. "
                f"Dernier contenu observé : '{texte_actuel}'"
            )
            raise NoSuchElementException(
                "Le texte du commentaire n'a pas pu être saisi correctement."
            )

        _log(f"Commentaire saisi : {texte}")

        # =========================
        # ATTENTE UI TIKTOK
        # =========================
        time.sleep(2)

        # =========================
        # ENVOYER COMMENTAIRE (ROBUSTE)
        # =========================
        try:
            btn_envoyer, used = _find_first(
                driver,
                [
                    # content-desc observé stable entre plusieurs versions de l'écran
                    (AppiumBy.XPATH,
                     '//android.widget.Button[@content-desc="@2131823090"]'),
                    (AppiumBy.ANDROID_UIAUTOMATOR,
                     'new UiSelector().description("@2131823090")'),
                    # IDs observés par inspection (changent selon la session/version)
                    (AppiumBy.ID, "com.zhiliaoapp.musically:id/cqf"),
                    (AppiumBy.ID, "com.zhiliaoapp.musically:id/e_d"),
                    (AppiumBy.ID, "com.zhiliaoapp.musically:id/e74"),
                    (AppiumBy.XPATH,
                     '//*[@resource-id="com.zhiliaoapp.musically:id/cqf" or @resource-id="com.zhiliaoapp.musically:id/e_d" or @resource-id="com.zhiliaoapp.musically:id/e74"]'),
                    # Fallback texte de bouton (FR/EN), au cas où l'ID change
                    (AppiumBy.XPATH,
                     '//*[@text="Envoyer" or @text="Post" or @text="Publier"]'),
                    # Fallback content-desc générique
                    (AppiumBy.XPATH,
                     '//*[contains(@content-desc,"Envoyer") or contains(@content-desc,"Post")]'),
                ],
                timeout=6,
            )

            # IMPORTANT : ce bouton reste enabled=false tant que le champ
            # de commentaire est vide ou que TikTok n'a pas fini de traiter
            # la saisie. On attend qu'il devienne enabled avant de cliquer,
            # sinon le clic ne déclenche rien (sans lever d'erreur).
            attente_max = 5
            intervalle = 0.5
            ecoule = 0.0
            while ecoule < attente_max:
                if (btn_envoyer.get_attribute("enabled") or "").lower() == "true":
                    break
                time.sleep(intervalle)
                ecoule += intervalle
                # on relocalise au cas où la référence devienne stale
                try:
                    btn_envoyer, used = _find_first(driver, [used], timeout=2)
                except NoSuchElementException:
                    pass
            else:
                _log("Bouton envoyer toujours désactivé après attente, on tente le clic quand même")

            btn_envoyer.click()
            _log(f"Commentaire envoyé via {used}")
        except NoSuchElementException as e:
            _log(f"Bouton envoyer introuvable : {str(e)}")
            raise

    except Exception as e:
        _log(f"Erreur commentaire : {str(e)}")
        raise