import time
import sys
import os
import json
import google.generativeai as genai
from datetime import datetime

# ==========================================
# KONFIGURASI API KEY
# ==========================================
API_KEY = "AIzaSyBe67A23XWkNEVwavwdmAX9J5t_SmUfKUg"

# Konfigurasi Gemini
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    print("Error konfigurasi API Key. Pastikan API Key benar.")
    sys.exit()

class Warna:
    HEADER = '\033[95m'
    BIRU = '\033[94m'
    HIJAU = '\033[92m'
    KUNING = '\033[93m'
    MERAH = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- UTILITAS ---
def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def ketik(teks, delay=0.01, warna=Warna.RESET):
    sys.stdout.write(warna)
    for char in teks:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Warna.RESET + "\n")

def simpan_catatan(topik, riwayat):
    waktu = datetime.now().strftime("%Y-%m-%d_%H-%M")
    nama_file = f"Catatan_{topik.replace(' ', '_')}_{waktu}.txt"
    try:
        with open(nama_file, "w", encoding="utf-8") as f:
            f.write(f"=== RANGKUMAN BELAJAR: {topik.upper()} ===\n")
            f.write(f"Dibuat pada: {waktu}\n\n")
            for i, item in enumerate(riwayat, 1):
                f.write(f"Soal {i}: {item['tanya']}\n")
                f.write(f"Jawaban Benar: {item['jawaban']}\n")
                f.write(f"Penjelasan: {item['penjelasan']}\n")
                f.write("-" * 40 + "\n")
        return nama_file
    except:
        return "Gagal menyimpan file"

# --- FUNGSI GENERATE SOAL (YANG DIPERBAIKI) ---
def generate_soal(topik, level):
    """
    Mencoba generate soal dengan sistem Retry dan Cleaning JSON yang lebih kuat.
    """
    prompt = f"""
    Buat 1 soal pilihan ganda (Multiple Choice) tentang '{topik}' tingkat '{level}'.
    Output HARUS JSON murni tanpa markdown (```json).
    Format:
    {{
        "pertanyaan": "teks pertanyaan",
        "pilihan": {{"A": "teks A", "B": "teks B", "C": "teks C", "D": "teks D"}},
        "jawaban_benar": "A",
        "penjelasan": "penjelasan singkat"
    }}
    """
    
    max_retries = 3
    for percataan in range(max_retries):
        try:
            # Request ke AI
            response = model.generate_content(prompt)
            raw_text = response.text
            
            # --- PEMBERSIH JSON ---
            # Cari kurung kurawal pertama { dan terakhir }
            start_idx = raw_text.find('{')
            end_idx = raw_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("Format JSON tidak ditemukan")
                
            clean_json = raw_text[start_idx:end_idx]
            data = json.loads(clean_json)
            
            # Validasi kunci (Key)
            if "pertanyaan" in data and "pilihan" in data and "jawaban_benar" in data:
                return data
            else:
                raise ValueError("Data JSON tidak lengkap")

        except Exception as e:
            # Jika error, print log kecil dan coba lagi (jangan langsung exit)
            print(f"\r{Warna.MERAH}Gagal memuat soal (Percobaan {percataan+1}/{max_retries})...{Warna.RESET}", end="")
            time.sleep(1)
    
    return None # Menyerah setelah 3x percobaan

