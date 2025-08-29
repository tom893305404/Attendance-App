# createDb.py
# 用於創建資料庫和員工表格

from employeeSql import create_employee_table
from sqlite import DatabaseManager


if __name__ == "__main__":
    create_employee_table()#創建員工表格
    db = DatabaseManager()#創建考勤表格
    db.create_table()
    print("Attendance table created successfully.")
    db.close()