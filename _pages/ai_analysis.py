import streamlit as st
from PIL import Image
import numpy as np
import cv2
import io
import json


def show():
    """
    AI Analiz sayfası — statik / frontend tasarım
    Bu sayfa demo amaçlıdır ve herhangi bir backend çağrısı yapmaz.
    """

    st.markdown('<div class="fs-h1">AI Analiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="fs-sub">Makine öğrenimi tabanlı analizlerin önizleme tasarımı — bu sayfa statiktir, backend içermez.</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Görüntü yükleyin (AI önizleme)",
        type=["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"],
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file).convert("RGB")
                st.image(image, caption="Yüklenen Görüntü", use_container_width=True)
            except Exception:
                st.error("Görüntü okunamadı")
        else:
            st.info("Görüntü yükleyin veya önizleme sonuçlarını gösterin.")

    with c2:
        st.markdown('<div class="fs-section">AI Ayarları</div>', unsafe_allow_html=True)
        model = st.selectbox("Model", ["DemoNet-V1 (simülasyon)", "SimulateNet-Light (simülasyon)"])
        threshold = st.slider("Manipülasyon eşiği (%)", 0, 100, 50)
        show_saliency = st.checkbox("Saliency haritası (simülasyon)", value=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Önizleme Sonuçları (statik)"):
            # Deterministic demo skor (görüntü mevcutsa boyuta göre küçük varyasyon)
            if uploaded_file is not None:
                w, h = image.size
                score = 0.4 + 0.6 * (((w * h) % 97) / 97)
            else:
                score = 0.62

            percent = int(score * 100)
            verdict = "Şüpheli" if percent >= threshold else "Büyük ihtimal orijinal"

            st.markdown('<hr class="fs-hr">', unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Model", model)
            with m2:
                st.metric("Manipülasyon Skoru", f"{percent}%")
            with m3:
                st.metric("Genel Karar", verdict)

            st.progress(percent / 100)

            st.markdown("<br>", unsafe_allow_html=True)

            # Simüle görsel açıklama
            col_big, col_small = st.columns([2, 1])
            with col_big:
                if uploaded_file is not None and show_saliency:
                    img_np = np.array(image)
                    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
                    heat = cv2.GaussianBlur(gray, (0, 0), sigmaX=15)
                    heat = cv2.normalize(heat, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
                    heat_color = cv2.applyColorMap(heat, cv2.COLORMAP_JET)
                    overlay = cv2.addWeighted(img_np, 0.6, heat_color, 0.4, 0)
                    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
                    st.image(overlay_rgb, caption="Simüle Saliency Haritası", use_container_width=True)
                else:
                    st.info("Saliency haritası için görüntü yükleyin veya simülasyonu etkinleştirin.")

            with col_small:
                st.markdown(f"""<div class="fs-card">
                    <div class="fs-card-title">AI Rapor Özet</div>
                    <div class="fs-info-row"><span class="fs-label">Model</span><span class="fs-value">{model}</span></div>
                    <div class="fs-info-row"><span class="fs-label">Skor</span><span class="fs-value">{percent}%</span></div>
                    <div class="fs-info-row"><span class="fs-label">Eşik</span><span class="fs-value">{threshold}%</span></div>
                </div>""", unsafe_allow_html=True)

            # Hazır raporu indirme
            report = {
                "model": model,
                "score": percent,
                "threshold": threshold,
                "verdict": verdict
            }
            report_json = json.dumps(report, ensure_ascii=False, indent=2)
            st.download_button("Raporu İndir (JSON)", data=report_json, file_name="ai_report.json", mime="application/json")

        st.markdown('<hr class="fs-hr">', unsafe_allow_html=True)
        st.markdown('<div class="fs-sub">Bu sayfa sadece arayüz/demonstrasyon amaçlıdır; gerçek analiz için backend gereklidir.</div>', unsafe_allow_html=True)
