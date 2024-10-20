import datetime

class Note:
    def __init__(self, note_id: int, title: str, body: str, color: str):
        self.id: int = note_id
        self.title: str = title
        self.body: str = body
        self.timestamp: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status: str = 'Не выполнено'
        self.color: str = color

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp,
            'status': self.status,
            'color': self.color
        }
