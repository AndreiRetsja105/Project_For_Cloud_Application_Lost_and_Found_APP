"""SQLite database access function fro project lost and found, databse added in version (v0.3)"""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

# The python source code directory , keep the local databe outside 
DEFAULT_DB_PATH= Path (__file__).resolve().parent.parent /"data"/ "lost_fround_db"

def get_database_path() ->Path:
    """ return configured SQLite file path / loacal dafault path """
    return Path(os.environ.get("LOST_FROUND_DB_PATH", str(DEFAULT_DB_PATH)))

@contextmanager
def database_conection() -> Iterator[sqlite3.Connection]:
    """ open SQLITE conection and commit changes """
    """if an error occurs within the block, the changes are automatically rolled back"""

    database_path = get_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection= sqlite3.connect(database_path, timeout=10)
    connection.row_factory = sqlite3.Row #  return rows accesable by the column Name
    try:
        with connection:   # commit on acces (roll back on failure)
        
            yield connection
    
    finally:
        connection.close() # release the data base file after each opreation 

def initialse_database() -> None:
    """create < Item table > if not exist """ 
    with database_conection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL CHECK (category IN ('lost', 'found')),
                location TEXT NOT NULL, 
                status TEXT NOT NULL DEFAULT 'open'
            )
            """
        )


def list_items(category:str| None = None ) -> list[dict]:
     """ read all reports < filter by lost or found category >"""
     with database_conection() as connection:
        
        if category is None:
            rows = connection.execute("SELECT * FROM items ORDER BY id").fetchall()

        else:
            # using a bound parameter prevents user-supplied strings from being interpreted as SQL code.
            rows = connection.execute("SELECT * FROM items WHERE category = ? ORDER BY id", (category,)).fetchall()
        return [dict(row) for row in rows]

     
def find_item(item_id: int) -> dict| None:
    """return the report by ID, or None if no matching row is found"""
    with database_conection() as connection:
        row = connection.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        
        return dict(row) if row is not None else None


def insert_item(data: dict) -> dict:
    """insert the verified report and return the new saved row """
    
    with database_conection() as connection:
        cursor = connection.execute("INSERT INTO items (title, description, category, location) VALUES (?, ?, ?, ?)",(data["title"], data["description"], data["category"], data["location"], data["status"]),)
        item_id = cursor.lastrowid

    return find_item(item_id)


def replace_item(item_id: int, data: dict) -> dict | None:
    """replace the fields of the saved report; return None if its identifier is missing"""
    
    with database_conection() as connection:
        cursor = connection.execute(""" UPDATE items SET title = ?, description = ?, category = ?, location = ?, status = ? WHERE id = ? """,(data["title"], data["description"], data["category"], data["location"], data["status"], item_id),)
    
    if cursor.rowcount == 0 :
        return None
    
    return find_item(item_id)


def delete_item(item_id: int ) -> bool:
    """delete the saved report and indicate whether anything was deleted"""
    
    with database_conection() as connection:
        cursor = connection.execute("DELETE FROM items WHERE id = ?", (item_id,))
        
        return cursor.rowcount > 0

