import tkinter as tk
from tkinter import ttk
import sqlite3

# Создание базы данных
connection = sqlite3.connect('employees.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        phone_number TEXT,
        email TEXT,
        salary REAL
    )
''')
connection.commit()

# Создание основного приложения
class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список сотрудников компании")

        # Создание виджетов
        self.tree = ttk.Treeview(self.root, columns=('id', 'full_name', 'phone_number', 'email', 'salary'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('full_name', text='ФИО')
        self.tree.heading('phone_number', text='Номер телефона')
        self.tree.heading('email', text='Адрес электронной почты')
        self.tree.heading('salary', text='Заработная плата')
        self.tree.pack()

        # Создание кнопок
        self.add_button = tk.Button(self.root, text="Добавить сотрудника", command=self.add_employee)
        self.add_button.pack()
        self.update_button = tk.Button(self.root, text="Обновить информацию", command=self.update_employee)
        self.update_button.pack()
        self.delete_button = tk.Button(self.root, text="Удалить сотрудника", command=self.delete_employee)
        self.delete_button.pack()

        # Создание поля для поиска
        self.search_label = tk.Label(self.root, text="Поиск по ФИО:")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="Найти", command=self.search_employee)
        self.search_button.pack()



    def add_employee(self):
        # Здесь код для добавления нового сотрудника
        name = "Иван Иванов"  # Предположим, что это вводится пользователем
        phone_number = "123456789"
        email = "ivan@example.com"
        salary = 50000

        cursor.execute('INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)', (name, phone_number, email, salary))
        connection.commit()
        self.show_employees()



    def update_employee(self):
        # Здесь код для обновления информации о сотруднике
        selected_item = self.tree.selection()[0]
        name = "Новое имя"  # Предположим, что это вводится пользователем
        phone_number = "987654321"
        email = "newemail@example.com"
        salary = 60000

        cursor.execute('UPDATE employees SET full_name=?, phone_number=?, email=?, salary=? WHERE id=?', (name, phone_number, email, salary, self.tree.set(selected_item, '#1')))
        connection.commit()
        self.show_employees()

    def delete_employee(self):
        # Здесь код для удаления сотрудника
        selected_item = self.tree.selection()[0]
        cursor.execute('DELETE FROM employees WHERE id=?', (self.tree.set(selected_item, '#1'),))
        connection.commit()
        self.show_employees()

    def search_employee(self):
        name = self.search_entry.get()
        cursor.execute('SELECT * FROM employees WHERE full_name LIKE ?', ('%' + name + '%',))
        records = cursor.fetchall()
        self.show_search_results(records)

    def show_search_results(self, records):
        for record in self.tree.get_children():
            self.tree.delete(record)
        for row in records:
            self.tree.insert('', 'end', values=row)

    def show_employees(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

        cursor.execute('SELECT * FROM employees')
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)

if __name__ == '__main__':
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    app.show_employees()  # Показать записи сотрудников при запуске приложения
    root.mainloop()