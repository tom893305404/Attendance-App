import tkinter as tk
from tkinter import font
import locale
from datetime import datetime
from functools import partial
from tkinter import messagebox  # 匯入 messagebox
from tkinter import filedialog

import pandas as pd
from employeeSql import get_employee_by_rfid
from widget.tkTable import create_table
from widget.tkClock import DigitalClock
import sqlite3
from sqlite import DatabaseManager


# 設置本地化以顯示中文日期和月份名稱
locale.setlocale(locale.LC_TIME, 'zh_TW.UTF-8')
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
def show_panel(panel):
    # 隱藏所有Panel
    for p in panels:
        p.grid_forget()
    # 顯示選定的Panel
    panel.grid(row=1, column=0, sticky="nsew")  # 使用sticky填充整個空間
    if panel == panel1:
        focus_on_hidden_entry()
    elif panel == panel2:
        focus_on_hidden_entry2()
    elif panel == panel3:
        focus_on_entry3()
def is_number(s):
    try:
        float(s)  # 尝试将字符串转换为浮点数
        return True
    except ValueError:
        return False



root = tk.Tk()
root.title("WorkForLife2025.08.24")
# root.attributes('-zoomed', True)  # 有些 Linux 支援
root.state('zoomed')


# 創建一個Panel，並設置背景色
button_panel = tk.Frame(root, bg="gray")
button_panel.grid(row=0, column=0, sticky="ew")  # 使用sticky使Panel填充水平空間

# 創建一個字體對象
font1 = font.Font(family="Times New Roman", size=18, weight="bold")
# 創建四個按鈕，每個按鈕對應一個Panel
button1 = tk.Button(button_panel,width=12,height=3, text="打卡",font=font1, command=lambda: show_panel(panel1))
button2 = tk.Button(button_panel,width=12,height=3, text="紀錄",font=font1, command=lambda: show_panel(panel2))
button3 = tk.Button(button_panel,width=12,height=3, text="其他",font=font1, command=lambda: show_panel(panel3))

# 使用grid佈局管理器排列按鈕
button1.grid(row=0, column=0)
button2.grid(row=0, column=1)
button3.grid(row=0, column=2)

# 創建四個Panel，並設置背景色
panel1 = tk.Frame(root, bg="lightyellow")
panel2 = tk.Frame(root, bg="lightblue")
panel3 = tk.Frame(root, bg="peach puff")

#/////////////////////////////////////////Panel1 打卡
# 創建一個StringVar來存儲uid
employee_name = tk.StringVar()
global worktime
worktime = '上班1'  # 用於存儲上班時間的變量
P1_font2 = font.Font(family="Times New Roman", size=24, weight="bold")
tabledata = pd.DataFrame(columns=["日期", "上班1", "下班1", "上班2", "下班2", "上班3", "下班3"])

for i in range(1, 32):
    tabledata.loc[i] = [i, "", "", "", "", "", ""]


def focus_on_hidden_entry(event=None):
    """將游標移動到卡號輸入框"""
    P1_sub_panel_hidden_entry1.focus_set()


