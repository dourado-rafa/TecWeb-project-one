from dataclasses import dataclass
from database import Database

@dataclass
class Note():
    title: str = None
    content: str = ''
    id: int = None


class NoteDatabase(Database):
    def __init__(self, database_name: str, path: str='data/') -> None:
        columns = [
            {'name': 'title',   'type': 'TEXT', 'restriction': ''},
            {'name': 'content', 'type': 'TEXT', 'restriction': 'NOT NULL'},
         ]
        super().__init__(database_name, 'note', columns, path)

    def add(self, note: Note) -> int:
        self.execute(f"INSERT INTO note (title, content) VALUES ('{note.title}', '{note.content}')")
        cursor = self.conn.execute('SELECT max(id) FROM note')
        for row in cursor:
            return row[0]
        
    def get(self, id: int) -> Note:
        cursor = self.conn.execute(f'SELECT title, content, id FROM note WHERE id = {id}')
        for row in cursor:
            return Note(row[0], row[1], row[2])

    def get_all(self) -> list:
        cursor = self.conn.execute('SELECT title, content, id FROM note')
        return [Note(row[0], row[1], row[2]) for row in cursor]

    def update(self, entry: Note) -> None:
        self.execute(f"UPDATE note SET title = '{entry.title}', content = '{entry.content}' WHERE id = {entry.id}")