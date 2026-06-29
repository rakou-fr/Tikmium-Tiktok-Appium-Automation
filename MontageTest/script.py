import os
from moviepy import VideoFileClip

# Fichiers
VIDEO_A = "VideoA.mp4"   # Image à conserver
VIDEO_B = "VideoB.mp4"   # Son à récupérer

# Dossier de sortie
OUTPUT_DIR = "final"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT = os.path.join(OUTPUT_DIR, "video_finale.mp4")

# Charger les vidéos
video_a = VideoFileClip(VIDEO_A)
video_b = VideoFileClip(VIDEO_B)

# Récupérer l'audio de B
audio = video_b.audio

if audio is None:
    raise Exception("La vidéo B ne contient aucun son.")

# Couper le son à la durée de la vidéo A
audio = audio.subclipped(0, min(audio.duration, video_a.duration))

# Remplacer l'audio de A
video_finale = video_a.with_audio(audio)

# Export
video_finale.write_videofile(
    OUTPUT,
    codec="libx264",
    audio_codec="aac"
)

# Libération des ressources
video_a.close()
video_b.close()
video_finale.close()

print("✅ Vidéo créée :", OUTPUT)