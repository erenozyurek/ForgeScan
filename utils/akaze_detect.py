import cv2
import numpy as np

def detect_akaze(image):
    """
    @brief AKAZE algoritması ile kopyala-yapıştır görüntü manipülasyon tespiti yapar
    @param image Analiz edilecek görüntü (numpy array)
    @return result dict: sonuç, keypoint sayısı, şüpheli eşleşme ve görüntü
    """
    
    if image is None:
        return {"algorithm": "AKAZE", "status": "❌ Geçersiz görüntü", "manipulated": False}

    # Görüntüyü griye çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # AKAZE oluştur
    akaze = cv2.AKAZE_create()
    
    # Keypoint ve descriptor bul
    keypoints, descriptors = akaze.detectAndCompute(gray, None)
    
    # Eğer resim çok düzse (yeterli özellik yoksa) direkt temiz dön
    if descriptors is None or len(keypoints) < 10:
        output_image = cv2.drawKeypoints(image.copy(), keypoints or [], None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return {
            "algorithm": "AKAZE",
            "status": "✅ Orijinal (Yeterli eşleşme noktası yok)",
            "manipulated": False,
            "keypoint_count": len(keypoints) if keypoints else 0,
            "suspicious_match_count": 0,
            "variance": "-",
            "output_image": output_image
        }

    # 1. Aşama: Orijinal resmin üzerine "baloncuklu" puan bulutunu çiz (Algoritmanın nereye baktığını gösterir)
    point_cloud_image = cv2.drawKeypoints(image.copy(), keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # 2. Aşama: Noktaları kendi aralarında eşleştir (Klonlama Tespiti)
    # AKAZE binary descriptor ürettiği için NORM_HAMMING kullanıyoruz
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

    # YENİ MANTIK: Sadece k=3 yapıyoruz (Gereksiz k=2 çağrısını sildik)
    # m = kendisi, n = kopya adayı, p = arka plandaki alakasız nokta
    matches = matcher.knnMatch(descriptors, descriptors, k=3)

    good_matches = []
    for match in matches:
        if len(match) == 3:
            m, n, p = match
            
            # Lowe's Ratio Test: Kopya adayı (n), alakasız noktadan (p) bariz şekilde daha iyi bir eşleşmeyse
            if n.distance < 0.75 * p.distance:
                # N'nin (kopya adayının) koordinatlarını alıyoruz
                pt1 = np.array(keypoints[n.queryIdx].pt)
                pt2 = np.array(keypoints[n.trainIdx].pt)
                
                # Fiziksel mesafeyi ölç
                dist = np.linalg.norm(pt1 - pt2)
                
                # Eğer aynı doku 50 pikselden daha uzak bir yerde de varsa, kopyadır!
                if dist > 50.0:
                    good_matches.append(n)

    # 3. Aşama: Baloncuklu resmin üzerine kopyalama çizgilerini (kırmızı) çiz
    output_image = point_cloud_image.copy()
    for match in good_matches:
        pt1 = tuple(map(int, keypoints[match.queryIdx].pt))
        pt2 = tuple(map(int, keypoints[match.trainIdx].pt))
        cv2.line(output_image, pt1, pt2, (0, 0, 255), 2)
        cv2.circle(output_image, pt1, 5, (0, 255, 0), -1)
        cv2.circle(output_image, pt2, 5, (0, 255, 0), -1)

    # Eşik değeri: 10'dan fazla klonlanmış bölge varsa alarm ver
    match_count = len(good_matches)
    manipulated = match_count > 10
    status = "⚠️ Manipüle Edilmiş" if manipulated else "✅ Orijinal"

    return {
        "algorithm": "AKAZE",
        "status": status,
        "manipulated": manipulated,
        "keypoint_count": len(keypoints),
        "suspicious_match_count": match_count,
        "variance": "-",
        "output_image": output_image
    }