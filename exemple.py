import requests
from datetime import datetime, timedelta

payload = {
    "video_path": "C:\\Users\\balin\\Desktop\\Projet\\Tikmium-Tiktok-Appium-Automation\\MontageTest",   # Chemin sur ton PC
    "title": "Meileur outils factures resell 2026",
    "description": "Meileur outils factures resell 2026 ",
    "hashtags": ["vinted", "facture", "resell"],
    "scheduled_time": (datetime.now() + timedelta(minutes=1)).isoformat()
}

r = requests.post("http://localhost:5000/schedule", json=payload)
print(r.json())