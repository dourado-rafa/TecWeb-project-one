import sqlite3
from abc import ABC, abstractmethod

class Database(ABC):
    def __init__(self, database_name: str, table_name: str, columns: list, path: str) -> None:
        self.database_name = database_name
        self.table_name = table_name
        self.conn = sqlite3.connect(path+database_name+'.db')
        
        columns.append({'name': 'id', 'type': 'INTEGER', 'restriction': 'PRIMARY KEY'})
        columns_instruction = [f"{column['name']} {column['type']} {column['restriction']}" for column in columns]
        self.conn.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ({", ".join(columns_instruction)});')

    def execute(self, action: str) -> None:
        self.conn.execute(action)
        self.conn.commit()

    @abstractmethod
    def add(self) -> None:
        ...

    @abstractmethod
    def get_all(self) -> list:
        ...

    @abstractmethod
    def update(self) -> None:
        ...

    def delete(self, id: int) -> None:
        self.execute(f"DELETE FROM {self.table_name} WHERE id = {id}")
