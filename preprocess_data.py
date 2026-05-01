import os
from PIL import Image, ImageChops
from tqdm import tqdm
import io
import numpy as np # En uste eklemeyi unutma

# Settings
RAW_PATH = os.path.join("data", "raw", "CASIA2")
PROCESSED_PATH = os.path.join("data", "processed")
IMAGE_SIZE = (128, 128)



def run_ela(image, quality=90):
    try:
        # Orijinal resmi RGB yap
        original = image.convert('RGB')
        
        # JPEG olarak gecici kaydet ve geri ac
        buffer = io.BytesIO()
        original.save(buffer, 'JPEG', quality=quality)
        buffer.seek(0)
        temporary = Image.open(buffer)
        
        # Resimleri Numpy dizisine cevir (Matematiksel islem icin)
        original_array = np.array(original).astype(np.float32)
        temporary_array = np.array(temporary).astype(np.float32)
        
        # Mutlak farki al (ELA'nin asli budur)
        diff = np.abs(original_array - temporary_array)
        
        # Farki gorunur kilmak icin parlakligi artir (Carpma islemi)
        # 15.0 degeri genelde idealdir, gerekirse artirilabilir
        enhanced_diff = diff * 15.0
        
        # Degerleri 0-255 arasina kisitla ve tekrar resme cevir
        enhanced_diff = np.clip(enhanced_diff, 0, 255).astype(np.uint8)
        ela_image = Image.fromarray(enhanced_diff)
        
        return ela_image
    except Exception:
        return None

def preprocess():
    for folder in ["Au", "Tp"]:
        p = os.path.join(PROCESSED_PATH, folder)
        if not os.path.exists(p):
            os.makedirs(p)

    for category in ["Au", "Tp"]:
        print(f"Processing: {category}")
        source_dir = os.path.join(RAW_PATH, category)
        target_dir = os.path.join(PROCESSED_PATH, category)
        
        if not os.path.exists(source_dir):
            print(f"Directory not found: {source_dir}")
            continue

        files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.png', '.tif', '.jpeg'))]
        
        for filename in tqdm(files):
            save_path = os.path.join(target_dir, filename.split('.')[0] + ".png")
            
            if os.path.exists(save_path):
                continue

            try:
                img_path = os.path.join(source_dir, filename)
                img = Image.open(img_path).convert('RGB')
                ela_img = run_ela(img)
                if ela_img:
                    ela_img = ela_img.resize(IMAGE_SIZE)
                    ela_img.save(save_path)
            except:
                continue

if __name__ == "__main__":
    preprocess()