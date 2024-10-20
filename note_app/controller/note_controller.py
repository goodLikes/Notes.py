from model.note_storage import NoteStorage
from model.note import Note

class NoteController:
    def __init__(self, storage: NoteStorage):
        self.storage = storage

    def get_notes(self) -> list[Note]:
        return self.storage.get_all_notes()

    def add_note(self, title: str, body: str, color: str) -> None:
        self.storage.add_note(title, body, color)

    def get_note_by_id(self, note_id: int) -> Note | None:
        return self.storage.get_note_by_id(note_id)

    def update_note_text(self, note_id: int, new_title: str, new_body: str) -> None:
        note = self.get_note_by_id(note_id)
        if note:
            note.title = new_title
            note.body = new_body
            self.storage.update_note(note)

    def delete_note(self, note_id: int) -> None:
        self.storage.delete_note(note_id)

    def get_note_status(self, note_id: int) -> str | None:
        note = self.storage.get_note_by_id(note_id)
        return note.status if note else None

    def edit_note(self, note_id: int, status: str | None = None, color: str | None = None) -> None:
        note = self.storage.get_note_by_id(note_id)
        if note:
            if status:
                note.status = status
            if color:
                note.color = color
            self.storage.update_note(note)
