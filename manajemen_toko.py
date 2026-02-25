import json
import customtkinter as ctk
from tkinter import messagebox,simpledialog
from turtle import title


FILE_DATA = "data_barang.json"  # Nama file untuk menyimpan data barang
ctk.set_appearance_mode("dark")  # Menggunakan mode tampilan sistem
ctk.set_default_color_theme("blue")  # Menggunakan tema warna biru

#Utilitas untuk input angka dengan validasi============================

# Fungsi untuk menampilkan garis pemisah
class TokoPrintATK:
    def __init__(self):
        self.barang = []
        self.load_data()

    def input_angka(self, prompt, min_value=None):
        while True:
            try:
                angka = int(input(prompt))
                if min_value is not None and angka < min_value:
                    print(f"Minimal {min_value}")
                    continue
                return angka
            except ValueError:
                print("Masukkan angka yang benar!")

    def input_text(self, prompt):
        while True:
            teks = input(prompt).strip()
            if teks:
                return teks
            print("Input tidak boleh kosong!")

    def pilih_barang(self, prompt):
        if not self.barang:
            print("Belum ada barang.")
            return None

        self.lihat_barang()
        index = self.input_angka(prompt, 1) - 1

        if index < 0 or index >= len(self.barang):
            print("Nomor barang tidak valid.")
            return None
        return index
    
    #===========================================================

    # CRUD Barang==============================================

    # Fungsi untuk menambahkan barang
    def tambah_barang(self):
        nama = self.input_text("Masukkan nama barang: ")
        harga = self.input_angka("Masukkan harga barang: ", 0)
        stok = self.input_angka("Masukkan jumlah stok barang: ", 0)
        data = {
            "nama": nama,
            "harga": harga,
            "stok": stok
        }
        self.barang.append(data)
        self.save_data()
        print(f"\n=== Barang '{nama}' berhasil ditambahkan. ===")

# Fungsi untuk melihat daftar barang
    def lihat_barang(self):
        if not self.barang:
            print("\n=== Belum ada barang yang ditambahkan. ===")
            return
        print("\n=== Daftar Barang ===")

        for i, item in enumerate(self.barang, start=1):
            print(f"{i}. Nama: {item['nama']} | Harga: {item['harga']} | Stok: {item['stok']}")

# Fungsi untuk mengupdate stok barang
    def update_stok(self):
        index = self.pilih_barang("Masukkan nomor barang yang ingin diupdate stoknya: ")
        if index is None:
            print("\n=== Belum ada barang yang ditambahkan. ===")
            return
        
        jumlah_barang = self.input_angka("Masukkan jumlah stok yang ingin ditambahkan: ", 0)
        if self.barang[index]['stok'] + jumlah_barang < 0:
            print("Stok tidak boleh negatif.")
            return
        
        self.barang[index]['stok'] += jumlah_barang
        self.save_data()
        print(f"Stok barang '{self.barang[index]['nama']}' berhasil diupdate.")

# Fungsi untuk menghapus barang
    def hapus_barang(self):
        index = self.pilih_barang("Masukkan nomor barang yang ingin dihapus: ")
        if index is None:
            print("\n=== Belum ada barang yang ditambahkan. ===")
            return
        
        nama_barang = self.barang[index]['nama']
        del self.barang[index]
        self.save_data()
        print(f"\n=== Barang '{nama_barang}' berhasil dihapus. ===")

# Fungsi untuk melakukan transaksi penjualan
    def transaksi_penjualan(self):
        index = self.pilih_barang("Masukkan nomor barang yang ingin dijual: ")
        if index is None:
            print("\n=== Belum ada barang yang ditambahkan. ===")
            return
        
        jumlah_penjualan = self.input_angka("Masukkan jumlah barang yang ingin dijual: ", 1)
        if self.barang[index]['stok'] < jumlah_penjualan:
            print("Stok tidak cukup untuk melakukan penjualan.")
            return
        
        total_harga = jumlah_penjualan * self.barang[index]['harga']
        self.barang[index]['stok'] -= jumlah_penjualan
        self.save_data()
        print(f"Penjualan berhasil! Total harga: Rp. {total_harga}")
        print(f"Sisa stok '{self.barang[index]['nama']}': {self.barang[index]['stok']}")

#=======================================================================================

# Fungsi untuk menyimpan data barang ke file JSON======================================
    def save_data(self):
        with open(FILE_DATA, "w") as file:
            json.dump(self.barang, file, indent=4)

    def load_data(self):
        try:
            with open(FILE_DATA, "r") as file:
                self.barang = json.load(file)
        except FileNotFoundError:
            self.barang = []
#=====================================================================================


#Tamnilan Menu dan Fungsi Utama========================================================

# Fungsi untuk menampilkan menu utama dengan CLI
    # def tampilan_menu(self):
    #     # Menampilkan menu utama
    #     print("\n=== Toko Print ATK ===")
    #     print("1. Tambah Barang")
    #     print("2. Lihat Barang")
    #     print("3. Update Stok Barang")
    #     print("4. Hapus Barang")
    #     print("5. Transaksi Penjualan")
    #     print("6. Keluar")

# Fungsi utama untuk menjalankan aplikasi dengan CLI
    # def run(self):
        # while True:
        #     self.tampilan_menu()
        #     pilihan = input("Pilih menu (1-6): ").strip()
        #     if pilihan == '1':
        #         self.tambah_barang()
        #     elif pilihan == '2':
        #         self.lihat_barang()
        #     elif pilihan == '3':
        #         self.update_stok()
        #     elif pilihan == '4':
        #         self.hapus_barang()
        #     elif pilihan == '5':
        #         self.transaksi_penjualan()
        #     elif pilihan == '6':
        #         self.save_data()
        #         print("Terima kasih telah menggunakan aplikasi Toko Print ATK!")
        #         break
        #     else:            
        #         print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")
