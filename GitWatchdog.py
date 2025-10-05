import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from datetime import datetime

PATH = r"C:\python_control"
BRANCH = "test"
TEXT_EXTENSIONS = {".py", ".txt", ".md", ".json", ".cfg", ".ini"}  # только текстовые файлы

class Watcher(FileSystemEventHandler):
    def update_text_files(self):
        for root, dirs, files in os.walk(PATH):
            if ".git" in dirs:
                dirs.remove(".git")
            for file in files:
                filepath = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                if ext not in TEXT_EXTENSIONS:
                    continue
                try:
                    with open(filepath, "a", encoding="utf-8") as f:
                        f.write(f"\n# synced: {datetime.now().isoformat()}")
                except Exception as e:
                    print(f"Не удалось обновить файл {filepath}: {e}")

    def on_any_event(self, event):
        print("Начинаем синхронизацию всех текстовых файлов...")
        os.chdir(PATH)
        self.update_text_files()

        subprocess.run(["git", "checkout", BRANCH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "add", "-A"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", "Полная авто-синхронизация"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "push", "--force", "origin", BRANCH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Синхронизация завершена!")

if __name__ == "__main__":
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, PATH, recursive=True)
    observer.start()
    print(f"Синхронизация папки '{PATH}' с веткой '{BRANCH}' запущена...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

