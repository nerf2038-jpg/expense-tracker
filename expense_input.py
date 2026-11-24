"""
Expense Tracker - Input Module (Member A)

讓使用者輸入多筆支出 (date, amount, category, note)，並存到 data/expenses.csv。
Visualization module (Member B) 會讀取同一個 CSV 來畫 pie chart。
"""

import csv
import os
from datetime import date, datetime

# 共用設定：B 的程式也要讀同一個檔案、同樣的欄位
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "expenses.csv")
FIELDNAMES = ["date", "amount", "category", "note"]
CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Other"]


def ensure_data_file():
    """若 CSV 不存在，就建立資料夾和含標題列的空檔案。"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()


def ask_date():
    """輸入日期 (YYYY-MM-DD)，直接按 Enter 代表今天。"""
    while True:
        raw = input(f"Date (YYYY-MM-DD) [Enter = {date.today()}]: ").strip()
        if raw == "":
            return date.today().isoformat()
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("  Invalid date format, please use YYYY-MM-DD (e.g. 2026-11-24).")


def ask_amount():
    """輸入金額，必須是大於 0 的數字。"""
    while True:
        raw = input("Amount: ").strip()
        try:
            amount = float(raw)
        except ValueError:
            print("  Please enter a number.")
            continue
        if amount <= 0:
            print("  Amount must be greater than 0.")
            continue
        return round(amount, 2)


def ask_category():
    """從預設分類中選擇，或輸入自訂分類。"""
    for i, name in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {name}")
    while True:
        raw = input("Category (number or custom name): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(CATEGORIES):
            return CATEGORIES[int(raw) - 1]
        if raw and not raw.isdigit():
            return raw.title()
        print("  Please choose a number from the list or type a category name.")


def add_expense(expense_date, amount, category, note=""):
    """把一筆支出寫入 CSV（供其他程式呼叫或測試使用）。"""
    ensure_data_file()
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerow({
            "date": expense_date,
            "amount": amount,
            "category": category,
            "note": note,
        })


def load_expenses():
    """讀取所有支出，回傳 list of dict。"""
    ensure_data_file()
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add_expenses_interactive():
    """連續輸入多筆支出，直到使用者選擇停止。"""
    while True:
        print("\n--- New expense ---")
        expense_date = ask_date()
        amount = ask_amount()
        category = ask_category()
        note = input("Note (optional): ").strip()
        add_expense(expense_date, amount, category, note)
        print(f"  Saved: {expense_date} | {amount} | {category} | {note}")

        again = input("Add another? (y/n) [y]: ").strip().lower()
        if again == "n":
            break


def show_expenses():
    """以表格列出目前所有支出與總額。"""
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print(f"\n{'Date':<12}{'Amount':>10}  {'Category':<15}Note")
    print("-" * 50)
    total = 0.0
    for e in expenses:
        amount = float(e["amount"])
        total += amount
        print(f"{e['date']:<12}{amount:>10.2f}  {e['category']:<15}{e['note']}")
    print("-" * 50)
    print(f"{'Total':<12}{total:>10.2f}  ({len(expenses)} records)")


def main():
    ensure_data_file()
    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add expenses")
        print("2. Show all expenses")
        print("3. Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            add_expenses_interactive()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            print(f"Data saved in {DATA_FILE}. Bye!")
            break
        else:
            print("Invalid option, please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