#=======================================================================================

class TokoGUI:
    def __init__(self, root, toko):
        self.root = root
        self.toko = toko

        self.root.title("Toko Print ATK")
        self.root.geometry("500x400")

        self.buat_layout()


    def buat_layout(self):

        # Title
        self.title_label = ctk.CTkLabel(
            self.root, 
            text="🛒 Toko Print ATK", 
            font=("Arial", 22, "bold"))
        self.title_label.pack(pady=20)

        # Frame tombol
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Tombol-tombol
        self.btn_tambah = ctk.CTkButton(
            self.frame,
            text="Tambah Barang",
            command=self.tambah_barang_gui
        )
        self.btn_tambah.pack(pady=8)

        self.btn_lihat = ctk.CTkButton(
            self.frame,
            text="Lihat Barang",
            command=self.lihat_barang_gui
        )
        self.btn_lihat.pack(pady=8)

        self.btn_update = ctk.CTkButton(
            self.frame,
            text="Update Stok",
            command=self.update_stok_gui
        )
        self.btn_update.pack(pady=8)

        self.btn_hapus = ctk.CTkButton(
            self.frame,
            text="Hapus Barang",
            command=self.hapus_barang_gui
        )
        self.btn_hapus.pack(pady=8)

        self.btn_transaksi = ctk.CTkButton(
            self.frame,
            text="Transaksi",
            command=self.transaksi_penjualan_gui
        )
        self.btn_transaksi.pack(pady=8)

        self.btn_keluar = ctk.CTkButton(
            self.frame,
            text="Keluar",
            fg_color="red",
            command=self.root.quit
        )
        self.btn_keluar.pack(pady=15)

    def input_int_gui(self, title, text):
        value = simpledialog.askinteger(title, text)
        if value is None:
            messagebox.showerror("Error", "Masukkan angka yang benar!")
            return None
        
        return value

    def tambah_barang_gui(self):
        nama = simpledialog.askstring("Tambah Barang", "Masukkan nama barang:")
        harga = self.input_int_gui("Tambah Barang", "Masukkan harga barang:")
        stok = self.input_int_gui("Tambah Barang", "Masukkan jumlah stok barang:")

        if nama is None or harga is None or stok is None:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        try:
            harga = int(harga)
            stok = int(stok)
        except ValueError:
            messagebox.showerror("Error", "Harga dan stok harus berupa angka!")
            return

        self.toko.barang.append({
            "nama": nama,
            "harga": harga,
            "stok": stok
            })
        self.toko.save_data()
        messagebox.showinfo("Sukses", f"Barang '{nama}' berhasil ditambahkan!")

    def lihat_barang_gui(self):
        data = "\n".join([f"{i+1}. {item['nama']} - Harga: {item['harga']} - Stok: {item['stok']}" for i, item in enumerate(self.toko.barang)])
        messagebox.showinfo("Daftar Barang", data if data else "Belum ada barang yang ditambahkan.")

    def update_stok_gui(self):
        index = simpledialog.askinteger("Update Stok", "Masukkan nomor barang yang ingin diupdate stoknya:")
        if index is None or index < 1 or index > len(self.toko.barang):
            messagebox.showerror("Error", "Nomor barang tidak valid!")
            return

        jumlah_barang = simpledialog.askinteger("Update Stok", "Masukkan jumlah stok yang ingin ditambahkan:")
        if jumlah_barang is None or jumlah_barang < 0:
            messagebox.showerror("Error", "Jumlah stok harus berupa angka positif!")
            return

        self.toko.barang[index-1]['stok'] += jumlah_barang
        self.toko.save_data()
        messagebox.showinfo("Sukses", f"Stok barang '{self.toko.barang[index-1]['nama']}' berhasil diupdate!")
    
    def hapus_barang_gui(self):
        index = simpledialog.askinteger("Hapus Barang", "Masukkan nomor barang yang ingin dihapus:")
        if index is None or index < 1 or index > len(self.toko.barang):
            messagebox.showerror("Error", "Nomor barang tidak valid!")
            return

        nama_barang = self.toko.barang[index-1]['nama']
        del self.toko.barang[index-1]
        self.toko.save_data()
        messagebox.showinfo("Sukses", f"Barang '{nama_barang}' berhasil dihapus!")

    def transaksi_penjualan_gui(self):
        index = simpledialog.askinteger("Transaksi Penjualan", "Masukkan nomor barang yang ingin dijual:")
        if index is None or index < 1 or index > len(self.toko.barang):
            messagebox.showerror("Error", "Nomor barang tidak valid!")
            return

        jumlah_penjualan = simpledialog.askinteger("Transaksi Penjualan", "Masukkan jumlah barang yang ingin dijual:")
        if jumlah_penjualan is None or jumlah_penjualan < 1:
            messagebox.showerror("Error", "Jumlah penjualan harus berupa angka positif!")
            return

        if self.toko.barang[index-1]['stok'] < jumlah_penjualan:
            messagebox.showerror("Error", "Stok tidak cukup untuk melakukan penjualan!")
            return

        total_harga = jumlah_penjualan * self.toko.barang[index-1]['harga']
        self.toko.barang[index-1]['stok'] -= jumlah_penjualan
        self.toko.save_data()
        messagebox.showinfo("Sukses", f"Penjualan berhasil! Total harga: Rp. {total_harga}\nSisa stok '{self.toko.barang[index-1]['nama']}': {self.toko.barang[index-1]['stok']}")

# Program utama
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    toko = TokoPrintATK()
    gui = TokoGUI(root, toko)

    root.mainloop()
    