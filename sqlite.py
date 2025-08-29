import sqlite3

class DatabaseManager:
    def __init__(self, db_name="./data/workforlife.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                name TEXT,
                am_in TEXT,
                am_out TEXT,
                pm_in TEXT,
                pm_out TEXT,
                ot_in TEXT,
                ot_out TEXT
            )
        ''')
        self.conn.commit()
    def insert_record(self, date, name, am_in=None, am_out=None, pm_in=None, pm_out=None, ot_in=None, ot_out=None):
        self.cursor.execute('''
            INSERT INTO attendance (date, name, am_in, am_out, pm_in, pm_out, ot_in, ot_out)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, name, am_in, am_out, pm_in, pm_out, ot_in, ot_out))
        self.conn.commit()
    def update_record(self, record_id, column, value):
        if column not in ['am_in', 'am_out', 'pm_in', 'pm_out', 'ot_in', 'ot_out']:
            raise ValueError("Invalid column name")
        self.cursor.execute(f'''
            UPDATE attendance
            SET {column} = ?
            WHERE id = ?
        ''', (value, record_id))
        self.conn.commit()
    def fetch_records(self, name, month):
        self.cursor.execute('''
            SELECT * FROM attendance
            WHERE name = ? AND strftime('%Y-%m', date) = ?
        ''', (name, month))
        return self.cursor.fetchall()
    def fetch_all_months_records(self, month):
        self.cursor.execute('''
            SELECT * FROM attendance
            WHERE strftime('%Y-%m', date) = ?
        ''', (month,))
        return self.cursor.fetchall()
    def fetch_record_by_name_and_date(self, name, date):
        self.cursor.execute('''
            SELECT * FROM attendance
            WHERE name = ? AND date = ?
        ''', (name, date))
        return self.cursor.fetchone()
    def close(self):
        self.conn.close()
if __name__ == "__main__":
    db = DatabaseManager()
    data = db.fetch_all_months_records("2025-08")
    print(data)
    db.close()
    # db = DatabaseManager()
    # db.create_table()
    # print("Attendance table created successfully.")
    # db.close()