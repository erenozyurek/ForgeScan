import streamlit as st
import os
import numpy as np
import io
from PIL import Image
import tensorflow as tf

# Ayarlar
MODEL_PATH = r"C:\Users\Ercüment Kocaoğlu\Source\Repos\ForgeScan\_pages\model_casia_ela.h5"
IMAGE_SIZE = (128, 128)

def run_ela(image, quality=90):
    """Numpy tabanlı ELA fonksiyonu"""
    try:
        original = image.convert('RGB')
        buffer = io.BytesIO()
        original.save(buffer, 'JPEG', quality=quality)
        buffer.seek(0)
        temporary = Image.open(buffer)
        
        original_array = np.array(original).astype(np.float32)
        temporary_array = np.array(temporary).astype(np.float32)
        
        diff = np.abs(original_array - temporary_array)
        enhanced_diff = diff * 15.0
        enhanced_diff = np.clip(enhanced_diff, 0, 255).astype(np.uint8)
        
        return Image.fromarray(enhanced_diff)
    except:
        return None

# KRİTİK NOKTA: Bu fonksiyonun adı tam olarak 'show' olmalı ve en soldan başlamalıdır.
def show():
    st.title("🔍 Yapay Zeka ile Resim Analizi")
    st.write("Eğitilmiş CNN modelimizi kullanarak resimlerdeki dijital manipülasyon izlerini tespit edin.")

    uploaded_file = st.file_uploader("Bir resim seçin...", type=["jpg", "jpeg", "png", "tif"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Orijinal Resim")
            st.image(image, use_container_width=True)
        
        with col2:
            st.subheader("ELA Görselleştirme")
            ela_img = run_ela(image)
            if ela_img:
                st.image(ela_img, use_container_width=True)

        if st.button("Analizi Başlat"):
            if not os.path.exists(MODEL_PATH):
                st.error(f"Model dosyası bulunamadı! Lütfen '{MODEL_PATH}' dosyasının ana dizinde olduğundan emin olun.")
            else:
                with st.spinner('Yapay zeka inceliyor...'):
                    # Modeli yükle
                    model = tf.keras.models.load_model(MODEL_PATH)
                    
                    # Resmi hazırla
                    ela_processed = ela_img.resize(IMAGE_SIZE)
                    x = np.array(ela_processed).astype('float32') / 255.0
                    x = np.expand_dims(x, axis=0)
                    
                    # Tahmin yap
                    prediction = model.predict(x)
                    class_idx = np.argmax(prediction[0])
                    confidence = prediction[0][class_idx] * 100
                    
                    st.divider()
                    if class_idx == 1:
                        st.error(f"SONUÇ: MANİPÜLE EDİLMİŞ (SAHTE) - Güven Oranı: %{confidence:.2f}")
                    else:
                        st.success(f"SONUÇ: ORİJİNAL (GERÇEK) - Güven Oranı: %{confidence:.2f}")