# --- MAIN PROGRAM ---
def main():
    riwayat_belajar = []
    bersihkan_layar()
    
    print(Warna.HEADER + "="*60)
    print(f"{Warna.BOLD}       🎓 KUIS PINTAR AI - SYSTEM V2.0       ")
    print(Warna.HEADER + "="*60 + Warna.RESET)

    # Input User
    topik = input(f"{Warna.KUNING}Topik Belajar: {Warna.RESET}")
    if not topik: topik = "Pengetahuan Umum" # Default jika kosong

    print(f"\nPilih Level:\n1. Mudah\n2. Sedang\n3. Sulit")
    lvl_input = input(f"{Warna.KUNING}Pilihan (1-3): {Warna.RESET}")
    level_str = {"1":"Mudah", "2":"Sedang", "3":"Sulit"}.get(lvl_input, "Sedang")

    try:
        jumlah_soal = int(input(f"{Warna.KUNING}Jumlah soal: {Warna.RESET}"))
    except:
        jumlah_soal = 5

    skor = 0
    soal_berhasil = 0 # Counter soal yang benar-benar muncul
    
    for i in range(1, jumlah_soal + 1):
        bersihkan_layar()
        print(f"{Warna.BIRU}Topik: {topik} ({level_str}) | Soal {i}/{jumlah_soal} | Skor: {skor}{Warna.RESET}")
        print("-" * 60)
        
        print(f"{Warna.CYAN}Sedang menghubungi Guru AI...{Warna.RESET}")
        
        # Panggil fungsi generate yang sudah diperbaiki
        soal = generate_soal(topik, level_str)
        
        # Jika AI Gagal total setelah 3x retry
        if not soal:
            print(f"\n{Warna.MERAH}⚠️ Terjadi kesalahan jaringan atau AI sibuk.{Warna.RESET}")
            print("Melewati soal ini...")
            time.sleep(2)
            continue # Pindah ke iterasi berikutnya, TAPI score tidak berubah
            
        # Validasi ulang agar program tidak crash jika pilihan bukan dict
        if not isinstance(soal['pilihan'], dict):
            print("Format soal rusak, lewati.")
            continue

        soal_berhasil += 1
        
        # Simpan riwayat
        riwayat_belajar.append({
            "tanya": soal['pertanyaan'],
            "jawaban": f"{soal['jawaban_benar']}. {soal.get('pilihan', {}).get(soal['jawaban_benar'], '?')}",
            "penjelasan": soal.get('penjelasan', '-')
        })

        # Tampilkan Soal
        bersihkan_layar()
        print(f"{Warna.BIRU}Topik: {topik} | Skor: {Warna.BOLD}{skor}{Warna.RESET}")
        print("-" * 60)
        
        ketik(soal['pertanyaan'], warna=Warna.BOLD)
        print()
        
        for k, v in soal['pilihan'].items():
            print(f"   {k}. {v}")
            
        while True:
            jawab = input(f"\n{Warna.KUNING}Jawabanmu (A/B/C/D): {Warna.RESET}").upper()
            if jawab in ['A', 'B', 'C', 'D']:
                break
            print("Masukkan huruf A, B, C, atau D saja.")
        
        if jawab == soal['jawaban_benar']:
            print(f"\n{Warna.HIJAU}✅ BENAR! (+1){Warna.RESET}")
            skor += 1
        else:
            print(f"\n{Warna.MERAH}❌ SALAH! (-1){Warna.RESET}")
            print(f"Jawaban: {soal['jawaban_benar']}")
            skor -= 1
            
        print(f"\n{Warna.CYAN}💡 PENJELASAN: {soal['penjelasan']}{Warna.RESET}")
        input("\n[Tekan Enter untuk lanjut...]")

    # --- OUTRO ---
    bersihkan_layar()
    print(Warna.HEADER + "="*50)
    print(f"SKOR AKHIR: {Warna.HIJAU if skor > 0 else Warna.MERAH}{skor}{Warna.RESET}")
    print(Warna.HEADER + "="*50)
    
    if soal_berhasil > 0:
        ketik(f"\n📝 Menyimpan Rapor...", warna=Warna.KUNING)
        file_out = simpan_catatan(topik, riwayat_belajar)
        print(f"Rangkuman disimpan di: {Warna.BOLD}{file_out}{Warna.RESET}")
    else:
        print("Tidak ada soal yang berhasil diselesaikan.")
    
    print("\nTerima kasih!")

if __name__ == "__main__":
    main()
