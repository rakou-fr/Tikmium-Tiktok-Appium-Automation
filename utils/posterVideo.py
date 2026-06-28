from utils import click
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


# =========================================================
# ETAPE 1 : ALLER SUR L'ONGLET POSTER
# =========================================================
def aller_sur_onglet_poster(driver):
    """
    Clique sur l'onglet "Poster" (bouton "+" central de la barre de
    navigation, libellé interne TikTok "Créer").
    Élément confirmé par inspection : Button resource-id "nr7",
    content-desc "Créer", clickable=true, bounds normales dans la barre
    de navigation. (L'élément "cck" initialement inspecté était un View
    technique invisible de 1px de haut, non cliquable — pas le vrai bouton.)
    """
    bouton, used = _find_first(
        driver,
        [
            (AppiumBy.ID, "com.zhiliaoapp.musically:id/nr7"),
            (AppiumBy.XPATH,
             '//android.widget.Button[@resource-id="com.zhiliaoapp.musically:id/nr7"]'),
            # Fallback par content-desc, au cas où l'ID change
            (AppiumBy.XPATH, '//*[@content-desc="Créer"]'),
            (AppiumBy.ANDROID_UIAUTOMATOR,
             'new UiSelector().description("Créer")'),
        ],
        timeout=6,
    )
    bouton.click()
    _log(f"Onglet Poster ouvert via {used}")


# =========================================================
# ETAPE 2 : CLIQUER SUR "CHOISIR IMAGES/VIDEOS" (galerie)
# =========================================================
def choisir_depuis_galerie(driver):
    """
    Clique sur la zone qui ouvre la galerie du téléphone.
    Élément confirmé par inspection : FrameLayout clickable=true.
    """
    bouton, used = _find_first(
        driver,
        [
            (AppiumBy.ID, "com.zhiliaoapp.musically:id/upload_hot_area"),
            (AppiumBy.XPATH,
             '//android.widget.FrameLayout[@resource-id="com.zhiliaoapp.musically:id/upload_hot_area"]'),
        ],
        timeout=6,
    )
    bouton.click()
    _log(f"Galerie ouverte via {used}")


# =========================================================
# ETAPE 3 : FILTRER SUR "VIDEO"
# =========================================================
def filtrer_video(driver):
    """
    Clique sur l'onglet de filtre "Vidéo" dans la galerie.
    Privilégie la recherche par texte visible (plus stable qu'un index de
    position, qui peut varier selon le contenu de la galerie). Le XPath
    positionnel observé par inspection est gardé en dernier fallback.
    """
    bouton, used = _find_first(
        driver,
        [
            # Recherche par texte visible (FR/EN), plus robuste qu'un index
            (AppiumBy.XPATH, '//*[@text="Vidéo" or @text="Video" or @text="Vidéos" or @text="Videos"]'),
            (AppiumBy.ANDROID_UIAUTOMATOR,
             'new UiSelector().textContains("Vidéo")'),
            (AppiumBy.ANDROID_UIAUTOMATOR,
             'new UiSelector().textContains("Video")'),
            # Fallback positionnel observé par inspection (fragile : dépend
            # du contenu de la galerie, à utiliser en dernier recours)
            (AppiumBy.XPATH,
             '//android.widget.GridView[@resource-id="com.zhiliaoapp.musically:id/j0u"]/android.widget.FrameLayout[8]'),
            (AppiumBy.ANDROID_UIAUTOMATOR,
             'new UiSelector().className("android.widget.FrameLayout").instance(102)'),
        ],
        timeout=6,
    )
    bouton.click()
    _log(f"Filtre Vidéo appliqué via {used}")


# =========================================================
# ETAPE 4 : SELECTIONNER LA PREMIERE VIDEO (la plus récente)
# =========================================================
def selectionner_premiere_video(driver):
    """
    Sélectionne la première vidéo de la grille (la plus récente).
    Élément confirmé par inspection : Button resource-id "k_x", instance(0).
    """
    elements = driver.find_elements(
        AppiumBy.ID, "com.zhiliaoapp.musically:id/k_x"
    )
    if not elements:
        raise NoSuchElementException(
            "Aucune vidéo trouvée dans la galerie (id k_x introuvable)."
        )

    elements[0].click()
    _log("Première vidéo (la plus récente) sélectionnée")


# =========================================================
# ETAPE 5 : CLIQUER SUR "SUIVANT"
# =========================================================
def cliquer_suivant(driver):
    """
    Clique sur le bouton "Suivant" pour valider la sélection de la vidéo.
    Élément confirmé par inspection : Button resource-id "wjp", text "Suivant".
    """
    bouton, used = _find_first(
        driver,
        [
            (AppiumBy.ID, "com.zhiliaoapp.musically:id/wjp"),
            (AppiumBy.XPATH,
             '//android.widget.Button[@resource-id="com.zhiliaoapp.musically:id/wjp"]'),
            # Fallback texte au cas où l'ID change
            (AppiumBy.XPATH, '//android.widget.Button[@text="Suivant" or @text="Next"]'),
        ],
        timeout=6,
    )
    bouton.click()
    _log(f"Bouton Suivant cliqué via {used}")


