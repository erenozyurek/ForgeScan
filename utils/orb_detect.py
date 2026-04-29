import cv2
import numpy as np

def detect_orb(image):
    """
    @brief ORB algoritması ile görüntü manipülasyon tespiti yapar
    @param image Analiz edilecek görüntü (numpy array)
    @return result dict: sonuç, keypoint sayısı, görüntü
    """
    
    # Görüntüyü griye çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # ORB oluştur
    orb = cv2.ORB_create(nfeatures=1000)
    
    # Keypoint ve descriptor bul
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    
    # Keypoint sayısına göre karar ver
    keypoint_count = len(keypoints)
    
    # Görüntüyü keypoint ile çiz
    output_image = cv2.drawKeypoints(
        image.copy(),
        keypoints,
        None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )
    
    # Eşik değeri
    if descriptors is not None:
        # Descriptor varyansı hesapla
        variance = np.var(descriptors.astype(np.float32))
        
        # Keypoint response değerlerini analiz et
        responses = [kp.response for kp in keypoints]
        avg_response = np.mean(responses) if responses else 0
        
        if variance > 1200 or avg_response > 0.02:
            status = "⚠️ Manipüle Edilmiş"
            manipulated = True
        else:
            status = "✅ Orijinal"
            manipulated = False
    else:
        status = "❓ Belirlenemedi"
        manipulated = False
        variance = 0
        avg_response = 0
    
    return {
        "algorithm": "ORB",
        "status": status,
        "manipulated": manipulated,
        "keypoint_count": keypoint_count,
        "variance": round(float(variance), 2),
        "avg_response": round(float(avg_response), 4),
        "output_image": output_image
    }