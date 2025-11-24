```
# 🚀 Genius Quiz AI (Ultimate Edition)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20PC-brightgreen)
![AI](https://img.shields.io/badge/Powered%20By-Google%20Gemini-orange)

**Genius Quiz AI** adalah aplikasi kuis berbasis konsol (CLI) modern yang ditenagai oleh **Google Gemini AI**. 

Berbeda dengan kuis biasa, aplikasi ini **tidak membutuhkan database soal manual**. Cukup ketik topik apa saja (Matematika, Sejarah, Game, Film, Koding), dan AI akan membuatkan soal unik, lengkap dengan penjelasan, sistem skor, dan efek suara.

---

## 📸 Tampilan Awal (Preview)

Saat program dijalankan di Terminal/CMD Windows, tampilannya akan seperti ini:

```text
  ╔══════════════════════════════════════╗
  ║        🤖 GEMINI AI SUPER QUIZ       ║
  ║      Ultimate Edition for Windows    ║
  ╚══════════════════════════════════════╝

  1. 🎮 Mulai Kuis Baru
  2. 🏆 Lihat Leaderboard (Skor Tertinggi)
  3. ❌ Keluar

  Pilih menu (1-3): _
```

**Saat Gameplay:**
```text
Player: Rofrod | Soal 3/5 | Skor: 25 | Streak: 3 🔥
------------------------------------------------------------
Pertanyaan:
Siapakah tokoh proklamator kemerdekaan Indonesia?

   A. Soeharto
   B. Soekarno
   C. B.J. Habibie
   D. Jenderal Sudirman

[1] 50:50 (ADA) | [2] Hint (ADA)
Jawab (A-D): _
```

---

## ✨ Fitur Unggulan (Ultimate Edition)

Versi ini dikhususkan untuk PC/Windows dengan fitur lengkap:

1.  **🔊 Efek Suara (Sound FX):** Menggunakan `winsound` bawaan Windows. Ada bunyi *Chime* saat benar, *Buzz* saat salah, dan *Bonus Sound*.
2.  **⚡ Bonus Kecepatan:** Jawab di bawah 7 detik untuk mendapatkan poin ekstra.
3.  **🔥 Combo Streak:** Jawaban benar berturut-turut akan melipatgandakan poin.
4.  **🆘 Lifelines (Bantuan):**
    *   **50:50:** Komputer menghapus 2 jawaban yang salah.
    *   **Hint:** Meminta AI memberikan petunjuk rahasia.
    *   **Infinity AI:** Soal dibuat otomatis dan tidak terbatas.
5.  **💾 Auto-Save:**
    *   **Leaderboard:** Skor tertinggi tersimpan abadi di `leaderboard_kuis.json`.
    *   **Rangkuman Materi:** Penjelasan soal otomatis diekspor ke file `.txt` untuk bahan belajar.

---

## 🛠️ Persiapan & Instalasi

### 1. Prasyarat
Pastikan kamu sudah menginstal **Python** (Versi 3.10 ke atas direkomendasikan).
*   Download di: [python.org](https://www.python.org/downloads/)
*   **PENTING:** Saat install, centang kotak **"Add Python to PATH"**.

### 2. Clone / Download
Download kode ini atau clone repository:
```bash
git clone https://github.com/username-kamu/nama-repo.git
cd nama-repo
```

### 3. Install Library
Hanya satu library yang dibutuhkan:
```bash
pip install google-generativeai
```
*(Jika error "pip not found", coba gunakan perintah: `python -m pip install google-generativeai`)*

---

## 🔑 Cara Mendapatkan API Key (Gratis)

Aplikasi ini butuh "kunci" untuk terhubung ke otak Google AI.

1.  Kunjungi **[Google AI Studio](https://aistudio.google.com/)**.
2.  Login dengan akun Google.
3.  Klik **"Get API key"** -> **"Create API key in new project"**.
4.  Copy kode kunci yang muncul.
5.  Buka file `kuis_ultimate.py` (atau nama file python kamu).
6.  Tempelkan di bagian paling atas:

```python
# ==========================================
# KONFIGURASI API KEY
# ==========================================
API_KEY = "TEMPEL_KODE_API_KEY_KAMU_DISINI"
```

> ⚠️ **Peringatan Keamanan:** Jangan pernah membagikan API Key kamu secara publik. Jika mengunggah ke GitHub, kosongkan bagian ini atau gunakan Environment Variable.

---

## 🚀 Cara Menjalankan

Buka **Command Prompt (CMD)** atau **PowerShell** di folder tempat kamu menyimpan file, lalu ketik:

```bash
python kuis_ultimate.py
```
*(Atau `py kuis_ultimate.py` jika perintah python tidak terdeteksi)*

---

## 📂 Struktur File

*   `kuis_ultimate.py`: Kode utama aplikasi (Logic, UI, Sound).
*   `leaderboard_kuis.json`: Database JSON penyimpan skor (Otomatis dibuat).
*   `Rangkuman_*.txt`: File catatan hasil belajar (Otomatis dibuat).

---
