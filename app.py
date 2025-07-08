import streamlit as st
import pandas as pd
import time

# --- FASE 1: Placeholder untuk Model Prediksi Penyakit ---
# Di aplikasi nyata, Anda akan memuat model yang sudah dilatih.
# Contoh: from joblib import load; model = load('model_prediksi_penyakit.pkl')


def predict_disease(age, gender, symptoms, blood_pressure):
    """
    Fungsi placeholder untuk memprediksi penyakit.
    Logika di sini HANYA untuk demonstrasi. Ganti dengan pemanggilan model ML Anda.
    """
    # Logika sederhana berbasis aturan sebagai pengganti model ML
    symptoms_set = set(symptoms)
    if "Nyeri Dada" in symptoms_set and "Sesak Napas" in symptoms_set and age > 40:
        return "Penyakit Jantung Koroner", 0.85
    elif "Sering Haus" in symptoms_set and "Sering Buang Air Kecil" in symptoms_set and blood_pressure > 130:
        return "Diabetes Mellitus Tipe 2", 0.78
    elif "Demam Tinggi" in symptoms_set and "Nyeri Sendi" in symptoms_set and "Bintik Merah" in symptoms_set:
        return "Demam Berdarah Dengue", 0.92
    elif "Batuk" in symptoms_set and "Demam Ringan" in symptoms_set:
        return "Infeksi Saluran Pernapasan Akut (ISPA)", 0.65
    else:
        return "Kondisi Tidak Teridentifikasi", 0.30


# --- FASE 2: Placeholder untuk Database Tarif INA-CBGs ---
# Di aplikasi nyata, ini bisa dimuat dari file CSV atau database.
INA_CBG_DATABASE = {
    "Penyakit Jantung Koroner": {"kode": "J-1-23-I", "tarif_jkn": 50000000},
    "Diabetes Mellitus Tipe 2": {"kode": "D-4-11-II", "tarif_jkn": 15000000},
    "Demam Berdarah Dengue": {"kode": "A-9-01-I", "tarif_jkn": 7500000},
    "Infeksi Saluran Pernapasan Akut (ISPA)": {"kode": "J-2-15-I", "tarif_jkn": 4000000},
    "Kondisi Tidak Teridentifikasi": {"kode": "N/A", "tarif_jkn": 2000000} # Biaya pemeriksaan awal
}


def get_treatment_cost(disease):
    """Mengambil data biaya dari database INA-CBG."""
    return INA_CBG_DATABASE.get(disease, INA_CBG_DATABASE["Kondisi Tidak Teridentifikasi"])


# --- FASE 3: Antarmuka Pengguna (UI) dengan Streamlit ---


# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi & Simulasi Finansial Kesehatan",
    page_icon="🏥",
    layout="wide"
)


# Judul Aplikasi
st.title("🏥 Aplikasi Prediksi Penyakit & Simulasi Finansial")
st.markdown("Sebuah purwarupa untuk Hackathon BI-OJK 2025. Aplikasi ini membantu memprediksi penyakit berdasarkan gejala dan mensimulasikan cakupan biayanya.")


# --- Sidebar untuk Input Pengguna ---
st.sidebar.header("📝 Masukkan Data Pasien")


# Input Faktor Risiko
age = st.sidebar.number_input("Umur", min_value=0, max_value=120, value=35, step=1)
gender = st.sidebar.selectbox("Jenis Kelamin", ["Pria", "Wanita"])
blood_pressure = st.sidebar.slider("Tekanan Darah Sistolik (mmHg)", min_value=80, max_value=200, value=120)


# Input Gejala (menggunakan multiselect)
possible_symptoms = [
    "Demam Tinggi", "Demam Ringan", "Batuk", "Sesak Napas", "Nyeri Dada",
    "Sakit Kepala", "Nyeri Sendi", "Bintik Merah", "Sering Haus",
    "Sering Buang Air Kecil", "Mual", "Lemas"
]
symptoms = st.sidebar.multiselect("Pilih Gejala yang Dirasakan", possible_symptoms)


# Input Data Finansial
st.sidebar.header("💰 Masukkan Data Finansial")
private_insurance_limit = st.sidebar.number_input("Plafon Asuransi Swasta (jika ada biaya tambahan)", min_value=0, value=20000000, step=1000000, format="%d")
personal_funds = st.sidebar.number_input("Dana Pribadi Tersedia", min_value=0, value=5000000, step=1000000, format="%d")
additional_cost = st.sidebar.number_input("Estimasi Biaya Tambahan (di luar paket JKN)", min_value=0, value=10000000, step=1000000, format="%d")




