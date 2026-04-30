import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.entries = []
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.root, text="Температура (°C):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.temp_entry = tk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.root, text="Описание погоды:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.root, text="Осадки:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.rain_var = tk.BooleanVar()
        tk.Checkbutton(self.root, variable=self.rain_var).grid(row=3, column=1, sticky="w")

        # Кнопка добавления
        tk.Button(self.root, text="Добавить запись", command=self.add_entry).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения
        self.tree = ttk.Treeview(self.root, columns=("Date", "Temp", "Desc", "Rain"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Температура")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Rain", text="Осадки")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Фильтры
        tk.Label(self.root, text="Фильтр по дате:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.filter_date_entry = tk.Entry(self.root)
        self.filter_date_entry.grid(row=6, column=1, padx=5, pady=2)

        tk.Label(self.root, text="Фильтр по температуре (>):").grid(row=7, column=0, sticky="w", padx=5, pady=2)
        self.filter_temp_entry = tk.Entry(self.root)
        self.filter_temp_entry.grid(row=7, column=1, padx=5, pady=2)

        tk.Button(self.root, text="Применить фильтры", command=self.apply_filters).grid(row=8, column=0, columnspan=2, pady=5)
        tk.Button(self.root, text="Сбросить фильтры", command=self.reset_filters).grid(row=9, column=0, columnspan=2, pady=5)

        # Кнопки сохранения/загрузки
        tk.Button(self.root, text="Сохранить в JSON", command=self.save_data).grid(row=10, column=0, pady=10)
        tk.Button(self.root, text="Загрузить из JSON", command=self.load_data).grid(row=10, column=1, pady=10)

        self.update_table()

    # Продолжение кода — см. следующие шаги
    def validate_input(self):
        """Проверка корректности ввода данных"""
        try:
            date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD")
            return False

        try:
            temp = float(self.temp_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return False

        desc = self.desc_entry.get().strip()
        if not desc:
            messagebox.showerror("Ошибка", "Описание не может быть пустым")
            return False

        return True
    def add_entry(self):
        """Добавление новой записи"""
        if not self.validate_input():
            return

        entry = {
            "date": self.date_entry.get(),
            "temperature": float(self.temp_entry.get()),
            "description": self.desc_entry.get(),
            "rain": self.rain_var.get()
        }

        self.entries.append(entry)
        self.update_table()
        self.clear_inputs()
        messagebox.showinfo("Успех", "Запись добавлена!")

    def clear_inputs(self):
        """Очистка полей ввода"""
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.rain_var.set(False)
    def save_data(self):
        """Сохранение данных в JSON-файл"""
        with open("weather_data.json", "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в weather_data.json")

    def load_data(self):
        """Загрузка данных из JSON-файла"""
        try:
            with open("weather_data.json", "r", encoding="utf-8") as f:
                self.entries = json.load(f)
            self.update_table()
            messagebox.showinfo("Успех", "Данные загружены из weather_data.json")
        except FileNotFoundError:
            self.entries = []
    def update_table(self, filtered_entries=None):
        """Обновление таблицы с записями"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        entries = filtered_entries if filtered_entries is not None else self.entries

        for entry in entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                f"{entry['temperature']}°C",
                entry["description"],
                "Да" if entry["rain"] else "Нет"
            ))

    def apply_filters(self):
        """Применение фильтров"""
        filtered = self.entries

        date_filter = self.filter_date_entry.get().strip()
        if date_filter:
            filtered = [e for e in filtered if e["date"] == date_filter]

        temp_filter = self.filter_temp_entry.get().strip()
        if temp_filter:
            try:
                temp_threshold = float(temp_filter)
                filtered = [e for e in filtered if e["temperature"] > temp_threshold]
            except ValueError:
                messagebox.showerror("Ошибка", "Температура фильтра должна быть числом")
                return

        self.update_table(filtered)

    def reset_filters(self):
        """Сброс фильтров"""
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.update_table()

    # Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()