def BeepCard(event=None):
    card_id = P1_sub_panel_hidden_entry1.get().strip()  # 獲取輸入框的值 (卡號)
    if not card_id:
        print("未讀取到卡號")
        P1_sub_panel_hidden_entry1.delete(0, tk.END)  # 清空輸入框
        return
    print("讀取到卡號:", card_id)
    emyployee = get_employee_by_rfid(card_id)
    # print("員工資料:", emyployee)
    #根據讀到的rfid，把該員工的姓名顯示出來，把這個月當前的資料也顯示出來
    if not emyployee:
        print("未找到對應的員工資料")
        messagebox.showwarning("警告", "未找到對應的員工資料")
        P1_sub_panel_hidden_entry1.delete(0, tk.END)  # 清空輸入框
        return

    emp_id, name, rfids, pic_path = emyployee
    employee_name.set(name)# 顯示員工姓名
    datetime_now = datetime.now()
    manager = DatabaseManager()
    old_records = manager.fetch_records(name=name, month=datetime_now.strftime("%Y-%m"))
    # print("當月舊紀錄:", old_records)
    
    #將舊資料更新到兩個table中
    # 先建立一個 31 天的空表格
    tabledata = pd.DataFrame(
    [[i, "", "", "", "", "", ""] for i in range(1, 32)],
    columns=["日期", "上班1", "下班1", "上班2", "下班2", "上班3", "下班3"]
    )

    # 把舊紀錄塞進 DataFrame
    for record in old_records:
        rec_id, date, rfid_id, am_in, am_out, pm_in, pm_out, ot_in, ot_out = record
        d = datetime.strptime(date, "%Y-%m-%d").day
        tabledata.loc[d-1] = [d, am_in or "", am_out or "", pm_in or "", pm_out or "", ot_in or "", ot_out or ""]
    #新紀錄的話，更新tabledata
    
    tabledata.loc[datetime_now.day-1, worktime] = datetime_now.strftime("%H:%M")

    P1_sub_panel2_table1.insert_df(tabledata[:16])
    P1_sub_panel2_table2.insert_df(tabledata[16:32])
    
    # print("當前時間:", datetime_now.strftime("%H:%M"))
    #把當前的打卡時間更新到資料庫
    # 檢查當天是否已有資料
    existing_record = manager.fetch_record_by_name_and_date(name=name, date=datetime_now.strftime("%Y-%m-%d"))
    if existing_record:
        record_id = existing_record[0]
        #把worktime轉換為資料庫的欄位名稱
        wt = worktime.replace("上班1", "am_in").replace("下班1", "am_out").replace("上班2", "pm_in").replace("下班2", "pm_out").replace("上班3", "ot_in").replace("下班3", "ot_out")
        
        #檢查是更新哪一個欄位，如果該欄位已經有值，表示在同一個時間重複beep卡
        if existing_record[3 + ["am_in", "am_out", "pm_in", "pm_out", "ot_in", "ot_out"].index(wt)]:
            print(f"{worktime} 已經有打卡紀錄，無法重複打卡")
            messagebox.showwarning("警告", f"{worktime} 已經有打卡紀錄，無法重複打卡")
            P1_sub_panel_hidden_entry1.delete(0, tk.END)  # 清空輸入框
        else:
            manager.update_record(record_id, wt, datetime_now.strftime("%H:%M"))
            print(f"更新紀錄ID {record_id} 的 {worktime} 為 {datetime_now.strftime('%H:%M')}")
    else:
        manager.insert_record(date=datetime_now.strftime("%Y-%m-%d"), name=name, **{worktime.replace("上班1", "am_in").replace("下班1", "am_out").replace("上班2", "pm_in").replace("下班2", "pm_out").replace("上班3", "ot_in").replace("下班3", "ot_out"): datetime_now.strftime("%H:%M")})   
    manager.close()       
    
    P1_sub_panel_hidden_entry1.delete(0, tk.END)  # 清空輸入框

P1_sub_panel1 = tk.Frame(panel1, bg="lightyellow")  # 用於顯示員工照片和姓名的子Panel
P1_sub_panel1_label1 = tk.Label(P1_sub_panel1, text="員工:", font=P1_font2, bg='lightyellow')  # 提示文字
P1_sub_panel1_label2 = tk.Label(P1_sub_panel1, textvariable= employee_name, bg='lightyellow', font=P1_font2)# 卡號顯示
P1_sub_panel_hidden_entry1 = tk.Entry(P1_sub_panel1, font=P1_font2, width=0) # 隱藏輸入框
#排版
P1_sub_panel1_label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")  
P1_sub_panel1_label2.grid(row=0, column=1, padx=10, pady=10, sticky="w")  
P1_sub_panel_hidden_entry1.place(x=-100, y=-100)
#事件
P1_sub_panel_hidden_entry1.bind("<Return>", BeepCard)


P1_sub_panel2 = tk.Frame(panel1, bg="lightyellow")  # 用於顯示打卡紀錄的子Panel
P1_sub_panel2_table1 = create_table(P1_sub_panel2,data=tabledata[:16],table_widths=[60, 60, 60, 60, 60, 60, 60])  # 打卡紀錄表格
P1_sub_panel2_table2 = create_table(P1_sub_panel2,data=tabledata[16:32],table_widths=[60, 60, 60, 60, 60, 60, 60])  # 打卡紀錄表格
#排版
P1_sub_panel2_table1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
P1_sub_panel2_table2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

