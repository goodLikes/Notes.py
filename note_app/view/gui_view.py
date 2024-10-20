import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, Toplevel, Label, Frame
from controller.note_controller import NoteController

class GUIView:
    def __init__(self, controller: NoteController):
        self.controller = controller
        self.window = tk.Tk()
        self.window.title("|Notes| by Denis B/")
        self.window.geometry("600x400")

        self.note_listbox = Listbox(self.window)
        self.note_listbox.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        self.add_button = tk.Button(button_frame, text="Добавить ", command=self.add_note)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(button_frame, text="Редактировать ", command=self.edit_note)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(button_frame, text="Удалить ", command=self.delete_note)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.status_button = tk.Button(button_frame, text="Изменить статус", command=self.change_status)
        self.status_button.pack(side=tk.LEFT, padx=5)

        self.note_listbox.bind("<Double-Button-1>", self.show_note_details)

        self.display_notes()  

    def display_notes(self):
        """Отображение всех заметок в listbox с цветовой конфигурацией."""
        self.note_listbox.delete(0, tk.END)
        for index, note in enumerate(self.controller.get_notes(), start=1):
            display_text = f"{note.timestamp} | № {note.id} | {note.title} - {note.status}"
            self.note_listbox.insert(tk.END, display_text)
            self.note_listbox.itemconfig(index - 1, {'bg': note.color})  

    def add_note(self) -> None:
        """Добавление новой заметки с запросом заголовка, текста и цвета."""
        self.show_note_input_window(action="add")

    def edit_note(self) -> None:
        """Редактирование выбранной заметки."""
        selected_note_index = self.note_listbox.curselection()
        if not selected_note_index:
            return
        selected_note_id = self.controller.get_notes()[selected_note_index[0]].id
        current_note = self.controller.get_notes()[selected_note_index[0]]
        
        self.show_note_input_window(action="edit", note_id=selected_note_id, title=current_note.title, body=current_note.body, current_color=current_note.color)

    def show_note_input_window(self, action, note_id=None, title=None, body=None, current_color=None):
        """Отображает окно для ввода заголовка и тела заметки с выбором цвета."""
        input_window = Toplevel(self.window)
        input_window.title("Введите заметку")

        title_label = Label(input_window, text="Заголовок:")
        title_label.pack(pady=5)

        title_entry = tk.Entry(input_window, width=50)
        title_entry.pack(pady=5)
        title_entry.insert(0, title if title else "")

        body_label = Label(input_window, text="Описание заметки:")
        body_label.pack(pady=5)

        body_text = tk.Text(input_window, width=50, height=10)
        body_text.pack(pady=5)
        body_text.insert("1.0", body if body else "")

        color_var = tk.StringVar(value=current_color if current_color else 'gray')

        colors = ['red', 'green', 'blue', 'yellow', 'gray']
        for color in colors:
            rb = tk.Radiobutton(input_window, text=color.capitalize(), variable=color_var, value=color, bg=color)
            rb.pack(side=tk.LEFT)

        def confirm_input():
            selected_color = color_var.get()
            if action == "add":
                self.controller.add_note(title_entry.get(), body_text.get("1.0", tk.END).strip(), selected_color)
            elif action == "edit":
                self.controller.update_note_text(note_id, title_entry.get(), body_text.get("1.0", tk.END).strip())
                note_to_update = self.controller.get_note_by_id(note_id)
                note_to_update.color = selected_color
                self.controller.storage.update_note(note_to_update)
            input_window.destroy()
            self.display_notes()

        confirm_button = tk.Button(input_window, text="Подтвердить", command=confirm_input)
        confirm_button.pack(pady=10)

    def delete_note(self) -> None:
        """Удаление выбранной заметки."""
        selected_note_index = self.note_listbox.curselection()
        if selected_note_index:
            selected_note_id = self.controller.get_notes()[selected_note_index[0]].id
            self.controller.delete_note(selected_note_id)
            self.display_notes()

    def change_status(self) -> None:
        """Изменяет статус выбранной заметки."""
        selected_note_index = self.note_listbox.curselection()
        if selected_note_index:
            selected_note_id = self.controller.get_notes()[selected_note_index[0]].id
            new_status = simpledialog.askstring("Статус", "Введите новый статус:", initialvalue=self.controller.get_note_status(selected_note_id))
            if new_status:
                self.controller.edit_note(selected_note_id, status=new_status)
                self.display_notes()

    def show_note_details(self, event) -> None:
        """Показывает детали выбранной заметки."""
        selected_note_index = self.note_listbox.curselection()
        if not selected_note_index:
            return
        note = self.controller.get_notes()[selected_note_index[0]]
        messagebox.showinfo("Заметка", f"Заголовок: {note.title}\n\nОписание: {note.body}\n\nСтатус: {note.status}")
    
    def run(self) -> None:
        """Запускает главный цикл приложения."""
        self.window.mainloop()
