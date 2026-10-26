
import tkinter as tk
from tkinter import messagebox
import sqlite3

# 1. Koneksi ke database SQLite
conn = sqlite3.connect("nilai_siswa.db")
cursor = conn.cursor()

# 2. Membuat tabel nilai_siswa
cursor.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT NOT NULL,
    biologi INTEGER NOT NULL,
    fisika INTEGER NOT NULL,
    inggris INTEGER NOT NULL,
    prediksi_fakultas TEXT NOT NULL
)
""")
conn.commit()


# 3. Fungsi submit nilai
def submit_nilai():
    nama = entry_nama.get().strip()

    try:
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())
    except ValueError:
        messagebox.showerror(
            "Error", "Semua nilai harus diisi dengan angka!"
        )
        return

    if not nama:
        messagebox.showerror("Error", "Nama siswa wajib diisi!")
        return

    if any(n < 0 or n > 100
           for n in [biologi, fisika, inggris]):
        messagebox.showerror(
            "Error", "Nilai harus antara 0 sampai 100!"
        )
        return

    # 4. Menentukan prediksi fakultas
    if biologi >= fisika and biologi >= inggris:
        prediksi = "Kedokteran"
    elif fisika >= biologi and fisika >= inggris:
        prediksi = "Teknik"
    else:
        prediksi = "Bahasa"

    # 5. Menyimpan data ke SQLite
    cursor.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))

    conn.commit()

    # 6. Menampilkan hasil prediksi
    label_hasil.config(
        text=f"Prediksi Fakultas: {prediksi}"
    )

    messagebox.showinfo(
        "Berhasil",
        f"Data {nama} berhasil disimpan!\n"
        f"Prediksi Fakultas: {prediksi}"
    )

    # Mengosongkan input setelah berhasil
    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_inggris.delete(0, tk.END)


# 7. Membuat tampilan Tkinter
root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("400x420")
root.resizable(False, False)

tk.Label(
    root, text="PREDIKSI FAKULTAS SISWA",
    font=("Arial", 15, "bold")
).pack(pady=15)


def buat_input(label_text):
    tk.Label(root, text=label_text).pack()
    entry = tk.Entry(root, width=35)
    entry.pack(pady=5)
    return entry




tk.Button(
    root,
    text="SUBMIT NILAI",
    command=submit_nilai,
    bg="blue",
    fg="white",
    width=20
).pack(pady=15)

label_hasil = tk.Label(
    root, text="Prediksi Fakultas: -",
    font=("Arial", 11, "bold")
)
label_hasil.pack(pady=5)


# 8. Menjalankan aplikasi
root.mainloop()

# Menutup koneksi saat program selesai
conn.close()
