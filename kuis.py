import time
import sys
import os
import json
import random
import google.generativeai as genai
from datetime import datetime

# Cek apakah di Windows untuk fitur suara
try:
    import winsound
    SOUND_ON = True
except ImportError:
    SOUND_ON = False

# ==========================================
# KONFIGURASI API KEY
# ==========================================
API_KEY = "AIzaSyBe67A23XWkNEVwavwdmAX9J5t_SmUfKUg"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    sys.exit("Error API Key.")

class Warna:
    HEADER = '\033[95m'
    BIRU = '\033[94m'
    HIJAU = '\033[92m'
    KUNING = '\033[93m'
    MERAH = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- FITUR SUARA ---
def mainkan_suara(jenis):
    if not SOUND_ON: return
    if jenis == "benar":
        winsound.Beep(1000, 100) # Nada tinggi
        winsound.Beep(1500, 200)
    elif jenis == "salah":
        winsound.Beep(500, 400) # Nada rendah

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
            f.write(f"=== MATERI: {topik.upper()} ===\n")
            for item in riwayat:
                f.write(f"Tanya: {item['tanya']}\n")
                f.write(f"Jawab: {item['jawaban']}\n")
                f.write(f"Info: {item['penjelasan']}\n")
                f.write("-" * 30 + "\n")
        return nama_file
    except:
        return "Error Save"

# --- AI GENERATOR ---
def generate_soal(topik, level):
    prompt = f"""
    Buat 1 soal pilihan ganda topik '{topik}' level '{level}'.
    Format JSON MURNI:
    {{
        "pertanyaan": "soal...",
        "pilihan": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
        "jawaban_benar": "A",
        "penjelasan": "penjelasan singkat",
        "clue": "satu kalimat petunjuk/hint tanpa menyebut jawaban"
    }}
    """
    # Logika Retry sama seperti sebelumnya
    for _ in range(3):
        try:
            resp = model.generate_content(prompt)
            txt = resp.text
            s = txt.find('{')
            e = txt.rfind('}') + 1
            return json.loads(txt[s:e])
        except:
            time.sleep(1)
    return None

# --- MAIN PROGRAM ---
def main():
    riwayat = []
    # Status Bantuan (Hanya bisa dipakai 1x per game)
    bantuan_5050 = True 
    bantuan_hint = True
    
    streak = 0 # Combo berturut-turut
    skor = 0
    
    bersihkan_layar()
    print(Warna.HEADER + "="*60)
    print(f"{Warna.BOLD}    🚀 KUIS AI ULTIMATE: STREAK & LIFELINE EDITION 🚀    ")
    print(Warna.HEADER + "="*60 + Warna.RESET)

    topik = input(f"{Warna.KUNING}Topik: {Warna.RESET}") or "Umum"
    jml_soal = int(input(f"{Warna.KUNING}Jumlah Soal: {Warna.RESET}") or 5)
    
    for i in range(1, jml_soal + 1):
        soal = None
        while not soal:
            print(f"\r{Warna.CYAN}Sedang memuat soal {i}...{Warna.RESET}", end="")
            soal = generate_soal(topik, "Sedang")
        
        opsi_aktif = list(soal['pilihan'].keys()) # ['A', 'B', 'C', 'D']
        mode_5050_aktif = False

        # --- LOOP TAMPILAN SOAL (Agar bisa refresh saat pakai bantuan) ---
        while True:
            bersihkan_layar()
            # Header Status
            bonus_str = f"🔥 STREAK x{streak}" if streak > 1 else ""
            print(f"{Warna.BIRU}Soal {i}/{jml_soal} | Skor: {skor} | {Warna.MERAH}{bonus_str}{Warna.RESET}")
            print("-" * 60)
            
            ketik(soal['pertanyaan'], warna=Warna.BOLD)
            print()
            
            # Tampilkan Opsi
            for k, v in soal['pilihan'].items():
                if k in opsi_aktif:
                    print(f"   {k}. {v}")
                else:
                    print(f"   {k}. -----") # Opsi yang dihapus 50:50

            # Menu Bantuan
            print("\n" + "-"*30)
            print(f"BANTUAN TERSEDIA:")
            if bantuan_5050: print(f"[1] 50:50 (Hapus 2 jawaban salah)") 
            else: print(f"{Warna.MERAH}[1] 50:50 (HABIS){Warna.RESET}")
            
            if bantuan_hint: print(f"[2] HINT (Minta petunjuk AI)")
            else: print(f"{Warna.MERAH}[2] HINT (HABIS){Warna.RESET}")

            jawab = input(f"\n{Warna.KUNING}Jawab (A-D) atau (1-2) untuk bantuan: {Warna.RESET}").upper()
            
            # --- LOGIKA BANTUAN ---
            if jawab == "1":
                if bantuan_5050:
                    bantuan_5050 = False
                    # Cari jawaban salah untuk dihapus
                    kunci = soal['jawaban_benar']
                    salahs = [k for k in opsi_aktif if k != kunci]
                    hapus = random.sample(salahs, 2) # Pilih 2 acak
                    for h in hapus: opsi_aktif.remove(h) # Hapus dari list aktif
                    print(f"{Warna.HIJAU}>>> 2 Jawaban Salah telah dihapus!{Warna.RESET}")
                    time.sleep(1)
                    continue # Refresh layar
                else:
                    print("Bantuan ini sudah terpakai!"); time.sleep(1)

            elif jawab == "2":
                if bantuan_hint:
                    bantuan_hint = False
                    print(f"\n{Warna.CYAN}🕵️  HINT DARI AI: {soal.get('clue', 'Pikirkan baik-baik!')}{Warna.RESET}")
                    input("[Enter kembali ke soal]")
                    continue
                else:
                    print("Bantuan ini sudah terpakai!"); time.sleep(1)

            # --- CEK JAWABAN ---
            elif jawab in ['A', 'B', 'C', 'D']:
                if jawab not in opsi_aktif:
                    print("Jawaban itu sudah dihapus!"); time.sleep(1); continue
                
                poin = 1
                if streak >= 2: poin = 2 # Bonus Streak
                
                if jawab == soal['jawaban_benar']:
                    mainkan_suara("benar")
                    print(f"\n{Warna.HIJAU}✅ BENAR! (+{poin} Poin){Warna.RESET}")
                    if streak > 1: print(f"{Warna.KUNING}🔥 COMBO BONUS!{Warna.RESET}")
                    skor += poin
                    streak += 1
                else:
                    mainkan_suara("salah")
                    print(f"\n{Warna.MERAH}❌ SALAH! (-1 Poin){Warna.RESET}")
                    print(f"Jawaban: {soal['jawaban_benar']}")
                    skor -= 1
                    streak = 0 # Reset streak
                
                # Simpan & Penjelasan
                riwayat.append({"tanya": soal['pertanyaan'], "jawaban": soal['jawaban_benar'], "penjelasan": soal['penjelasan']})
                print(f"\n💡 {Warna.CYAN}{soal['penjelasan']}{Warna.RESET}")
                input("\n[Enter lanjut...]")
                break # Keluar dari loop soal ini, lanjut soal berikutnya
            
            else:
                print("Input tidak valid.")

    # END GAME
    bersihkan_layar()
    ketik(f"Permainan Selesai! Skor Akhir: {skor}", warna=Warna.BOLD)
    file = simpan_catatan(topik, riwayat)
    print(f"Rangkuman disimpan di: {file}")

if __name__ == "__main__":
    main()
