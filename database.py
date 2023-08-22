import sqlite3
from dataclasses import dataclass

@dataclass
class Note():
    title: str = None
    content: str = ''
    id: int = None


class Database():
    def __init__(self, database_name: str) -> None:
        self.conn = sqlite3.connect(database_name+'.db')
        self.conn.execute('CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL);')

    def add(self, note: Note) -> None:
        self.conn.execute(f"INSERT INTO note (title, content) VALUES ('{note.title}', '{note.content}')")
        self.conn.commit()

    def get_all(self) -> list:
        cursor = self.conn.execute('Select title, content, id FROM note')
        return [Note(row[0], row[1], row[2]) for row in cursor]

    def update(self, entry: Note) -> None:
        self.conn.execute(f"UPDATE note SET title = '{entry.title}', content = '{entry.content}' WHERE id = {entry.id}")
        self.conn.commit()

    def delete(self, id=int) -> None:
        self.conn.execute(f"DELETE FROM note WHERE id = {id}")
        self.conn.commit()
