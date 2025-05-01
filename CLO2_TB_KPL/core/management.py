from models.client import Client
from models.vendor import Vendor
from models.staff import Staff
from models.inventory import InventoryItem
from models.finance import FinanceRecord
from typing import List

clients: List[Client] = []
vendors: List[Vendor] = []
staffs: List[Staff] = []
inventories: List[InventoryItem] = []
finances: List[FinanceRecord] = []

# Manajemen Klien
def tambah_klien(name: str, contact: str, address: str) -> Client:
    new_client = Client(name, contact, address)
    clients.append(new_client)
    return new_client

# Manajemen Vendor
def tambah_vendor(name: str, service: str, contact: str) -> Vendor:
    new_vendor = Vendor(name, service, contact)
    vendors.append(new_vendor)
    return new_vendor

# Manajemen Staff
def tambah_staff(name: str, role: str) -> Staff:
    new_staff = Staff(name, role)
    staffs.append(new_staff)
    return new_staff

# Manajemen Inventaris
def tambah_inventaris(name: str) -> InventoryItem:
    new_item = InventoryItem(name)
    inventories.append(new_item)
    return new_item

# Manajemen Keuangan
def tambah_keuangan(description: str, amount: float, type: str) -> FinanceRecord:
    type = type.title()  # Pastikan type selalu "Income" atau "Expense"
    new_record = FinanceRecord(description, amount, type)
    finances.append(new_record)
    return new_record

# Pelaporan sederhana
def laporan_keuangan():
    total_income = sum(r.amount for r in finances if r.type == "Income")
    total_expense = sum(r.amount for r in finances if r.type == "Expense")
    saldo = total_income - total_expense

    print("\n--- Laporan Keuangan ---")
    print(f"Pemasukan  : Rp{total_income:,.2f}")
    print(f"Pengeluaran: Rp{total_expense:,.2f}")
    print(f"Saldo      : Rp{saldo:,.2f}")
