import os
import re
from core.event_manager import *
from core.management import (
    tambah_klien, tambah_vendor, tambah_staff,
    tambah_inventaris, tambah_keuangan, laporan_keuangan
)
from lib.utils import tampilkan_event

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi validasi format tanggal
def validasi_tanggal(tanggal: str) -> bool:
    pola = r"^(0[1-9]|[12][0-9]|3[01])\s(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s\d{4}$"
    return re.match(pola, tanggal) is not None

# --- fungsi login ---
def login():
    admin_username = "admin"
    admin_password = "1234"

    print("=== LOGIN ADMIN ===")
    username = input("Username: ")
    password = input("Password: ")

    if username == admin_username and password == admin_password:
        print("\nLogin berhasil!\n")
        return True
    else:
        print("\nUsername atau password salah. Akses ditolak.\n")
        return False

# --- tampilkan menu ---
def tampilkan_menu():
    print("\n=== CLI EVENT ORGANIZER ===")
    print("1. Tambah Event")
    print("2. Tambah Peserta ke Event")
    print("3. Atur RSVP")
    print("4. Lihat Semua Event")
    print("5. Export Data ke File")
    print("6. Tambah Klien")
    print("7. Tambah Vendor")
    print("8. Tambah Staff")
    print("9. Tambah Inventaris")
    print("10. Tambah Catatan Keuangan")
    print("11. Lihat Laporan Keuangan")
    print("12. Keluar")

# --- program utama ---
def main():
    if not login():
        return

    while True:
        tampilkan_menu()
        pilih = input("Pilih menu: ")

        if pilih == "1":
            title = input("Judul Event: ")
            location = input("Lokasi      : ")

            while True:
                date = input("Tanggal (format: DD Bulan YYYY, contoh: 01 Januari 2025): ")
                if validasi_tanggal(date):
                    break
                else:
                    print("❌ Format tanggal tidak valid. Pastikan sesuai 'DD Bulan YYYY' dengan nama bulan kapital.")

            event = tambah_event(title, location, date)
            print("\n✅ Event berhasil ditambahkan!")
            print(f"Judul   : {event.title}")
            print(f"Lokasi  : {event.location}")
            print(f"Tanggal : {event.date}")
            print("Peserta : (belum ada peserta)")

        elif pilih == "2":
            if not events:
                print("❌ Belum ada event.")
            else:
                for i, e in enumerate(events):
                    print(f"[{i+1}] {e.title}")
                try:
                    idx = int(input("Pilih nomor event: ")) - 1
                    name = input("Nama Peserta: ")
                    tambah_peserta(idx, name)
                    print(f"✅ Peserta {name} berhasil ditambahkan ke event '{events[idx].title}'.")
                except:
                    print("❌ Pilihan tidak valid.")

        elif pilih == "3":
            if not events:
                print("❌ Belum ada event.")
            else:
                for i, e in enumerate(events):
                    print(f"[{i+1}] {e.title}")
                try:
                    idx = int(input("\nPilih event: ")) - 1
                    if not events[idx].participants:
                        print("❌ Belum ada peserta.")
                    else:
                        for p in events[idx].participants:
                            print(f"- {p.name:<8} | Status: {p.status.value}")
                        nama = input("\nMasukkan nama peserta: ")
                        konfirmasi = input("Konfirmasi kehadiran? (ya/tidak): ")
                        if atur_rsvp(idx, nama, konfirmasi):
                            print("✅ Status berhasil diperbarui!")
                        else:
                            print("❌ Peserta tidak ditemukan.")
                except:
                    print("❌ Pilihan tidak valid.")

        elif pilih == "4":
            if not events:
                print("❌ Belum ada event.")
            else:
                for e in events:
                    tampilkan_event(e)

        elif pilih == "5":
            file = export_data()
            print(f"\n✅ Semua data berhasil diekspor ke file:\n./{file}")

        elif pilih == "6":
            name = input("Nama Klien : ")
            contact = input("Kontak     : ")
            address = input("Alamat     : ")
            klien = tambah_klien(name, contact, address)
            print(f"✅ Klien '{klien.name}' berhasil ditambahkan.")

        elif pilih == "7":
            name = input("Nama Vendor : ")
            service = input("Layanan     : ")
            contact = input("Kontak      : ")
            vendor = tambah_vendor(name, service, contact)
            print(f"✅ Vendor '{vendor.name}' berhasil ditambahkan.")

        elif pilih == "8":
            name = input("Nama Staff : ")
            role = input("Peran      : ")
            staff = tambah_staff(name, role)
            print(f"✅ Staff '{staff.name}' berhasil ditambahkan.")

        elif pilih == "9":
            name = input("Nama Barang Inventaris: ")
            item = tambah_inventaris(name)
            print(f"✅ Inventaris '{item.name}' berhasil ditambahkan.")

        elif pilih == "10":
            print("\n=== Tambah Catatan Keuangan ===")

            # Loop deskripsi
            while True:
                description = input("Deskripsi pengeluaran/pemasukan: ").strip()
                if description:
                    break
                else:
                    print("❌ Deskripsi tidak boleh kosong!")

            # Loop jumlah
            while True:
                amount_str = input("Jumlah (Rp): ").replace('.', '').replace(',', '').strip()
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        print("❌ Jumlah harus lebih dari 0.")
                        continue
                    break
                except ValueError:
                    print("❌ Jumlah harus angka valid! Contoh: 150000 atau 150.000")

            # Loop tipe transaksi
            while True:
                print("Tipe Transaksi:")
                print("1. Income (Pemasukan)")
                print("2. Expense (Pengeluaran)")
                tipe_input = input("Pilih tipe (1/2): ").strip()

                if tipe_input == "1":
                    tipe = "Income"
                    break
                elif tipe_input == "2":
                    tipe = "Expense"
                    break
                else:
                    print("❌ Pilihan tidak valid. Harus 1 atau 2.")

            record = tambah_keuangan(description, amount, tipe)

            # Format jumlah ke Rupiah
            formatted_amount = f"Rp {int(amount):,}".replace(',', '.')

            # Emoji berdasarkan tipe
            tipe_emoji = "💰" if tipe == "Income" else "💸"

            print("\n✅ Catatan berhasil ditambahkan!")
            print(f"  {tipe_emoji} {record.description}")
            print(f"     Tipe   : {record.type}")
            print(f"     Jumlah : {formatted_amount}")



        elif pilih == "11":
            laporan_keuangan()

        elif pilih == "12":
            print("👋 Terima kasih! Sampai jumpa.")
            break

        else:
            print("❌ Pilihan tidak valid!")

        input("\nTekan Enter untuk kembali ke menu...")  # biar ga ketumpuk print menu lagi

if __name__ == "__main__":
    main()
