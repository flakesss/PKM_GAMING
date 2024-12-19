import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Fungsi untuk menghasilkan data tanggal dan waktu
def generate_timestamps(start_date, num_samples):
    timestamps = []
    current_time = start_date
    for _ in range(num_samples):
        timestamps.append(current_time.strftime('%Y-%m-%d %H:%M:%S'))  # ISO 8601 format
        # Increment waktu secara acak antara 30 hingga 90 menit
        current_time += timedelta(minutes=np.random.randint(30, 90))
    return timestamps

# Fungsi untuk menentukan label 'Benar' atau 'Salah'
def determine_label(dosing, volume):
    # Definisikan takaran bioflok yang benar berdasarkan volume (dosis per m3)
    toleransi = 0.2

    batas_bawah = {
        'Garam_Krosok (kg)': 1 * (1 - toleransi),
        'Molase (ml)': 100 * (1 - toleransi),
        'Probiotik (ml)': 10 * (1 - toleransi),
        'Kapur_Dolomit (ml)': 50 * (1 - toleransi)
    }

    batas_atas = {
        'Garam_Krosok (kg)': 1 * (1 + toleransi),
        'Molase (ml)': 100 * (1 + toleransi),
        'Probiotik (ml)': 10 * (1 + toleransi),
        'Kapur_Dolomit (ml)': 50 * (1 + toleransi)
    }

    for bahan in dosing:
        if dosing[bahan] < batas_bawah[bahan] * volume or dosing[bahan] > batas_atas[bahan] * volume:
            return 'Salah'
    return 'Benar'

# Fungsi untuk menghasilkan takaran "Benar" dalam rentang yang ditentukan
def generate_benar_takaran(volume_m3):
    return {
        'Garam_Krosok (kg)': np.random.uniform(1 * 0.8, 1 * 1.2) * volume_m3,
        'Molase (ml)': np.random.uniform(100 * 0.8, 100 * 1.2) * volume_m3,
        'Probiotik (ml)': np.random.uniform(10 * 0.8, 10 * 1.2) * volume_m3,
        'Kapur_Dolomit (ml)': np.random.uniform(50 * 0.8, 50 * 1.2) * volume_m3
    }

# Fungsi untuk menghasilkan takaran "Salah" dengan setidaknya satu takaran di luar rentang
def generate_salah_takaran(volume_m3):
    # Pilih bahan secara acak yang akan di luar rentang
    bahan = np.random.choice(['Garam_Krosok (kg)', 'Molase (ml)', 'Probiotik (ml)', 'Kapur_Dolomit (ml)'])
    dosing = {
        'Garam_Krosok (kg)': np.random.uniform(1 * 0.8, 1 * 1.2) * volume_m3,
        'Molase (ml)': np.random.uniform(100 * 0.8, 100 * 1.2) * volume_m3,
        'Probiotik (ml)': np.random.uniform(10 * 0.8, 10 * 1.2) * volume_m3,
        'Kapur_Dolomit (ml)': np.random.uniform(50 * 0.8, 50 * 1.2) * volume_m3
    }
    # Modifikasi salah satu bahan agar berada di luar rentang ±20%
    if np.random.rand() < 0.5:
        # Kurangi dosis menjadi 50% dari optimal
        dosing[bahan] = (dosis_optimal[bahan] * 0.5) * volume_m3
    else:
        # Tingkatkan dosis menjadi 150% dari optimal
        dosing[bahan] = (dosis_optimal[bahan] * 1.5) * volume_m3
    return dosing

# Set seed untuk reproduktibilitas
np.random.seed(42)

# Jumlah sampel
num_samples_total = 100
num_benar = num_salah = num_samples_total // 2  # 50 masing-masing

# Menghasilkan timestamps mulai dari 1 Februari 2024
start_date = datetime(2024, 2, 1)
timestamps_benar = generate_timestamps(start_date, num_benar)
timestamps_salah = generate_timestamps(start_date + timedelta(days=1), num_salah)  # Offset tanggal untuk variasi

# Fungsi untuk menghasilkan karakteristik kolam
def generate_kolam_data(num_samples):
    bentuk_kolam = np.random.choice(['Bulat', 'Kotak'], size=num_samples, p=[0.6, 0.4])
    material_kolam = np.random.choice(['Terpal', 'Beton'], size=num_samples, p=[0.5, 0.5])

    # Dimensi Kolam
    diameter = np.where(bentuk_kolam == 'Bulat',
                        np.round(np.random.uniform(1.0, 5.0, size=num_samples), 4),
                        np.nan)

    panjang = np.where(bentuk_kolam == 'Kotak',
                       np.round(np.random.uniform(1.0, 5.0, size=num_samples), 4),
                       np.nan)

    lebar = np.where(bentuk_kolam == 'Kotak',
                     np.round(np.random.uniform(1.0, 5.0, size=num_samples), 4),
                     np.nan)

    tinggi = np.round(np.random.uniform(0.5, 2.0, size=num_samples), 4)

    # Volume Air (L)
    volume_air = np.where(
        bentuk_kolam == 'Bulat',
        np.round(np.pi * (diameter / 2)**2 * tinggi * 1000, 4),  # dalam liter
        np.round(panjang * lebar * tinggi * 1000, 4)  # dalam liter
    )

    return bentuk_kolam, material_kolam, diameter, panjang, lebar, tinggi, volume_air

