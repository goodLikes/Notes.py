import json
import os
from .note import Note

class NoteStorage:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes: list[Note] = []
        self.load_notes()

    def get_all_notes(self) -> list[Note]:
        return self.notes

    def add_note(self, title: str, body: str, color: str) -> None:
        note_id = self.get_next_id()
        new_note = Note(note_id, title, body, color)
        self.notes.append(new_note)
        self.save_notes()

    def get_note_by_id(self, note_id: int) -> Note | None:
        return next((note for note in self.notes if note.id == note_id), None)

    def update_note(self, updated_note: Note) -> None:
        for i, note in enumerate(self.notes):
            if note.id == updated_note.id:
                self.notes[i] = updated_note
                self.save_notes()
                return

    def delete_note(self, note_id: int) -> None:
        self.notes = [note for note in self.notes if note.id != note_id]
        self.save_notes()

    def save_notes(self) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([note.to_dict() for note in self.notes], f, ensure_ascii=False)

    def load_notes(self) -> None:
        if not os.path.exists(self.filename):
            return  # Если файл не найден, просто пропускаем
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                notes_data = json.load(f)
                for note_data in notes_data:
                    note = Note(note_data['id'], note_data['title'], note_data['body'], note_data['color'])
                    note.timestamp = note_data['timestamp']
                    note.status = note_data['status']
                    self.notes.append(note)
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON. Проверьте файл.")

    def get_next_id(self) -> int:
        return len(self.notes) + 1 if self.notes else 1
