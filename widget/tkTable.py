import tkinter as tk
from tkinter import ttk
import pandas as pd  # 匯入 pandas

    

def create_table(parent, columns=None, data=None, table_widths=None):
    """
    創建一個表格 (Treeview) 並插入資料，並提供欄位存取功能，支援 pandas.DataFrame。

    :param parent: 父元件 (例如 tk.Frame 或 tk.Tk)
    :param columns: 欄位名稱的列表 (例如 ["日期", "上午上班", "上午下班", ...])
    :param data: 要插入的資料 (例如 [(1, "Alice", 25), (2, "Bob", 30)] 或 pandas.DataFrame)
    :param table_widths: 每欄的寬度 (例如 [50, 150, 50])，可選
    :return: 返回創建的表格 (Treeview)
    """
    # 如果 data 是 pandas.DataFrame，提取欄位和資料
    if isinstance(data, pd.DataFrame):
        if columns is None:
            columns = list(data.columns)  # 使用 DataFrame 的欄位名稱
        data = data.values.tolist()  # 將 DataFrame 轉換為列表
    # Create a style
    style = ttk.Style()
    # You can give the font a name and size
    my_font = ("Arial", 12)  # font name and size
    style.configure("Treeview", font=my_font,rowheight= 30)  # For the treeview content
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"))  # For the header

    # 創建Treeview表格
    table = ttk.Treeview(parent, columns=columns, show="headings",height=16)

    # 定義每一欄的標題和寬度
    for i, col in enumerate(columns):
        table.heading(col, text=col)
        width = table_widths[i] if table_widths and i < len(table_widths) else 100
        table.column(col, width=width, anchor="center", stretch=False)
    
    #屏蔽對table的滑鼠選取
    def disable_event(event):
        return "break"
    table.bind("<Button-1>", disable_event)
    # 插入資料
    for row in data:
        table.insert("", tk.END, values=row)
    

    def get_all_rows():
        """取得所有列的資料"""
        rows = []
        for item in table.get_children():
            rows.append(table.item(item, "values"))
        return rows

    def update_row(item_id, values):
        """更新指定列的資料"""
        table.item(item_id, values=values)
    def update_cell(item_id, column, value):
        """更新指定儲存格的資料"""
        current_values = list(table.item(item_id, "values"))
        if column in columns:
            col_index = columns.index(column)
            current_values[col_index] = value
            table.item(item_id, values=current_values)
        else:
            raise ValueError(f"Column '{column}' does not exist.")
    def to_dataframe():
        """將表格資料轉換為 pandas.DataFrame"""
        rows = get_all_rows()
        return pd.DataFrame(rows, columns=columns)
    def clear_table():
        """清空表格資料"""
        for item in table.get_children():
            table.delete(item)
    def insert_df(data):
        """插入 pandas.DataFrame 資料"""
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame.")
        clear_table()
        for row in data.values.tolist():
            table.insert("", tk.END, values=row)
        table.update_idletasks()  # 更新顯示
    

    # 將操作方法綁定到表格物件
    table.get_all_rows = get_all_rows
    table.update_row = update_row
    table.to_dataframe = to_dataframe
    table.update_cell = update_cell        
    table.clear_table = clear_table
    table.insert_df = insert_df




    return table

# 測試函數
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Table Example")

    # 測試資料
    data = pd.DataFrame({
        "日期": [4, 5, 6],
        "上午上班": ["09:00", "09:15", "09:05"],
        "上午下班": ["12:00", "12:05", "12:10"],
        "下午上班": ["13:00", "13:10", "13:05"],
        "下午下班": ["18:00", "18:15", "18:05"],
        "加班上班": ["19:00", "", "19:05"],
        "加班下班": ["21:00", "", "21:10"]
    })

    table_widths = [50, 100, 100, 100, 100, 100, 100]

    # 創建表格
    table = create_table(root, data=data, table_widths=table_widths)

    # 測試所有操作方法
    def test_operations():
        print("=== 測試操作方法 ===")

        print("所有資料:")
        print(table.get_all_rows())
        # 3. 更新第二列資料
        print("更新第二列資料...")
        second_item = table.get_children()[1]  # 取得第二列的ID
        table.update_row(second_item, (2, "09:30", "12:30", "13:30", "18:30", "19:30", "21:30"))
        print("所有資料:")
        print(table.get_all_rows())

        #update cell
        third_item = table.get_children()[2]
        print("更新第二列 '上午上班' 儲存格資料...")
        table.update_cell(third_item, "上午上班", "10:00")
        print("所有資料:")
        print(table.get_all_rows())


    # 測試按鈕
    bt1 = tk.Button(root, text="Test Operations", command=test_operations)
    table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    bt1.pack()

    root.mainloop()