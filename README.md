# ForgeScan

Streamlit tabanlı bir uygulama. Bu dosya, projeyi sıfırdan alan (Git ve Python yüklü olmayan) kullanıcılar için Windows ve macOS adımlarını içerir.

**Önkoşullar**

- Git (https://git-scm.com/)
- Python 3.8 veya daha yeni (https://python.org)
- `pip` (Python ile gelir)

**Not:** Bu proje için bağımlılıklar `requirements.txt` dosyasında listelenmiştir.

---

**Windows (PowerShell - önerilen)**

1. PowerShell'i açın.
2. Git ve Python yüklü değilse kurun (https://git-scm.com/, https://python.org).
3. Aşağıdaki komutları sırasıyla çalıştırın:

```powershell
git clone https://github.com/erenozyurek/ForgeScan.git
cd ForgeScan
py -3 -m venv .venv
# Eğer PowerShell script çalıştırma engeliyse (sadece geçici izin verir):
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

PowerShell yerine CMD kullanıyorsanız:

```cmd
git clone https://github.com/erenozyurek/ForgeScan.git
cd ForgeScan
py -3 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Eğer Git Bash veya WSL kullanıyorsanız (Unix-uyumlu yollar):

```bash
git clone https://github.com/erenozyurek/ForgeScan.git
cd ForgeScan
python3 -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
streamlit run app.py
```

---

**macOS (Terminal)**

1. Terminal'i açın.
2. Eğer Python yüklü değilse Homebrew ile kurabilirsiniz: `brew install python` veya https://python.org'dan kurun.
3. Aşağıdaki komutları sırasıyla çalıştırın:

```bash
git clone https://github.com/erenozyurek/ForgeScan.git
cd ForgeScan
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Uygulama çalıştıktan sonra tarayıcınızda otomatik açılmıyorsa, şu adrese gidin: http://localhost:8501

---

**Çalıştırma (genel)**

- Geliştirme sırasında uygulamayı başlatmak için:

```bash
streamlit run app.py
```

- Web arayüzü genelde `http://localhost:8501` üzerinde erişilir.

**Diğer scriptler (opsiyonel)**

- Veri ön işleme veya modeli eğitmek isterseniz proje kökündeki scriptleri çalıştırabilirsiniz:

```bash
python preprocess_data.py
python train_model.py
```

---

**Yükleme sorunları / ipuçları**

- `opencv-python` gibi paketlerin native bağımlılıkları olabilir; eğer `pip install` sırasında hata alırsanız, Anaconda/Miniconda kullanmayı veya sistem paketlerini (ör. `cmake`) kurmayı deneyin.
- macOS Apple Silicon (M1/M2) kullanıyorsanız bazı paketlerin özel tekerlekleri gerekebilir; hata aldığınız paket için proje sayfasındaki veya hata mesajındaki önerileri kontrol edin.

---

Herhangi bir adımda hata alırsanız, hata çıktısını paylaşın; yardımcı olayım.

