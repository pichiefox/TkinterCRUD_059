import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL)
        ''')
    conn.commit()
    conn.close()

def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi >= inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak dapat ditentukan"

def submit_nilai():
    nama = entry_nama.get().strip()
    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return

    hasil_prediksi = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil_prediksi))
    conn.commit()
    conn.close()

    messagebox.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {hasil_prediksi}")

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)


def on_enter(e):
    btn_submit[bg] = "#fac46f"
    btn_submit[fg] = "black"

def on_leave(e):
    btn_submit[bg] = "#4e381f"
    btn_submit[fg] = "white"

create_db()

root = tk.Tk()
root.title("Aplikasi Prediksi Fakultas")
root.geometry("400x400")
root.configure(bg="#f0f0f0") # Warna background jendela
root.eval('tk::PlaceWindow . center') # Pusatkan jendela di layar

# Label Judul
tk.Label(root, text="Input Nilai Siswa", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=15)

# Frame untuk form agar rapi
frame_form = tk.Frame(root, bg="#f0f0f0")
frame_form.pack(pady=10)

# Label dan Entry Nama
tk.Label(frame_form, text="Nama Siswa:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5, padx=5)
entry_nama = tk.Entry(frame_form, width=30)
entry_nama.grid(row=0, column=1, pady=5, padx=5)

# Label dan Entry Biologi
tk.Label(frame_form, text="Nilai Biologi:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5, padx=5)
entry_bio = tk.Entry(frame_form, width=30)
entry_bio.grid(row=1, column=1, pady=5, padx=5)

# Label dan Entry Fisika
tk.Label(frame_form, text="Nilai Fisika:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5, padx=5)
entry_fis = tk.Entry(frame_form, width=30)
entry_fis.grid(row=2, column=1, pady=5, padx=5)

# Label dan Entry Inggris
tk.Label(frame_form, text="Nilai Inggris:", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5, padx=5)
entry_ing = tk.Entry(frame_form, width=30)
entry_ing.grid(row=3, column=1, pady=5, padx=5)

# Tombol Submit
btn_submit = tk.Button(root, text="Submit Nilai", command=submit_nilai, 
                       bg="#ff87b1", fg="white", font=("Arial", 10, "bold"), 
                       width=20, height=2, cursor="hand2")
btn_submit.pack(pady=20)

# Binding efek hover ke tombol
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

root.mainloop()