import os
import shutil
from datetime import datetime
from PIL import Image
import pytesseract

SOURCE_DIR = 'screenshots'
DEST_DIR = 'sorted'

def get_creation_date(filepath):
    return datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d')

def detect_app_name(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        for app in ["YouTube", "Chrome", "Zoom", "Slack", "VS Code", "Notion"]:
            if app.lower() in text.lower():
                return app
    except:
        pass
    return "Unknown"

def organize_screenshots():
    if not os.path.exists(SOURCE_DIR):
        print("❌ 'screenshots' folder not found.")
        return
    os.makedirs(DEST_DIR, exist_ok=True)

    for file in os.listdir(SOURCE_DIR):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            src_path = os.path.join(SOURCE_DIR, file)
            date_str = get_creation_date(src_path)
            app_name = detect_app_name(src_path)

            target_dir = os.path.join(DEST_DIR, app_name, date_str)
            os.makedirs(target_dir, exist_ok=True)

            shutil.copy(src_path, os.path.join(target_dir, file))
            print(f"✅ {file} → {target_dir}")

if __name__ == "__main__":
    organize_screenshots()
