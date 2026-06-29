import time
import datetime
import threading
import subprocess
import random
from flask import Flask, request, jsonify

from core.driver import create_driver
from utils.posterVideo import poster_video
from utils.scroll_tiktok import scroll_tiktok
from utils.likes import like

app = Flask(__name__)

scheduled_tasks = []
task_lock = threading.Lock()

def transfer_video_to_phone(video_path, phone_path="/sdcard/DCIM/Camera/"):
    """Transfère la vidéo sur le téléphone via ADB"""
    try:
        print(f"📤 Transfert de {video_path} vers le téléphone...")
        result = subprocess.run(["adb", "push", video_path, phone_path], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Vidéo transférée avec succès")
            return True
        else:
            print(f"❌ Erreur ADB: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erreur transfert: {e}")
        return False

def human_like_activity(driver, duration_minutes=4):
    """Activité humaine réaliste avant publication"""
    print(f"🤖 Début activité humaine ({duration_minutes} min)...")
    end_time = time.time() + (duration_minutes * 60)
    
    while time.time() < end_time:
        # Scroll
        scrolls = random.randint(3, 7)
        scroll_tiktok(driver, nb_scrolls=scrolls, pause=random.uniform(2.5, 5))
        
        # Like aléatoire
        if random.random() < 0.35:
            try:
                like(driver)
                time.sleep(random.uniform(1.5, 4))
            except:
                pass
                
        time.sleep(random.uniform(4, 12))  # Pause humaine
    
    print("✅ Activité humaine terminée.")

def process_task(task):
    """Exécute la tâche complète"""
    try:
        with task_lock:
            if task in scheduled_tasks:
                scheduled_tasks.remove(task)
        
        print(f"\n🚀 Lancement publication : {task.get('title')}")
        
        # Transfert vidéo
        if not transfer_video_to_phone(task['video_path']):
            return
        
        # Lancement TikTok + activité humaine
        driver = create_driver()
        duration_minutes = random.randint(3, 17)
        human_like_activity(driver, duration_minutes)
        
        # Publication
        description = task.get('description') or task.get('title', '')
        hashtags = task.get('hashtags', [])
        
        poster_video(driver, description=description, hashtags=hashtags)
        print("🎉 Publication terminée avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur globale: {e}")
    finally:
        if 'driver' in locals():
            try:
                driver.quit()
            except:
                pass

def scheduler():
    """Surveille les tâches"""
    while True:
        now = datetime.datetime.now()
        with task_lock:
            for task in scheduled_tasks[:]:
                task_time = datetime.datetime.fromisoformat(task['scheduled_time'])
                if task_time - now <= datetime.timedelta(minutes=6):
                    threading.Thread(target=process_task, args=(task,), daemon=True).start()
        time.sleep(20)

@app.route('/schedule', methods=['POST'])
def schedule_upload():
    data = request.json
    required = ['video_path', 'scheduled_time']
    
    if not all(k in data for k in required):
        return jsonify({"error": "video_path et scheduled_time requis"}), 400
    
    task = {
        "id": len(scheduled_tasks) + 1,
        "video_path": data['video_path'],
        "title": data.get('title', 'Vidéo sans titre'),
        "description": data.get('description', ''),
        "hashtags": data.get('hashtags', []),
        "scheduled_time": data['scheduled_time']
    }
    
    with task_lock:
        scheduled_tasks.append(task)
    
    return jsonify({
        "status": "success",
        "message": f"Upload planifié pour {task['scheduled_time']}",
        "task_id": task["id"]
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(scheduled_tasks)

if __name__ == '__main__':
    threading.Thread(target=scheduler, daemon=True).start()
    print("🌐 Orchestrateur Tikmium démarré → http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)