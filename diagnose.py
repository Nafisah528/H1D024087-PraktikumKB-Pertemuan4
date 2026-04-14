import tkinter as tk
from tkinter import messagebox

# =========================
# DATA GEJALA
# =========================
gejala_list = [
    ("G01", "Apakah komputer sering terasa lambat saat digunakan?"),
    ("G02", "Apakah aplikasi sering error atau crash?"),
    ("G03", "Apakah komputer tiba-tiba mati sendiri?"),
    ("G04", "Apakah terdengar bunyi beep saat dinyalakan?"),
    ("G05", "Apakah perangkat terasa sangat panas?"),
    ("G06", "Apakah layar tidak menampilkan gambar?"),
    ("G07", "Apakah kipas berbunyi sangat keras?"),
    ("G08", "Apakah harddisk tidak terbaca?"),
    ("G09", "Apakah proses booting sangat lama?"),
    ("G10", "Apakah file sering rusak atau tidak bisa dibuka?")
]

# =========================
# KNOWLEDGE BASE
# =========================
rules = {
    "Gangguan RAM": {
        "kode": ["G01", "G02", "G04"],
        "solusi": "Bersihkan pin RAM menggunakan penghapus, lalu pasang kembali atau ganti RAM."
    },
    "Kerusakan Power Supply": {
        "kode": ["G03", "G06"],
        "solusi": "Periksa kondisi PSU dan pastikan kabel daya terhubung dengan baik."
    },
    "Overheat Prosesor": {
        "kode": ["G05", "G07", "G03"],
        "solusi": "Bersihkan kipas dan ganti thermal paste pada prosesor."
    },
    "Kerusakan VGA": {
        "kode": ["G06", "G02"],
        "solusi": "Periksa dan pasang ulang VGA atau ganti jika diperlukan."
    },
    "Kerusakan Harddisk": {
        "kode": ["G08", "G09", "G10"],
        "solusi": "Segera backup data dan lakukan pengecekan atau penggantian harddisk."
    }
}

# =========================
# STATE
# =========================
index = 0
jawaban_user = set()

# =========================
# FUNGSI
# =========================
def mulai():
    global index, jawaban_user
    index = 0
    jawaban_user.clear()

    btn_mulai.pack_forget()
    btn_ya.pack(side="left", padx=10)
    btn_tidak.pack(side="right", padx=10)

    tampil_pertanyaan()

def tampil_pertanyaan():
    if index < len(gejala_list):
        kode, teks = gejala_list[index]
        label_info.config(text=f"Pertanyaan {index+1} dari {len(gejala_list)}")
        label_pertanyaan.config(text=teks)
    else:
        tampilkan_hasil()

def jawab(pilihan):
    global index
    kode, _ = gejala_list[index]

    if pilihan:
        jawaban_user.add(kode)

    index += 1
    tampil_pertanyaan()

def tampilkan_hasil():
    # Hitung kecocokan untuk setiap kerusakan
    skor_kerusakan = []  # list of (nama, cocok, total, solusi)
    for nama, data in rules.items():
        cocok = sum(1 for k in data["kode"] if k in jawaban_user)
        total = len(data["kode"])
        skor_kerusakan.append((nama, cocok, total, data["solusi"]))

    # Pisahkan yang cocok sempurna (cocok == total)
    sempurna = [(nama, cocok, total, solusi) for (nama, cocok, total, solusi) in skor_kerusakan if cocok == total]

    if sempurna:
        # Tampilkan semua kerusakan yang cocok 100%
        hasil = "=== HASIL DIAGNOSA ===\n\n"
        for nama, _, _, solusi in sempurna:
            hasil += f"Kerusakan: {nama}\nSolusi: {solusi}\n\n"
        messagebox.showinfo("Hasil Diagnosa", hasil.strip())
    else:
        # Cari skor tertinggi (max cocok)
        if not skor_kerusakan:
            messagebox.showinfo("Hasil Diagnosa", "Tidak dapat mendiagnosa kerusakan.")
            reset()
            return

        max_cocok = max(skor_kerusakan, key=lambda x: x[1])[1]
        if max_cocok == 0:
            messagebox.showinfo("Hasil Diagnosa", "Tidak ada gejala yang cocok dengan basis pengetahuan.")
            reset()
            return

        # Ambil semua kerusakan dengan skor tertinggi
        terbaik = [(nama, cocok, total, solusi) for (nama, cocok, total, solusi) in skor_kerusakan if cocok == max_cocok]

        hasil = "=== HASIL DIAGNOSA (Tidak ada kecocokan sempurna) ===\n\n"
        for nama, cocok, total, solusi in terbaik:
            persen = (cocok / total) * 100
            hasil += f"Kerusakan: {nama}\nTingkat kecocokan: {persen:.0f}%\nSolusi: {solusi}\n\n"
        messagebox.showinfo("Hasil Diagnosa", hasil.strip())

    reset()

def reset():
    btn_ya.pack_forget()
    btn_tidak.pack_forget()
    btn_mulai.pack(pady=10)

    label_info.config(text="Klik mulai untuk memulai diagnosa")
    label_pertanyaan.config(text="Tekan tombol di bawah untuk memulai")

# =========================
# GUI
# =========================
root = tk.Tk()
root.title("Sistem Pakar Diagnosa Komputer")
root.geometry("500x300")
root.config(bg="#f4f6f7")

judul = tk.Label(root,
                 text="Sistem Pakar Diagnosa Kerusakan Komputer",
                 font=("Arial", 14, "bold"),
                 bg="#f4f6f7")
judul.pack(pady=10)

label_info = tk.Label(root,
                      text="Klik mulai untuk memulai diagnosa",
                      font=("Arial", 10),
                      bg="#f4f6f7")
label_info.pack()

label_pertanyaan = tk.Label(root,
                            text="Tekan tombol di bawah untuk memulai",
                            font=("Arial", 11),
                            bg="white",
                            width=45,
                            height=5,
                            wraplength=380,
                            relief="ridge",
                            justify="center")
label_pertanyaan.pack(pady=15)

frame = tk.Frame(root, bg="#f4f6f7")
frame.pack()

btn_ya = tk.Button(frame, text="Ya", width=12,
                   command=lambda: jawab(True))

btn_tidak = tk.Button(frame, text="Tidak", width=12,
                      command=lambda: jawab(False))

btn_mulai = tk.Button(root,
                      text="Mulai Diagnosa",
                      width=18,
                      command=mulai)
btn_mulai.pack(pady=10)

root.mainloop()