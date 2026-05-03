# bike-sharing-analytics-dashboard
An end-to-end data analysis project on the Bike Sharing Dataset, combining deep EDA with an interactive Streamlit dashboard. It utilizes advanced visualizations to reveal complex rental patterns and external influences for data-driven decision-making.
=======
# 🚲 Bike Sharing Analytics Dashboard

Dashboard interaktif untuk menganalisis pola peminjaman sepeda dari sistem **Capital Bikeshare**, Washington D.C. periode 2011-2012. Dibangun menggunakan Streamlit dengan visualisasi berbasis Matplotlib dan Seaborn.

Proyek ini merupakan submission akhir kursus [Belajar Fundamental Analisis Data](https://www.dicoding.com/academies/555/corridor) dari Dicoding, bagian dari program **Coding Camp powered by DBS Foundation**.

## 📁 Struktur Proyek

```
submission
├───dashboard
|   ├───day.csv
|   ├───hour.csv
|   └───dashboard.py
├───data
|   ├───day.csv
|   └───hour.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## 📊 Dataset

Dataset berasal dari [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset) yang dikumpulkan oleh Hadi Fanaee-T dari Universitas Porto.

| File | Granularitas | Jumlah Record |
|---|---|---|
| `day.csv` | Harian | 731 hari |
| `hour.csv` | Per jam | 17.379 jam |

**Variabel utama:**

| Kolom | Deskripsi |
|---|---|
| `dteday` | Tanggal |
| `season` | Musim (1=Spring, 2=Summer, 3=Fall, 4=Winter) |
| `weathersit` | Kondisi cuaca (1=Clear s.d. 4=Heavy Rain) |
| `temp` | Suhu ternormalisasi (x41 untuk °C) |
| `hum` | Kelembaban ternormalisasi (x100 untuk %) |
| `windspeed` | Kecepatan angin ternormalisasi (x67 untuk km/h) |
| `casual` | Jumlah peminjam non-member |
| `registered` | Jumlah peminjam member |
| `cnt` | Total peminjaman |

## 🔍 Pertanyaan Analisis

Dashboard ini dirancang untuk menjawab dua pertanyaan utama:

1. **Bagaimana pola peminjaman sepeda berdasarkan waktu?**
   Meliputi tren bulanan, perbedaan hari kerja vs akhir pekan, dan pola per jam dalam sehari.

2. **Faktor apa saja yang paling memengaruhi jumlah peminjaman sepeda?**
   Meliputi pengaruh musim, kondisi cuaca, suhu, kelembaban, dan segmentasi pengguna.

## 📈 Visualisasi

| # | Judul | Tipe |
|---|---|---|
| 1 | Tren Total Peminjaman per Bulan (2011 vs 2012) | Line Chart |
| 2 | Rata-rata Peminjaman per Musim | Horizontal Bar |
| 3 | Pola Peminjaman per Jam (Hari Kerja vs Akhir Pekan) | Line Chart |
| 4 | Rata-rata Peminjaman per Hari dalam Seminggu | Bar Chart |
| 5 | Pengaruh Kondisi Cuaca terhadap Peminjaman | Bar Chart + Error Bar |
| 6 | Hubungan Suhu dan Jumlah Peminjaman | Scatter Plot + Regresi |
| 7 | Tren Casual vs Registered per Bulan | Stacked Area Chart |
| 8 | Matriks Korelasi Variabel Utama | Heatmap |
| 9 | Heatmap Peminjaman: Jam x Hari dalam Seminggu | Heatmap |

## 🚀 Cara Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/username/bike-sharing-dashboard.git
cd bike-sharing-dashboard
```

### 2. Buat Virtual Environment (opsional tapi disarankan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`.

## 📦 Dependensi

| Library | Versi Minimum | Kegunaan |
|---|---|---|
| `streamlit` | 1.32.0 | Framework dashboard |
| `pandas` | 2.0.0 | Manipulasi data |
| `matplotlib` | 3.7.0 | Visualisasi utama |
| `seaborn` | 0.13.0 | Heatmap & statistik |
| `numpy` | 1.24.0 | Komputasi numerik |

## ✨ Fitur Dashboard

- **Filter Interaktif** - Sidebar dengan filter tahun, musim, dan kondisi cuaca. Semua visualisasi update secara reaktif.
- **KPI Cards** - Ringkasan total peminjaman, rata-rata harian, puncak harian, dan persentase pengguna registered.
- **Insight Otomatis** - Kartu temuan utama yang menampilkan jam puncak, musim terbaik, dan pertumbuhan year-over-year secara dinamis.

## 💡 Insight Utama

- Peminjaman di **2012 tumbuh sekitar 65%** dibanding 2011, menandakan adopsi layanan yang cepat.
- Pola hari kerja membentuk **dua puncak** (08:00 dan 17:00), mencerminkan penggunaan untuk commuting.
- Pola akhir pekan membentuk **satu puncak** di sekitar pukul 13:00, mencerminkan penggunaan rekreasi.
- **Musim gugur (Fall)** secara konsisten mencatat rata-rata peminjaman tertinggi.
- **Suhu** adalah faktor lingkungan yang paling berkorelasi positif dengan jumlah peminjaman.
- Pengguna **registered** mendominasi lebih dari 75% total peminjaman di sepanjang periode.

## 📚 Referensi

Fanaee-T, Hadi, and Gama, Joao. *"Event labeling combining ensemble detectors and background knowledge"*. Progress in Artificial Intelligence (2013): pp. 1-15, Springer Berlin Heidelberg. [doi:10.1007/s13748-013-0040-3](https://doi.org/10.1007/s13748-013-0040-3)

## 👤 Penulis

**Satrio Budi Pratama**  
Submission akhir kursus Belajar Fundamental Analisis Data, Dicoding  
Coding Camp powered by DBS Foundation