# =========================================================
# ETAPE 5bis : ECRAN D'EDITION INTERMEDIAIRE ("Ta Story" / "Suivant")
# =========================================================
def cliquer_suivant_edition(driver):
    """
    Après la sélection de la vidéo, TikTok affiche un écran d'édition
    intermédiaire (options "Ta Story" à gauche, "Suivant" à droite) avant
    d'arriver à l'écran final de description. Cette étape clique sur ce
    second bouton "Suivant".
    Élément confirmé par inspection : LinearLayout resource-id "p2y",
    clickable=true, contenant un TextView enfant avec text="Suivant" (p31).
    """
    bouton, used = _find_first(
        driver,
        [
            (AppiumBy.ID, "com.zhiliaoapp.musically:id/p2y"),
            (AppiumBy.XPATH,
             '//android.widget.LinearLayout[@resource-id="com.zhiliaoapp.musically:id/p2y"]'),
            # Fallback texte au cas où l'ID change
            (AppiumBy.XPATH, '//*[@text="Suivant" or @text="Next"]'),
        ],
        timeout=6,
    )
    bouton.click()
    _log(f"Bouton Suivant (écran d'édition) cliqué via {used}")


# =========================================================
# ETAPE 6 : AJOUTER DESCRIPTION + HASHTAGS
# =========================================================
def ajouter_description(driver, description="", hashtags=None):
    """
    Renseigne la description (légende) et les hashtags dans le champ
    EditText prévu à cet effet.
    Élément confirmé par inspection : EditText resource-id "gpr",
    hint "Ajouter une description…".
    """
    hashtags = hashtags or []
    # Tolère hashtags passé comme une chaîne unique ("#a #b") ou comme
    # une liste (["a", "#b"]) : une simple chaîne ne doit pas être itérée
    # caractère par caractère.
    if isinstance(hashtags, str):
        hashtags = hashtags.split()

    texte_complet = description.strip()
    if hashtags:
        hashtags_str = " ".join(f"#{h.lstrip('#')}" for h in hashtags)
        texte_complet = f"{texte_complet} {hashtags_str}".strip()

    champ, used = _find_first(
        driver,
        [
            (AppiumBy.ID, "com.zhiliaoapp.musically:id/gpr"),
            (AppiumBy.XPATH,
             '//android.widget.EditText[@resource-id="com.zhiliaoapp.musically:id/gpr"]'),
            (AppiumBy.CLASS_NAME, "android.widget.EditText"),
        ],
        timeout=6,
    )
    champ.click()
    time.sleep(0.5)
    champ.send_keys(texte_complet)
    _log(f"Description/hashtags saisis via {used} : {texte_complet}")

    # Le clavier reste ouvert après la saisie et masque le bas de l'écran
    # (où se trouve le bouton "Publier"). On le ferme explicitement pour
    # libérer la vue avant de chercher ce bouton.
    try:
        driver.hide_keyboard()
        _log("Clavier fermé via driver.hide_keyboard()")
    except Exception as e:
        _log(f"hide_keyboard() a échoué ({str(e)}), tentative via touche BACK")
        try:
            driver.press_keycode(4)  # KEYCODE_BACK
            _log("Clavier fermé via KEYCODE_BACK")
        except Exception as e2:
            _log(f"Impossible de fermer le clavier : {str(e2)}")

    time.sleep(0.5)


# =========================================================
# ETAPE 7 : PUBLIER
# =========================================================
def publier(driver):
    """
    Clique sur le bouton final "Publier".
    Si la popup de confirmation d'utilisation de la musique apparaît,
    clique également sur "Publier la vidéo".
    """
    # Bouton Publier principal
    bouton, used = _find_first(
        driver,
        [
            (AppiumBy.ID, "com.zhiliaoapp.musically:id/sa3"),
            (AppiumBy.XPATH,
             '//android.widget.Button[@resource-id="com.zhiliaoapp.musically:id/sa3"]'),
            (AppiumBy.XPATH,
             '//android.widget.Button[@text="Publier" or @text="Post"]'),
        ],
        timeout=6,
    )

    bouton.click()
    _log(f"Publication lancée via {used}")

    # Attendre quelques secondes pour voir si la popup apparaît
    time.sleep(2)

    try:
        popup_btn, popup_used = _find_first(
            driver,
            [
                (
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().text("Publier la vidéo")'
                ),
                (
                    AppiumBy.XPATH,
                    '//android.widget.Button[@text="Publier la vidéo"]'
                ),
            ],
            timeout=3,
        )

        popup_btn.click()
        _log(f"Popup musique confirmée via {popup_used}")

    except NoSuchElementException:
        _log("Aucune popup de confirmation musique détectée.")


# =========================================================
# FONCTION PRINCIPALE : ENCHAINE TOUTES LES ETAPES
# =========================================================
def poster_video(driver, description="", hashtags=None):
    """
    Enchaîne toutes les étapes pour poster la vidéo la plus récente
    de la galerie du téléphone, avec description et hashtags.
    """
    try:
        aller_sur_onglet_poster(driver)
        time.sleep(1.5)

        choisir_depuis_galerie(driver)
        time.sleep(1.5)

        filtrer_video(driver)
        time.sleep(1)

        selectionner_premiere_video(driver)
        time.sleep(1)

        cliquer_suivant(driver)
        time.sleep(1.5)

        cliquer_suivant_edition(driver)
        time.sleep(1.5)

        ajouter_description(driver, description=description, hashtags=hashtags)
        time.sleep(1)

        publier(driver)
        _log("Vidéo publiée avec succès")

    except Exception as e:
        _log(f"Erreur lors de la publication de la vidéo : {str(e)}")
        raise