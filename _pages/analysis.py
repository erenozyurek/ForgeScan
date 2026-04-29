import streamlit as st
import cv2
import numpy as np
from PIL import Image

from utils.sift_detect import detect_sift
from utils.surf_detect import detect_surf
from utils.akaze_detect import detect_akaze
from utils.orb_detect import detect_orb

def show():
    """
    @brief Analiz ve sonuçlar sayfası
    """

    st.markdown('<div class="fs-h1">Görüntü Analizi</div>', unsafe_allow_html=True)
    st.markdown('<div class="fs-sub">Görüntünüzü yükleyin, algoritma seçin ve analizi başlatın.</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Görüntü yükleyin",
        type=["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"],
        help="JPG, PNG, GIF, BMP, TIFF, WEBP"
    )

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        uploaded_file.seek(0)
        pil_image = Image.open(uploaded_file)

        st.markdown('<hr class="fs-hr">', unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            st.image(pil_image, caption="Yüklenen Görüntü", use_container_width=True)
        with c2:
            fmt = pil_image.format if pil_image.format else uploaded_file.type
            kb = uploaded_file.size / 1024
            st.markdown(f"""<div class="fs-card">
                <div class="fs-section" style="margin-bottom:12px;">Dosya Bilgileri</div>
                <div class="fs-info-row"><span class="fs-label">Ad</span><span class="fs-value">{uploaded_file.name}</span></div>
                <div class="fs-info-row"><span class="fs-label">Format</span><span class="fs-value">{fmt}</span></div>
                <div class="fs-info-row"><span class="fs-label">Çözünürlük</span><span class="fs-value">{pil_image.size[0]} × {pil_image.size[1]} px</span></div>
                <div class="fs-info-row"><span class="fs-label">Mod</span><span class="fs-value">{pil_image.mode}</span></div>
                <div class="fs-info-row"><span class="fs-label">Boyut</span><span class="fs-value">{kb:.1f} KB</span></div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="fs-hr">', unsafe_allow_html=True)
        st.markdown('<div class="fs-section">Algoritma Seçimi</div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            use_sift = st.checkbox("SIFT", value=True)
        with c2:
            use_surf = st.checkbox("SURF", value=True)
        with c3:
            use_akaze = st.checkbox("AKAZE", value=True)
        with c4:
            use_orb = st.checkbox("ORB", value=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Analizi Başlat"):
            results = {}
            with st.spinner("Analiz yapılıyor..."):
                if use_sift:
                    results["SIFT"] = detect_sift(image)
                if use_surf:
                    try:
                        results["SURF"] = detect_surf(image)
                    except Exception:
                        st.warning("SURF kullanılamadı — opencv-contrib-python gerekli.")
                if use_akaze:
                    results["AKAZE"] = detect_akaze(image)
                if use_orb:
                    results["ORB"] = detect_orb(image)

            if results:
                st.markdown('<hr class="fs-hr">', unsafe_allow_html=True)
                st.markdown('<div class="fs-section">Sonuçlar</div>', unsafe_allow_html=True)

                manipulated_count = sum(1 for r in results.values() if r["manipulated"])
                total_count = len(results)
                clean_count = total_count - manipulated_count

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"""<div class="fs-metric-card">
                        <div class="fs-metric-num">{total_count}</div>
                        <div class="fs-metric-label">Toplam Algoritma</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    color = "#f97316" if manipulated_count > 0 else "#71717a"
                    st.markdown(f"""<div class="fs-metric-card">
                        <div class="fs-metric-num" style="color:{color}">{manipulated_count}</div>
                        <div class="fs-metric-label">Manipülasyon Tespit Eden</div>
                    </div>""", unsafe_allow_html=True)
                with c3:
                    color2 = "#4ade80" if clean_count > 0 else "#71717a"
                    st.markdown(f"""<div class="fs-metric-card">
                        <div class="fs-metric-num" style="color:{color2}">{clean_count}</div>
                        <div class="fs-metric-label">Temiz Bulan</div>
                    </div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Genel karar
                if manipulated_count >= total_count / 2:
                    st.markdown("""<div class="fs-verdict-warn">
                        <div class="fs-verdict-title">⚠ Bu görüntü manipüle edilmiş olabilir</div>
                        <div class="fs-verdict-desc">Algoritmaların çoğunluğu sahteciliğe işaret ediyor.</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""<div class="fs-verdict-safe">
                        <div class="fs-verdict-title">✓ Bu görüntü büyük ihtimalle orijinaldir</div>
                        <div class="fs-verdict-desc">Algoritmaların çoğunluğu manipülasyon tespit etmedi.</div>
                    </div>""", unsafe_allow_html=True)

                st.markdown('<hr class="fs-hr">', unsafe_allow_html=True)
                st.markdown('<div class="fs-section">Algoritma Detayları</div>', unsafe_allow_html=True)

                for algo, result in results.items():
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        out_rgb = cv2.cvtColor(result["output_image"], cv2.COLOR_BGR2RGB)
                        st.image(out_rgb, caption=f"{algo} — Keypoint Haritası", use_container_width=True)
                    with c2:
                        badge_cls = "fs-status-warn" if result["manipulated"] else "fs-status-ok"
                        prog_cls = "fs-progress-warn" if result["manipulated"] else "fs-progress-ok"
                        prog_val = 75 if result["manipulated"] else 20

                        extra = ""
                        if "avg_response" in result:
                            extra = f'<div class="fs-info-row"><span class="fs-label">Ort. Response</span><span class="fs-value">{result["avg_response"]}</span></div>'

                        st.markdown(f"""<div class="fs-card">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                                <span class="fs-card-title" style="margin:0">{algo}</span>
                                <span class="{badge_cls}">{result['status']}</span>
                            </div>
                            <div class="fs-progress"><div class="{prog_cls}" style="width:{prog_val}%"></div></div>
                            <div style="margin-top:12px;">
                                <div class="fs-info-row"><span class="fs-label">Keypoint</span><span class="fs-value">{result['keypoint_count']}</span></div>
                                <div class="fs-info-row"><span class="fs-label">Varyans</span><span class="fs-value">{result['variance']}</span></div>
                                {extra}
                            </div>
                        </div>""", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="fs-empty">
            <div class="fs-empty-icon">📁</div>
            <div class="fs-empty-title">Henüz görüntü yüklenmedi</div>
            <div class="fs-empty-desc">JPG, PNG, GIF, BMP, TIFF, WEBP formatları desteklenir</div>
        </div>""", unsafe_allow_html=True)