import streamlit as st

def show():
    """
    @brief Ana sayfa görünümü
    """

    st.markdown('<div class="fs-h1">Görüntü Sahteciliği Tespiti</div>', unsafe_allow_html=True)
    st.markdown('<div class="fs-sub">Yüklediğiniz görselleri SIFT, SURF, AKAZE ve ORB algoritmaları ile analiz edin.</div>', unsafe_allow_html=True)

    # Nasıl Çalışır
    st.markdown('<div class="fs-section">Nasıl Çalışır</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="fs-card">
            <div class="fs-step">1</div>
            <div class="fs-card-title">Görüntü Yükle</div>
            <div class="fs-card-desc">JPEG, PNG, WEBP ve diğer yaygın formatları destekler.</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="fs-card">
            <div class="fs-step">2</div>
            <div class="fs-card-title">Algoritma Seç</div>
            <div class="fs-card-desc">Dört farklı algoritma ile kapsamlı analiz başlatın.</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="fs-card">
            <div class="fs-step">3</div>
            <div class="fs-card-title">Sonuçları İncele</div>
            <div class="fs-card-desc">Detaylı rapor ve keypoint haritası ile karar verin.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="fs-hr">', unsafe_allow_html=True)

    # Algoritmalar
    st.markdown('<div class="fs-section">Algoritmalar</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="fs-card">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <div class="fs-algo-badge">S</div>
                <div class="fs-algo-name">SIFT</div>
            </div>
            <div class="fs-card-desc">Scale Invariant Feature Transform — ölçek ve rotasyondan bağımsız anahtar nokta tespiti.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div class="fs-card">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <div class="fs-algo-badge">A</div>
                <div class="fs-algo-name">AKAZE</div>
            </div>
            <div class="fs-card-desc">Accelerated KAZE — binary descriptor kullanan, gürültüye dayanıklı modern algoritma.</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="fs-card">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <div class="fs-algo-badge">U</div>
                <div class="fs-algo-name">SURF</div>
            </div>
            <div class="fs-card-desc">Speeded Up Robust Features — SIFT'e benzer ancak çok daha hızlı, gerçek zamanlı uygulamalar için ideal.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div class="fs-card">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <div class="fs-algo-badge">O</div>
                <div class="fs-algo-name">ORB</div>
            </div>
            <div class="fs-card-desc">Oriented FAST and Rotated BRIEF — açık kaynaklı, hızlı ve ticari kullanıma uygun alternatif.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="fs-hr">', unsafe_allow_html=True)

    # Formatlar
    st.markdown('<div class="fs-section">Desteklenen Formatlar</div>', unsafe_allow_html=True)
    st.markdown("""<div>
        <span class="fs-tag">JPEG</span><span class="fs-tag">PNG</span><span class="fs-tag">GIF</span>
        <span class="fs-tag">BMP</span><span class="fs-tag">TIFF</span><span class="fs-tag">WEBP</span>
    </div>""", unsafe_allow_html=True)