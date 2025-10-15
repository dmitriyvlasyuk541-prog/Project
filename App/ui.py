import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
import csv

# Импортируем функции генерации и открытия браузера
from generator import generate_pairs
from browser import open_in_incognito


# Путь к файлу, куда будут сохраняться данные
OUT_FILE = Path(__file__).parent / "human_creds.csv"


# ---------- Функция сохранения CSV ----------
def save_to_csv(rows):
    """Сохраняет сгенерированные пары логин/пароль в CSV-файл."""
    with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "Password", "CreatedUTC"])
        writer.writerows(rows)
    messagebox.showinfo("Сохранено", f"✅ Сохранено в {OUT_FILE.name}")


# ---------- Класс интерфейса приложения ----------
class GeneratorApp(ctk.CTk):
    """Главное окно приложения (на CustomTkinter)."""

    def __init__(self):
        super().__init__()

        # --- Настройки окна ---
        self.title("Генератор логинов и паролей")
        self.geometry("800x600")

        # Устанавливаем тему оформления (тёмная + синяя цветовая схема)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Переменные интерфейса ---
        # Они автоматически связаны с элементами ввода (Entry, CheckBox и т.д.)
        self.qty_var = ctk.StringVar(value="10")       # количество логинов
        self.len_var = ctk.StringVar(value="14")       # длина пароля
        self.save_var = ctk.BooleanVar(value=True)     # сохранять ли в CSV
        self.symbols_var = ctk.BooleanVar(value=True)  # использовать ли символы в паролях

        # --- Верхняя панель параметров ---
        frame = ctk.CTkFrame(self)
        frame.pack(pady=15, padx=15, fill="x")

        # Метки и поля ввода
        ctk.CTkLabel(frame, text="Количество логинов:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(frame, textvariable=self.qty_var, width=70).grid(row=0, column=1, padx=10)

        ctk.CTkLabel(frame, text="Длина пароля:").grid(row=0, column=2, padx=10)
        ctk.CTkEntry(frame, textvariable=self.len_var, width=70).grid(row=0, column=3, padx=10)

        # Чекбоксы
        ctk.CTkCheckBox(frame, text="Сохранять в CSV", variable=self.save_var).grid(row=1, column=0, padx=10)
        ctk.CTkCheckBox(frame, text="Использовать символы", variable=self.symbols_var).grid(row=1, column=1, padx=10)

        # Кнопка генерации
        ctk.CTkButton(frame, text="🎲 Сгенерировать", command=self.generate).grid(row=1, column=3, padx=10)

        # --- Поле вывода результатов ---
        self.textbox = ctk.CTkTextbox(self, width=760, height=400, font=("Consolas", 13))
        self.textbox.pack(padx=10, pady=10)

        # --- Нижняя панель с кнопками ---
        bottom = ctk.CTkFrame(self)
        bottom.pack(pady=5)

        # Кнопка копирования всех данных
        ctk.CTkButton(bottom, text="📋 Скопировать всё", command=self.copy_all).grid(row=0, column=0, padx=10)

        # Кнопка открытия браузера в инкогнито
        ctk.CTkButton(bottom, text="🌐 Открыть сайт в инкогнито", command=self.open_preview).grid(row=0, column=1, padx=10)

        # Кнопка выхода из приложения
        ctk.CTkButton(bottom, text="Выход", command=self.destroy).grid(row=0, column=2, padx=10)

    # ---------- Метод генерации ----------
    def generate(self):
        """Создаёт указанное количество логинов и паролей."""
        self.textbox.delete("0.0", "end")  # очищаем текстовое поле

        try:
            qty = int(self.qty_var.get())      # количество логинов
            length = int(self.len_var.get())   # длина пароля
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа.")
            return

        # Генерация пар логин/пароль через модуль generator.py
        pairs = generate_pairs(qty, length, self.symbols_var.get())

        # Выводим результат в окно
        for username, password, _ in pairs:
            self.textbox.insert("end", f"{username} : {password}\n")

        # Сохраняем в CSV при необходимости
        if self.save_var.get():
            save_to_csv(pairs)

    # ---------- Метод копирования ----------
    def copy_all(self):
        """Копирует всё содержимое поля в буфер обмена."""
        text = self.textbox.get("0.0", "end").strip()
        if not text:
            messagebox.showinfo("Инфо", "Нет данных для копирования.")
            return

        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("✅", "Скопировано в буфер обмена.")

    # ---------- Метод открытия браузера ----------

    def open_preview(self):
        """Открывает сразу две вкладки (Outlook + Steam) в инкогнито."""
        urls = [
            "https://login.live.com",
            "https://store.steampowered.com/"
        ]
        try:
            open_in_incognito(urls)  # ← без browser=
            messagebox.showinfo("Запуск", "🌐 Браузер открыт в инкогнито.\nВкладки: Outlook + Steam")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
