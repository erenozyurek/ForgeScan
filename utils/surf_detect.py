import cv2
import numpy as np

def _create_detector():
    """Öncelikle SIFT'i dener, bulamazsa ORB'ye geçer."""
    try:
        sift = cv2.SIFT_create()
        return sift, "SIFT"
    except Exception:
        pass
    try:
        orb = cv2.ORB_create(nfeatures=1000)
        return orb, "ORB"
    except Exception:
        pass
    return None, None

def detect_forgery_feature_based(image):
    if image is None:
        return {"status": "❌ Geçersiz görüntü", "manipulated": False}

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector, used_algo = _create_detector()

    if detector is None:
        return {"status": "❌ Detector bulunamadı", "manipulated": False}

    keypoints, descriptors = detector.detectAndCompute(gray, None)
    
    if descriptors is None or len(keypoints) < 10:
        # Puan bulutunu çizip dönelim
        output_image = cv2.drawKeypoints(image.copy(), keypoints or [], None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return {
            "used_algorithm": used_algo,
            "status": "✅ Orijinal (Yeterli eşleşme noktası yok)",
            "manipulated": False,
            "keypoint_count": len(keypoints) if keypoints else 0,
            "suspicious_match_count": 0,
            "variance": "-",
            "output_image": output_image
        }

    # Öncelikle "baloncuklu" yapıyı, yani puan bulutunu çizelim.
    point_cloud_image = cv2.drawKeypoints(image.copy(), keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    norm_type = cv2.NORM_HAMMING if used_algo == "ORB" else cv2.NORM_L2
    matcher = cv2.BFMatcher(norm_type, crossCheck=False)
    
    # K=3 MANTIĞI: m=kendisi, n=kopya adayı, p=alakasız nokta
    matches = matcher.knnMatch(descriptors, descriptors, k=3)

    good_matches = []
    # Lowe's Ratio Test
    for match in matches:
        if len(match) == 3:
            m, n, p = match
            
            # Kopya adayı (n), alakasız noktadan (p) bariz şekilde daha iyi bir eşleşmeyse
            if n.distance < 0.75 * p.distance:
                pt1 = np.array(keypoints[n.queryIdx].pt)
                pt2 = np.array(keypoints[n.trainIdx].pt)
                
                # Fiziksel piksel mesafesini ölç
                dist = np.linalg.norm(pt1 - pt2)
                
                # Eğer aynı doku 50 pikselden daha uzak bir yerde de varsa, kopyadır!
                if dist > 50.0:
                    good_matches.append(n)

    # Baloncuklu resmin üzerine kopyalama çizgilerini çizeceğiz.
    output_image = point_cloud_image.copy() 
    
    for match in good_matches:
        pt1 = tuple(map(int, keypoints[match.queryIdx].pt))
        pt2 = tuple(map(int, keypoints[match.trainIdx].pt))
        cv2.line(output_image, pt1, pt2, (0, 0, 255), 2) # Kırmızı çizgi ile kopyalanan yerleri bağla
        cv2.circle(output_image, pt1, 5, (0, 255, 0), -1)
        cv2.circle(output_image, pt2, 5, (0, 255, 0), -1)

    match_count = len(good_matches)
    manipulated = match_count > 10
    status = "⚠️ Manipüle Edilmiş (Kopyala-Yapıştır Tespit Edildi)" if manipulated else "✅ Orijinal"

    return {
        "used_algorithm": used_algo,
        "status": status,
        "manipulated": manipulated,
        "keypoint_count": len(keypoints),
        "suspicious_match_count": match_count,
        "variance": "-",
        "output_image": output_image
    }