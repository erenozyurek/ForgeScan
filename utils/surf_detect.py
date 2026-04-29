import cv2
import numpy as np


def _create_detector():
    """Try to create SURF; if unavailable, try SIFT then ORB as fallbacks.
    Returns (detector, name) or (None, None) if none available.
    """
    # SURF (requires opencv-contrib)
    try:
        surf = cv2.xfeatures2d.SURF_create(400)
        return surf, "SURF"
    except Exception:
        pass

    # SIFT (may be available in many opencv builds)
    try:
        sift = cv2.SIFT_create()
        return sift, "SIFT"
    except Exception:
        pass

    # ORB as a last-resort fallback
    try:
        orb = cv2.ORB_create(nfeatures=1000)
        return orb, "ORB"
    except Exception:
        pass

    return None, None


def detect_surf(image):
    """
    @brief SURF (ve/veya fallback) ile görüntü manipülasyon tespiti yapar
    @param image Analiz edilecek görüntü (numpy array)
    @return result dict: sonuç, keypoint sayısı, görüntü ve kullanılan alg.
    """

    requested_algorithm = "SURF"

    # Güvenli girdi kontrolü
    if image is None:
        return {
            "algorithm": requested_algorithm,
            "used_algorithm": None,
            "available": False,
            "status": "❌ Geçersiz görüntü (None)",
            "manipulated": False,
            "keypoint_count": 0,
            "variance": 0,
            "output_image": None,
            "suggested_command": "pip install opencv-contrib-python"
        }

    # Görüntüyü griye çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    detector, used_algo = _create_detector()

    if detector is None:
        # Hem SURF hem de fallback bulunamadı
        return {
            "algorithm": requested_algorithm,
            "used_algorithm": None,
            "available": False,
            "status": "❌ SURF ve fallback detectorlar bulunamadı",
            "manipulated": False,
            "keypoint_count": 0,
            "variance": 0,
            "output_image": image.copy(),
            "suggested_command": "pip install opencv-contrib-python"
        }

    # Keypoint ve descriptor bul
    keypoints, descriptors = detector.detectAndCompute(gray, None)
    keypoints = keypoints or []
    keypoint_count = len(keypoints)

    # Görüntüyü keypoint ile çiz
    output_image = cv2.drawKeypoints(
        image.copy(),
        keypoints,
        None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    # Descriptor analizi
    if descriptors is not None:
        try:
            descriptors_f = descriptors.astype(np.float32)
        except Exception:
            descriptors_f = np.array(descriptors, dtype=np.float32)

        variance = float(np.var(descriptors_f))

        # Basit heuristic eşikleri: fallback'a göre farklı davran
        if used_algo == "SURF":
            manipulated = variance > 0.02
        elif used_algo == "SIFT":
            manipulated = variance > 1500
        else:  # ORB
            manipulated = variance > 1200

        status = "⚠️ Manipüle Edilmiş" if manipulated else "✅ Orijinal"
    else:
        variance = 0.0
        manipulated = False
        status = "❓ Belirlenemedi"

    return {
        "algorithm": requested_algorithm,
        "used_algorithm": used_algo,
        "available": True,
        "status": status,
        "manipulated": manipulated,
        "keypoint_count": keypoint_count,
        "variance": round(float(variance), 4),
        "output_image": output_image
    }