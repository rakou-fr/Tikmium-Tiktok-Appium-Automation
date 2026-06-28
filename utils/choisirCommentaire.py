import json
import random


def construire_commentaire():
    with open("./utils/data/commentaires.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    type_commentaire = random.choice(["positif", "neutre", "negatif"])

    debut = random.choice(data[f"{type_commentaire}_debut"])
    milieu = random.choice(data[f"{type_commentaire}_milieu"])
    fin = random.choice(data[f"{type_commentaire}_fin"])

    commentaire = f"{debut} {milieu} {fin}"

    return commentaire