# Dosis optimal
dosis_optimal = {
    'Garam_Krosok (kg)': 1,    # kg/m3
    'Molase (ml)': 100,        # ml/m3
    'Probiotik (ml)': 10,      # ml/m3
    'Kapur_Dolomit (ml)': 50    # ml/m3
}

# Menghasilkan data untuk label "Benar"
bentuk_benar, material_benar, diameter_benar, panjang_benar, lebar_benar, tinggi_benar, volume_air_benar = generate_kolam_data(num_benar)
volume_m3_benar = volume_air_benar / 1000  # Konversi liter ke m3

# Menghasilkan takaran "Benar"
dosing_benar = [generate_benar_takaran(v) for v in volume_m3_benar]
garam_benar = [round(d['Garam_Krosok (kg)'], 4) for d in dosing_benar]
molase_benar = [round(d['Molase (ml)'], 4) for d in dosing_benar]
probiotik_benar = [round(d['Probiotik (ml)'], 4) for d in dosing_benar]
kapur_benar = [round(d['Kapur_Dolomit (ml)'], 4) for d in dosing_benar]

data_benar = {
    'Timestamp': timestamps_benar,
    'Bentuk_Kolam': bentuk_benar,
    'Material_Kolam': material_benar,
    'Diameter (m)': diameter_benar,
    'Panjang (m)': panjang_benar,
    'Lebar (m)': lebar_benar,
    'Tinggi (m)': tinggi_benar,
    'Volume_Air (L)': volume_air_benar,
    'Garam_Krosok (kg)': garam_benar,
    'Molase (ml)': molase_benar,
    'Probiotik (ml)': probiotik_benar,
    'Kapur_Dolomit (ml)': kapur_benar,
    'Label': 'Benar'
}

df_benar = pd.DataFrame(data_benar)

# Validasi data "Benar" dengan determine_label
mask_benar = df_benar.apply(lambda row: determine_label(
    {
        'Garam_Krosok (kg)': row['Garam_Krosok (kg)'],
        'Molase (ml)': row['Molase (ml)'],
        'Probiotik (ml)': row['Probiotik (ml)'],
        'Kapur_Dolomit (ml)': row['Kapur_Dolomit (ml)']
    },
    row['Volume_Air (L)'] / 1000
), axis=1) == 'Benar'

df_benar = df_benar[mask_benar]

# Menghasilkan data untuk label "Salah"
bentuk_salah, material_salah, diameter_salah, panjang_salah, lebar_salah, tinggi_salah, volume_air_salah = generate_kolam_data(num_salah)
volume_m3_salah = volume_air_salah / 1000

# Menghasilkan takaran "Salah"
dosing_salah = [generate_salah_takaran(v) for v in volume_m3_salah]
garam_salah = [round(d['Garam_Krosok (kg)'], 4) for d in dosing_salah]
molase_salah = [round(d['Molase (ml)'], 4) for d in dosing_salah]
probiotik_salah = [round(d['Probiotik (ml)'], 4) for d in dosing_salah]
kapur_salah = [round(d['Kapur_Dolomit (ml)'], 4) for d in dosing_salah]

data_salah = {
    'Timestamp': timestamps_salah,
    'Bentuk_Kolam': bentuk_salah,
    'Material_Kolam': material_salah,
    'Diameter (m)': diameter_salah,
    'Panjang (m)': panjang_salah,
    'Lebar (m)': lebar_salah,
    'Tinggi (m)': tinggi_salah,
    'Volume_Air (L)': volume_air_salah,
    'Garam_Krosok (kg)': garam_salah,
    'Molase (ml)': molase_salah,
    'Probiotik (ml)': probiotik_salah,
    'Kapur_Dolomit (ml)': kapur_salah,
    'Label': 'Salah'
}

df_salah = pd.DataFrame(data_salah)

# Validasi data "Salah" dengan determine_label
mask_salah = df_salah.apply(lambda row: determine_label(
    {
        'Garam_Krosok (kg)': row['Garam_Krosok (kg)'],
        'Molase (ml)': row['Molase (ml)'],
        'Probiotik (ml)': row['Probiotik (ml)'],
        'Kapur_Dolomit (ml)': row['Kapur_Dolomit (ml)']
    },
    row['Volume_Air (L)'] / 1000
), axis=1) == 'Salah'

df_salah = df_salah[mask_salah]

# Gabungkan data "Benar" dan "Salah"
df = pd.concat([df_benar, df_salah], ignore_index=True)

# Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Reset index
df = df.reset_index(drop=True)

# Mengganti NaN dengan kosong untuk CSV
df = df.replace({np.nan: ''})

# Menyimpan dataset ke file CSV dengan encoding UTF-8 dan format standar
df.to_csv('dataset_Media_Bioflok_kecil.csv', index=False, encoding='utf-8')

print("Dataset sintetis seimbang dengan label 'Benar' dan 'Salah' (100 sampel) berhasil dibuat dan disimpan sebagai 'dataset_bioflok_terlabel_seimbang_100.csv'")