P1_sub_panel3_buttons={}
def P1_sub_panel3_button_action(num,key=None):
        #num: 按鈕編號 0-5
        global worktime
        worktime = key
        for btn in P1_sub_panel3_buttons:
            btn.config(bg="lightgray")  # 恢復原來的顏色
        P1_sub_panel3_buttons[num].config(bg="#f7510f")  # 按下的按鈕變色
        # print(f"設定打卡時間為: {worktime}")  # 打印按鈕動作
    
P1_sub_panel3 = tk.Frame(panel1, bg="lightyellow")  # 用於顯示打卡按鈕的子Panel
P1_sub_panel3_button1 = tk.Button(P1_sub_panel3, text="上班1", font=P1_font2, width=6, height=2, command=lambda:P1_sub_panel3_button_action(0,"上班1"),bg="#f7510f")
P1_sub_panel3_button2 = tk.Button(P1_sub_panel3, text="下班1", font=P1_font2, width=6, height=2, command=lambda:P1_sub_panel3_button_action(1,"下班1"))
P1_sub_panel3_button3 = tk.Button(P1_sub_panel3, text="上班2", font=P1_font2, width=6, height=2, command=lambda:P1_sub_panel3_button_action(2,"上班2"))
P1_sub_panel3_button4 = tk.Button(P1_sub_panel3, text="下班2", font=P1_font2, width=6, height=2, command=lambda:P1_sub_panel3_button_action(3,"下班2"))
P1_sub_panel3_button5 = tk.Button(P1_sub_panel3, text="上班3", font=P1_font2, width=6, height=2, command=lambda:P1_sub_panel3_button_action(4,"上班3"))
P1_sub_panel3_button6 = tk.Button(P1_sub_panel3, text="下班3", font=P1_font2, width=6, height=2, command=lambda:P1_sub_panel3_button_action(5,"下班3"))
P1_sub_panel3_buttons = [P1_sub_panel3_button1, P1_sub_panel3_button2, P1_sub_panel3_button3, P1_sub_panel3_button4, P1_sub_panel3_button5, P1_sub_panel3_button6]

# 排版
P1_sub_panel3_button1.grid(row=0, column=0, padx=5, pady=5)
P1_sub_panel3_button2.grid(row=0, column=1, padx=5, pady=5)
P1_sub_panel3_button3.grid(row=0, column=2, padx=5, pady=5)
P1_sub_panel3_button4.grid(row=0, column=3, padx=5, pady=5)
P1_sub_panel3_button5.grid(row=0, column=4, padx=5, pady=5)
P1_sub_panel3_button6.grid(row=0, column=5, padx=5, pady=5)


# 時鐘小部件
P1_sub_panel4 = tk.Frame(panel1, bg="lightyellow")  # 用於顯示時鐘的子Panel
P1_clock = DigitalClock(P1_sub_panel4)
P1_clock.pack(padx=10, pady=10)

P1_sub_panel1.grid(row=0, column=0, sticky="w")
P1_sub_panel2.grid(row=1, column=0, sticky="nsw")
P1_sub_panel3.grid(row=2, column=0, sticky="ew")
P1_sub_panel4.grid(row=1, column=1, sticky="ns")


#////////////////////////////////////////////////////////////end of Panel1 打卡
#//////////////////////////////////////////////////////////////Panel2 紀錄
# Panel2 紀錄
P2_employee_name = tk.StringVar()
P2_current_date = datetime.now()  # 用於追蹤當前顯示的年月
panel2_tabledata = pd.DataFrame(columns=["日期", "上班1", "下班1", "上班2", "下班2", "上班3", "下班3"])
for i in range(1, 32):
    panel2_tabledata.loc[i] = [i, "", "", "", "", "", ""]

def focus_on_hidden_entry2(event=None):
    """將游標移動到卡號輸入框"""
    P2_sub_panel_hidden_entry1.focus_set()

