import sqlite3

path = "./data/employee_data.db"
def create_employee_table():
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rfids TEXT NOT NULL,
            pic_path TEXT
        )
    ''')
    conn.commit()
    conn.close()
def add_employee(name, rfids, pic_path=None): #rfids is a comma-separated string of RFID tags
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (name, rfids, pic_path)
        VALUES (?, ?, ?)
    ''', (name, rfids, pic_path))
    conn.commit()
    conn.close()

def get_employee_by_rfid(rfid):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    for emp in employees:
        emp_id, name, rfids, pic_path = emp
        rfid_list = [r.strip() for r in rfids.split(',')]
        if rfid in rfid_list:
            conn.close()
            return emp
    conn.close()
    return None


if __name__ == "__main__":
    create_employee_table()
    print("Employee table created successfully.")
    