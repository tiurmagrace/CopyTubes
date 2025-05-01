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

def validasi_tanggal(tanggal: str) -> bool:
    pola = r"^(0?[1-9]|[12][0-9]|3[01])\s(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)\s\d{4}$"
    return re.match(pola, tanggal.strip().lower()) is not None

def format_tanggal(tanggal: str) -> str:
    bagian = tanggal.strip().split(" ")
    if len(bagian) != 3:
        return tanggal
    hari, bulan, tahun = bagian
    return f"{int(hari)} {bulan.capitalize()} {tahun}"

def login():
    admin_username = "admin"
    admin_password = "1234"

    print("\n=== LOGIN ADMIN ===")
    username = input("Username: ")
    password = input("Password: ")

    if username == admin_username and password == admin_password:
        print("\n✅ Login berhasil!\n")
        return True
    else:
        print("\n❌ Username atau password salah. Akses ditolak.\n")
        return False

def tampilkan_menu():
    print("\n╔════════════════════════════════╗")
    print("║      CLI EVENT ORGANIZER       ║")
    print("╚════════════════════════════════╝")
    print("[1] Tambah Event")
    print("[2] Tambah Peserta ke Event")
    print("[3] Atur RSVP")
    print("[4] Lihat Semua Event")
    print("[5] Export Data ke File")
    print("[6] Tambah Klien")
    print("[7] Tambah Vendor")
    print("[8] Tambah Staff")
    print("[9] Tambah Inventaris")
    print("[10] Tambah Catatan Keuangan")
    print("[11] Lihat Laporan Keuangan")
    print("[12] Keluar")
    print("────────────────────────────────")

def main():
    if not login():
        return

    while True:
        tampilkan_menu()
        pilih = input("Pilih menu: ")

        if pilih == "1":
            print("\n────────────── Tambah Event ──────────────")
            title = input("Judul Event   : ")
            location = input("Lokasi        : ")

            while True:
                date = input("Tanggal       : ")
                if validasi_tanggal(date):
                    date = format_tanggal(date)
                    break
                else:
                    print("❌ Format tanggal tidak valid. Contoh: 01 Januari 2025 / 1 januari 2025")

            event = tambah_event(title, location, date)
            print("\n✅ Event berhasil ditambahkan!")
            print("────────────────────────────────────────────")
            print(f"📌 Judul   : {event.title}")
            print(f"📍 Lokasi  : {event.location}")
            print(f"📅 Tanggal : {event.date}")
            print(f"👥 Peserta : (belum ada peserta)")
            print("────────────────────────────────────────────")

        elif pilih == "2":
            print("\n────────── Tambah Peserta ──────────")
            if not events:
                print("❌ Belum ada event.")
            else:
                print("Daftar Event:")
                for i, e in enumerate(events):
                    print(f"[{i+1}] {e.title}")
                try:
                    idx = int(input("Pilih nomor event: ")) - 1
                    name = input("\nNama Peserta: ")
                    tambah_peserta(idx, name)
                    print(f"\n✅ Peserta '{name}' berhasil ditambahkan ke event '{events[idx].title}'.")
                except:
                    print("❌ Pilihan tidak valid.")

        elif pilih == "3":
            print("\n──────────── Atur RSVP ────────────")
            if not events:
                print("❌ Belum ada event.")
            else:
                print("Daftar Event:")
                for i, e in enumerate(events):
                    print(f"[{i+1}] {e.title}")
                try:
                    idx = int(input("Pilih event: ")) - 1
                    if not events[idx].participants:
                        print("❌ Belum ada peserta.")
                    else:
                        print("\n📋 Daftar Peserta:")
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

            while True:
                description = input("Deskripsi pengeluaran/pemasukan: ").strip()
                if description:
                    break
                else:
                    print("❌ Deskripsi tidak boleh kosong!")

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
            formatted_amount = f"Rp {int(amount):,}".replace(',', '.')
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

        input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()