import pandas as pd

# Membaca dataset yang telah dihasilkan
df = pd.read_csv('dataset_Media_Bioflok.csv')

# Definisikan dosis optimal per m3
dosis_optimal = {
    'Garam_Krosok (kg)': 1,    # kg/m3
    'Molase (ml)': 100,        # ml/m3
    'Probiotik (ml)': 10,      # ml/m3
    'Kapur_Dolomit (ml)': 50    # ml/m3
}

# Definisikan toleransi
toleransi = 0.2  # ±20%

# Fungsi untuk memeriksa apakah dosing berada dalam rentang yang benar
def check_benar(row):
    volume_m3 = row['Volume_Air (L)'] / 1000  # Konversi liter ke m3
    for bahan, optimal in dosis_optimal.items():
        dosis = row[bahan]
        batas_bawah = optimal * (1 - toleransi) * volume_m3
        batas_atas = optimal * (1 + toleransi) * volume_m3
        if not (batas_bawah <= dosis <= batas_atas):
            return False
    return True

# Fungsi untuk memeriksa apakah setidaknya satu dosing di luar rentang yang benar
def check_salah(row):
    volume_m3 = row['Volume_Air (L)'] / 1000  # Konversi liter ke m3
    for bahan, optimal in dosis_optimal.items():
        dosis = row[bahan]
        batas_bawah = optimal * (1 - toleransi) * volume_m3
        batas_atas = optimal * (1 + toleransi) * volume_m3
        if dosis < batas_bawah or dosis > batas_atas:
            return True
    return False

# Tambahkan kolom validasi
df['Validasi'] = df.apply(
    lambda row: 'Valid' if (
        (row['Label'] == 'Benar' and check_benar(row)) or 
        (row['Label'] == 'Salah' and check_salah(row))
    ) else 'Invalid',
    axis=1
)

# Tampilkan hasil validasi
print(df['Validasi'].value_counts())

# Tampilkan sampel yang invalid jika ada
invalid_samples = df[df['Validasi'] == 'Invalid']
if not invalid_samples.empty:
    print("Sampel yang tidak valid ditemukan:")
    print(invalid_samples)
else:
    print("Semua sampel valid sesuai dengan label yang diberikan.")