# Tombol untuk memulai prediksi
if st.sidebar.button("🚀 Prediksi dan Hitung Simulasi"):
    if not symptoms:
        st.warning("Mohon pilih minimal satu gejala.")
    else:
        # Tampilkan progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()


        # 1. Prediksi Penyakit
        status_text.text("Menganalisis data dan memprediksi penyakit...")
        progress_bar.progress(33)
        time.sleep(1) # Simulasi proses berpikir model
        predicted_disease, confidence = predict_disease(age, gender, symptoms, blood_pressure)


        # 2. Ambil data biaya
        status_text.text(f"Mengambil data tarif INA-CBGs untuk {predicted_disease}...")
        progress_bar.progress(66)
        time.sleep(1) # Simulasi query database
        cost_data = get_treatment_cost(predicted_disease)
        base_cost = cost_data['tarif_jkn']


        # 3. Lakukan Kalkulasi Finansial Berjenjang
        status_text.text("Menghitung simulasi pembiayaan...")
       
        # Biaya yang ditanggung JKN sesuai paket
        covered_by_jkn = base_cost
       
        # Sisa biaya adalah biaya tambahan di luar paket
        remaining_cost_1 = additional_cost
       
        # Ditutup oleh asuransi swasta
        covered_by_private = min(remaining_cost_1, private_insurance_limit)
        remaining_cost_2 = remaining_cost_1 - covered_by_private
       
        # Ditutup oleh dana pribadi
        covered_by_personal = min(remaining_cost_2, personal_funds)
        final_shortfall = remaining_cost_2 - covered_by_personal
       
        progress_bar.progress(100)
        status_text.text("Analisis Selesai!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()


        # --- Tampilkan Hasil di Halaman Utama ---
        st.header("📊 Hasil Analisis")
       
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🩺 Prediksi Penyakit")
            if confidence > 0.8:
                st.success(f"**Prediksi Utama:** {predicted_disease}")
            elif confidence > 0.6:
                st.warning(f"**Prediksi Utama:** {predicted_disease}")
            else:
                st.error(f"**Prediksi:** {predicted_disease}")
            st.caption(f"Tingkat keyakinan model: {confidence:.0%}")
            st.info(f"Kode INA-CBGs terkait: **{cost_data['kode']}**")


        with col2:
            st.subheader("💰 Estimasi Biaya Dasar")
            st.metric(label="Tarif Dasar Perawatan (sesuai INA-CBGs)", value=f"Rp {base_cost:,.0f}")
            st.caption("Biaya ini diasumsikan ditanggung penuh oleh JKN.")




        st.header("💸 Simulasi Pembiayaan Biaya Tambahan")
        st.markdown(f"Berikut adalah simulasi untuk **biaya tambahan** sebesar **Rp {additional_cost:,.0f}**.")
       
        col_jkn, col_swasta, col_pribadi = st.columns(3)
        col_jkn.metric(
            label="Ditanggung Asuransi Swasta",
            value=f"Rp {covered_by_private:,.0f}",
            help=f"Sesuai plafon Anda sebesar Rp {private_insurance_limit:,.0f}"
        )
        col_swasta.metric(
            label="Ditanggung Dana Pribadi",
            value=f"Rp {covered_by_personal:,.0f}",
            help=f"Dari dana tersedia Rp {personal_funds:,.0f}"
        )
        col_pribadi.metric(
            label="Total Tertanggung",
            value=f"Rp {covered_by_private + covered_by_personal:,.0f}"
        )


        st.header("🚨 Kebutuhan Dana Lanjutan")
        if final_shortfall > 0:
            st.error(f"**Masih ada kekurangan dana sebesar: Rp {final_shortfall:,.0f}**")
            st.markdown(
                """
                Kekurangan dana ini dapat dicarikan melalui:
                - **Platform Donasi Publik (Crowdfunding)**
                - **Pinjaman Lunak dari Institusi Keuangan**
                - **Bantuan Sosial dari Pemerintah atau Lembaga Filantropi**
               
                Aplikasi ini dapat diintegrasikan dengan platform tersebut untuk memfasilitasi pengajuan dana.
                """
            )
        else:
            st.success("**Selamat! Seluruh estimasi biaya tambahan telah tertutupi.**")
            st.balloons()
else:
    st.info("👈 Silakan isi data di sidebar kiri dan klik tombol **'Prediksi dan Hitung Simulasi'** untuk memulai.")