def update_panel2_table():
    """更新 Panel2 的表格資料"""
    global P2_current_date
    manager = DatabaseManager()
    name = P2_employee_name.get()
    if not name:
        messagebox.showwarning("警告", "請先輸入員工卡號並查詢")
        return

    # 獲取指定年月的資料
    old_records = manager.fetch_records(name=name, month=P2_current_date.strftime("%Y-%m"))
    panel2_tabledata = pd.DataFrame(
        [[i, "", "", "", "", "", ""] for i in range(1, 32)],
        columns=["日期", "上班1", "下班1", "上班2", "下班2", "上班3", "下班3"]
    )
    for record in old_records:
        rec_id, date, rfid_id, am_in, am_out, pm_in, pm_out, ot_in, ot_out = record
        d = datetime.strptime(date, "%Y-%m-%d").day
        panel2_tabledata.loc[d - 1] = [d, am_in or "", am_out or "", pm_in or "", pm_out or "", ot_in or "", ot_out or ""]
    
    # 更新表格
    P2_sub_panel2_table1.insert_df(panel2_tabledata[:16])
    P2_sub_panel2_table2.insert_df(panel2_tabledata[16:32])
    manager.close()

def go_to_previous_month():
    """切換到上一個月"""
    global P2_current_date
    P2_current_date = P2_current_date.replace(day=1) - pd.Timedelta(days=1)
    P2_current_date = P2_current_date.replace(day=1)
    P2_label_date.config(text=P2_current_date.strftime("%Y-%m"))
    update_panel2_table()

def go_to_next_month():
    """切換到下一個月"""
    global P2_current_date
    P2_current_date = P2_current_date.replace(day=28) + pd.Timedelta(days=4)
    P2_current_date = P2_current_date.replace(day=1)
    P2_label_date.config(text=P2_current_date.strftime("%Y-%m"))
    update_panel2_table()

def BeepCard2(event=None):
    """處理 Panel2 的刷卡事件"""
    card_id = P2_sub_panel_hidden_entry1.get().strip()
    if not card_id:
        print("未讀取到卡號")
        P2_sub_panel_hidden_entry1.delete(0, tk.END)
        return

    emyployee = get_employee_by_rfid(card_id)
    if not emyployee:
        messagebox.showwarning("警告", "未找到對應的員工資料")
        P2_sub_panel_hidden_entry1.delete(0, tk.END)
        return

    emp_id, name, rfids, pic_path = emyployee
    P2_employee_name.set(name)
    update_panel2_table()
    P2_sub_panel_hidden_entry1.delete(0, tk.END)

# Panel2 子面板1: 員工資訊和月份切換
P2_sub_panel1 = tk.Frame(panel2, bg="lightblue")
P2_sub_panel1_label1 = tk.Label(P2_sub_panel1, text="員工:", font=P1_font2, bg='lightblue')
P2_sub_panel1_label2 = tk.Label(P2_sub_panel1, textvariable=P2_employee_name, bg='lightblue', font=P1_font2)
P2_sub_panel_hidden_entry1 = tk.Entry(P2_sub_panel1, font=P1_font2, width=0)
P2_sub_panel_hidden_entry1.place(x=-100, y=-100)
P2_sub_panel_hidden_entry1.bind("<Return>", BeepCard2)

# 左右切換按鈕和年月顯示
P2_button_prev = tk.Button(P2_sub_panel1, text="←", font=P1_font2, command=go_to_previous_month)
P2_label_date = tk.Label(P2_sub_panel1, text=P2_current_date.strftime("%Y-%m"), font=P1_font2, bg="lightblue")
P2_button_next = tk.Button(P2_sub_panel1, text="→", font=P1_font2, command=go_to_next_month)

# 排版
P2_sub_panel1_label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
P2_sub_panel1_label2.grid(row=0, column=1, padx=10, pady=10, sticky="w")
P2_button_prev.grid(row=0, column=2, padx=10, pady=10)
P2_label_date.grid(row=0, column=3, padx=10, pady=10)
P2_button_next.grid(row=0, column=4, padx=10, pady=10)

P2_sub_panel1.grid(row=0, column=0, sticky="w")

