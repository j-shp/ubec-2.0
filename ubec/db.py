import sqlite3
import numpy as np
import cv2
from typing import Optional, Tuple

"""

Mainly Database Operations

"""

class DatabaseManager:
    def __init__(self, db_path: str = 'images.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS detected_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_filename TEXT NOT NULL,
                processed_image BLOB NOT NULL,
                detection_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_entry(self, filename: str, image_bytes: bytes) -> bool:
        try:
            self.cursor.execute(
                "INSERT INTO detected_images (original_filename, processed_image) VALUES (?, ?)",
                (filename, image_bytes)
            )
            self.conn.commit()
            print(f"Created entry for: {filename}")
            return True
        except sqlite3.Error as e:
            print(f"Error creating entry: {e}")
            self.conn.rollback()
            return False

    def get_entry(self, filename: str) -> Optional[Tuple[str, bytes]]:
        try:
            self.cursor.execute(
                "SELECT original_filename, processed_image FROM detected_images WHERE original_filename = ?",
                (filename,)
            )
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving entry: {e}")
            return None

    def delete_entry(self, filename: str) -> bool:
        try:
            self.cursor.execute(
                "DELETE FROM detected_images WHERE original_filename = ?",
                (filename,)
            )
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"Deleted entry: {filename}")
                return True
            print(f"No entry found for: {filename}")
            return False
        except sqlite3.Error as e:
            print(f"Error deleting entry: {e}")
            self.conn.rollback()
            return False

    def close(self):
        self.conn.close()