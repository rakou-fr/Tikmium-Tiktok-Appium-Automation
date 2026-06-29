# Tikmium - TikTok Appium Automation + Orchestrator

**Outil complet d'automatisation TikTok pour Android** utilisant Appium avec planification intelligente des publications.

---

## ✨ Fonctionnalités

- Publication automatique de vidéos (description + hashtags)
- Transfert automatique de la vidéo du PC vers le téléphone via **ADB**
- Activité humaine réaliste (scroll + likes aléatoires) avant chaque upload
- Orchestrateur web pour programmer les publications à l'heure souhaitée
- Système de logs détaillé
- Interface API simple (Flask)

---

## 📁 Structure du projet
Tikmium-Tiktok-Appium-Automation/
├── orchestrator.py            # Orchestrateur principal + API
├── main.py                    # Script de base original
├── schedule_example.py        # Exemple d'utilisation de l'API
├── core/
│   └── driver.py              # Configuration Appium
├── utils/
│   ├── posterVideo.py
│   ├── scroll_tiktok.py
│   ├── likes.py
│   ├── click.py
│   ├── log.py
│   └── ...
├── log.txt                    # Logs d'exécution
├── requirements.txt
└── README.md
text---

## 🚀 Installation

### Prérequis

- Python 3.8+
- Appium Server installé et lancé
- ADB installé (`adb devices` doit fonctionner)
- Téléphone Android connecté en USB avec **USB Debugging** activé
- TikTok installé sur le téléphone

### Installation

```bash
git clone https://github.com/rakou-fr/Tikmium-Tiktok-Appium-Automation.git
cd Tikmium-Tiktok-Appium-Automation

pip install -r requirements.txt

▶️ Démarrage
Lancer l'orchestrateur
Bashpython orchestrator.py
Le serveur sera accessible sur : http://localhost:5000

📡 API
Planifier une publication
POST /schedule
JSON{
  "video_path": "/chemin/absolu/vers/ta_video.mp4",
  "title": "Titre de la vidéo",
  "description": "Description complète...",
  "hashtags": ["fyp", "viral", "pourtoi"],
  "scheduled_time": "2026-06-30T14:30:00"
}
Voir les tâches planifiées
GET /tasks

📌 Exemple d'utilisation
Voir le fichier  fourni dans le repo.

⚙️ Configuration

Modifie l'udid dans core/driver.py avec celui de ton téléphone (adb devices)
Le dossier de destination sur le téléphone est configurable dans 


📝 Logs
Tous les événements (transfert, activité humaine, publication, erreurs) sont enregistrés dans :

La console
Le fichier log.txt


⚠️ Avertissement
Cet outil est destiné à un usage éducatif et personnel.
Respectez les conditions d'utilisation de TikTok. Une utilisation intensive peut entraîner des restrictions de compte.

📄 License
MIT License

Auteur : rakou-fr
Projet Open Source

**Copie tout le texte ci-dessus** (de `# Tikmium` jusqu'à la fin) et colle-le dans un fichier nommé exactement `README.md`. C’est prêt pour GitHub.