# Panel2 子面板2: 打卡紀錄表格
P2_sub_panel2 = tk.Frame(panel2, bg="lightblue")
P2_sub_panel2_table1 = create_table(P2_sub_panel2, data=panel2_tabledata[:16], table_widths=[60, 60, 60, 60, 60, 60, 60])
P2_sub_panel2_table2 = create_table(P2_sub_panel2, data=panel2_tabledata[16:32], table_widths=[60, 60, 60, 60, 60, 60, 60])

# 排版
P2_sub_panel2_table1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
P2_sub_panel2_table2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

P2_sub_panel2.grid(row=1, column=0, sticky="nsw")
#///////////////////////////////////////////////////////end of Panel2
#//////////////////////////////////////////////////////Panel3 其他
# Panel3 新增員工功能
global hidden_count #隱藏介面的計數器
hidden_count = 0
def toggle_sub_panel2(action):
    """根據按鈕操作顯示或隱藏 P3_sub_panel2"""
    global hidden_count
    if action == "+":
        hidden_count += 1
    elif action == "-":
        hidden_count -= 1

    # 限制計數器範圍
    hidden_count = max(0, min(hidden_count, 5))

    # 顯示或隱藏 P3_sub_panel2
    if hidden_count == 5:
        P3_sub_panel2.grid(row=1, column=0, sticky="nw")  # 顯示
    elif hidden_count == 0:
        P3_sub_panel2.grid_forget()  # 隱藏

def focus_on_entry3(event=None):
    """將游標移動到員工姓名輸入框"""
    P3_entry_name.focus_set()
def add_rfid_to_list():
    """將輸入的 RFID 添加到 ListView"""
    toggle_sub_panel2("+")  # 增加計數器
    rfid = P3_entry_rfid.get().strip()
    if rfid:
        P3_listbox.insert(tk.END, rfid)  # 添加到 ListView
        P3_entry_rfid.delete(0, tk.END)  # 清空輸入框


def remove_selected_rfid():
    """移除選中的 RFID"""
    toggle_sub_panel2("-")  # 減少計數器
    selected_indices = P3_listbox.curselection()
    for index in selected_indices[::-1]:  # 倒序刪除，避免索引錯誤
        P3_listbox.delete(index)

def add_employee_ui():
    """新增員工到資料庫"""
    employee_name = P3_entry_name.get().strip()
    rfids = [P3_listbox.get(i) for i in range(P3_listbox.size())]  # 獲取所有 RFID
    rfids_str = ",".join(rfids)  # 格式化為逗號分隔的字串

    if not employee_name or not rfids:
        print("員工姓名和 RFID 均為必填")
        messagebox.showwarning("警告", "員工姓名和 RFID 均為必填")
        return
    for rfid in rfids:
        if get_employee_by_rfid(rfid): #檢查是否有已經登記的rfid
            messagebox.showwarning("警告", f"RFID {rfid} 已經被登記，請檢查")
            return

    try:
        # 使用 employeeSql.py 中的 add_employee 函數
        from employeeSql import add_employee
        add_employee(name=employee_name, rfids=rfids_str)
        print(f"成功新增員工: {employee_name}")
        # 清空輸入框和 ListView
        P3_entry_name.delete(0, tk.END)
        P3_listbox.delete(0, tk.END)
        #跳一個提示messagebox
        messagebox.showinfo("成功", f"成功新增員工: {employee_name}")

    except Exception as e:
        print(f"新增員工時發生錯誤: {e}")
        messagebox.showerror("錯誤", f"新增員工時發生錯誤: {e}")

def modify_employee_attendance():
    """修改員工的打卡紀錄"""
    name = P3_entry_modify_name.get().strip()
    date = P3_entry_modify_date.get().strip()
    col = P3_combobox_modify_time.get()
    time = P3_entry_modify_time.get().strip()


    if not name or not date or not col or not time:
        messagebox.showwarning("警告", "所有欄位均為必填")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")  # 驗證日期格式
    except ValueError:
        messagebox.showwarning("警告", "日期格式應為 YYYY-MM-DD")
        return
    
    try:
        db = DatabaseManager()
        records = db.fetch_record_by_name_and_date(name, date)
        if records:
            record_id = records[0]
            col = col.replace("上班1", "am_in").replace("下班1", "am_out").replace("上班2", "pm_in").replace("下班2", "pm_out").replace("上班3", "ot_in").replace("下班3", "ot_out")
            db.update_record(record_id, col, time)
            db.close()
            messagebox.showinfo("成功", f"成功修改 {name} 的 {date} {col} 為 {time}")
        else:
            messagebox.showwarning("警告", f"未找到 {name} 在 {date} 的紀錄")
    except Exception as e:
        messagebox.showerror("錯誤", f"修改打卡紀錄時發生錯誤: {e}")



