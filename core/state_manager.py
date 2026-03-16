import sqlite3
import datetime

class StateManager:
    def __init__(self, db_path="edge_farm.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sensor Data Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            moisture REAL,
            nitrogen REAL,
            phosphorus REAL,
            potassium REAL,
            temperature REAL
        )
        ''')
        
        # Diagnostics Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnostics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            crop_type TEXT,
            disease_detected TEXT,
            confidence REAL
        )
        ''')

        # Chat History Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            role TEXT,
            message TEXT
        )
        ''')

        conn.commit()
        conn.close()

    def log_sensor_data(self, moisture, n, p, k, temp):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sensor_data (timestamp, moisture, nitrogen, phosphorus, potassium, temperature) VALUES (?, ?, ?, ?, ?, ?)',
                       (datetime.datetime.now(), moisture, n, p, k, temp))
        conn.commit()
        conn.close()

    def get_latest_sensor_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT moisture, nitrogen, phosphorus, potassium, temperature FROM sensor_data ORDER BY timestamp DESC LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {"moisture": row[0], "n": row[1], "p": row[2], "k": row[3], "temp": row[4]}
        return {"moisture": 42.0, "n": 120.0, "p": 40.0, "k": 60.0, "temp": 28.0} # Fallback dummy data

    def log_diagnostic(self, crop_type, disease, confidence):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO diagnostics (timestamp, crop_type, disease_detected, confidence) VALUES (?, ?, ?, ?)',
                       (datetime.datetime.now(), crop_type, disease, confidence))
        conn.commit()
        conn.close()
        
    def get_latest_diagnostic(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT crop_type, disease_detected, confidence FROM diagnostics ORDER BY timestamp DESC LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"crop": row[0], "disease": row[1], "confidence": row[2]}
        return {"crop": "Tomato", "disease": "Early Blight", "confidence": 89.0}

    def log_chat(self, role, message):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO chat_history (timestamp, role, message) VALUES (?, ?, ?)',
                       (datetime.datetime.now(), role, message))
        conn.commit()
        conn.close()

    def get_chat_history(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT role, message FROM chat_history ORDER BY timestamp ASC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [{"role": row[0], "message": row[1]} for row in rows]