# Panel3 UI

P3_sub_panel1 = tk.Frame(panel3, bg="peach puff")
P3_label_name = tk.Label(P3_sub_panel1, text="員工姓名:", font=("Times New Roman", 16), bg="peach puff")
P3_entry_name = tk.Entry(P3_sub_panel1, font=("Times New Roman", 16), width=20)
P3_label_rfid = tk.Label(P3_sub_panel1, text="RFID卡號:", font=("Times New Roman", 16), bg="peach puff")
P3_entry_rfid = tk.Entry(P3_sub_panel1, font=("Times New Roman", 16), width=20)
P3_button_add_rfid = tk.Button(P3_sub_panel1, text="+", font=("Times New Roman", 16), width=3, command=add_rfid_to_list)
P3_button_remove_rfid = tk.Button(P3_sub_panel1, text="-", font=("Times New Roman", 16), width=3, command=remove_selected_rfid)
P3_listbox = tk.Listbox(P3_sub_panel1, font=("Times New Roman", 16), width=30, height=10)
P3_button_add_employee = tk.Button(P3_sub_panel1, text="新增員工", font=("Times New Roman", 16), command=add_employee_ui)
# 排版
P3_label_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")
P3_entry_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")
P3_label_rfid.grid(row=1, column=0, padx=10, pady=10, sticky="w")
P3_entry_rfid.grid(row=1, column=1, padx=10, pady=10, sticky="w")
P3_button_add_rfid.grid(row=1, column=2, padx=5, pady=10)
P3_button_remove_rfid.grid(row=1, column=3, padx=5, pady=10)
P3_listbox.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
P3_button_add_employee.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

# 修改員工打卡紀錄
P3_sub_panel2 = tk.Frame(panel3, bg="peach puff")
# Panel3 修改打卡紀錄的 UI
P3_label_modify_name = tk.Label(P3_sub_panel2, text="員工姓名:", font=("Times New Roman", 16), bg="peach puff")
P3_entry_modify_name = tk.Entry(P3_sub_panel2, font=("Times New Roman", 16), width=20)

P3_label_modify_date = tk.Label(P3_sub_panel2, text="日期 (YYYY-MM-DD):", font=("Times New Roman", 16), bg="peach puff")
P3_entry_modify_date = tk.Entry(P3_sub_panel2, font=("Times New Roman", 16), width=20)

P3_label_modify_time = tk.Label(P3_sub_panel2, text="時段:", font=("Times New Roman", 16), bg="peach puff")
P3_combobox_modify_time = tk.ttk.Combobox(P3_sub_panel2, font=("Times New Roman", 16), width=18, state="readonly")
P3_combobox_modify_time['values'] = ["上班1", "下班1", "上班2", "下班2", "上班3", "下班3"]

P3_label_modify_time_value = tk.Label(P3_sub_panel2, text="時間 (HH:MM):", font=("Times New Roman", 16), bg="peach puff")
P3_entry_modify_time = tk.Entry(P3_sub_panel2, font=("Times New Roman", 16), width=20)

P3_button_modify_attendance = tk.Button(P3_sub_panel2, text="修改打卡紀錄", font=("Times New Roman", 16), command=modify_employee_attendance)

# 排版P3_sub_panel2
P3_label_modify_name.grid(row=4, column=0, padx=10, pady=10, sticky="w")
P3_entry_modify_name.grid(row=4, column=1, padx=10, pady=10, sticky="w")

P3_label_modify_date.grid(row=5, column=0, padx=10, pady=10, sticky="w")
P3_entry_modify_date.grid(row=5, column=1, padx=10, pady=10, sticky="w")

P3_label_modify_time.grid(row=6, column=0, padx=10, pady=10, sticky="w")
P3_combobox_modify_time.grid(row=6, column=1, padx=10, pady=10, sticky="w")

P3_label_modify_time_value.grid(row=7, column=0, padx=10, pady=10, sticky="w")
P3_entry_modify_time.grid(row=7, column=1, padx=10, pady=10, sticky="w")

P3_button_modify_attendance.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

P3_current_date = datetime.now()  # 用於追蹤當前顯示的年月
def P3_go_to_previous_month():
    """切換到上一個月"""
    global P3_current_date
    P3_current_date = P3_current_date.replace(day=1) - pd.Timedelta(days=1)
    P3_current_date = P3_current_date.replace(day=1)
    P3_label_date.config(text=P3_current_date.strftime("%Y-%m"))


def P3_go_to_next_month():
    """切換到下一個月"""
    global P3_current_date
    P3_current_date = P3_current_date.replace(day=28) + pd.Timedelta(days=4)
    P3_current_date = P3_current_date.replace(day=1)
    P3_label_date.config(text=P3_current_date.strftime("%Y-%m"))

def export_to_excel():
    """匯出指定月份的所有員工打卡紀錄到 Excel (全部在同一張表)"""
    month = P3_label_date.cget("text")  # 例如 "2025-08"
    manager = DatabaseManager()
    records = manager.fetch_all_months_records(month)
    manager.close()

    if not records:
        messagebox.showwarning("警告", f"{month} 沒有任何資料")
        return

    # 整理成 DataFrame
    df = pd.DataFrame(records, columns=[
        "ID", "日期", "姓名", "上班1", "下班1", "上班2", "下班2", "上班3", "下班3"
    ])

    # 移除 ID 欄位（非必要）
    df = df.drop(columns=["ID"])

    # 依照「姓名、日期」排序
    df = df.sort_values(by=["姓名", "日期"])

    # 選擇儲存位置
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")],
        initialfile=f"出勤紀錄_{month}.xlsx"
    )

    if not file_path:
        return  # 使用者取消

    # 直接輸出成單一 Excel 工作表
    df.to_excel(file_path, sheet_name="出勤紀錄", index=False)

    messagebox.showinfo("成功", f"成功匯出 {month} 的出勤紀錄\n檔案位置:\n{file_path}")

#選擇月份會出資料
P3_sub_panel3 = tk.Frame(panel3, bg="peach puff")
# 左右切換按鈕和年月顯示
P3_button_prev = tk.Button(P3_sub_panel3, text="←", font=P1_font2, command=P3_go_to_previous_month)
P3_label_date = tk.Label(P3_sub_panel3, text=P2_current_date.strftime("%Y-%m"), font=P1_font2, bg="peach puff")
P3_button_next = tk.Button(P3_sub_panel3, text="→", font=P1_font2, command=P3_go_to_next_month)
P3_export_button = tk.Button(P3_sub_panel3, text="匯出Excel", font=P1_font2,command=export_to_excel)

#P3_sub_panel3的排版
P3_button_prev.grid(row=0, column=0, padx=10, pady=10)
P3_label_date.grid(row=0, column=1, padx=10, pady=10)
P3_button_next.grid(row=0, column=2, padx=10, pady=10)
P3_export_button.grid(row=0, column=3, padx=10, pady=10)


P3_sub_panel1.grid(row=0, column=0, sticky="nw")
P3_sub_panel3.grid(row=0, column=1, sticky="nw")
# P3_sub_panel2.grid(row=1, column=0, sticky="nw")

#///////////////////////////////////////////////end of Panel3 其他

# 創建一個列表來存儲所有Panel，按照顯示的順序排列
panels = [panel1, panel2, panel3]

# 設置panel的行和列，使其填充整個視窗
for panel in panels:
    panel.grid(row=1, column=0, sticky="nsew")

# 設置button_panel的行和列，使其填充整個視窗
button_panel.grid(row=0, column=0, sticky="nsew")

# 使用rowconfigure和columnconfigure來設置權重
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)


# 預設顯示第一個Panel
show_panel(panel1)
# 啟動主迴圈
root.mainloop()
