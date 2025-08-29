import tkinter as tk
from tkinter import Label
import time

class DigitalClock(tk.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        """
        初始化數字時鐘小部件
        :param parent: 父容器 (例如 tk.Frame 或 tk.Tk)
        """
        super().__init__(parent, *args, **kwargs)
        self.configure(bg="lightyellow")  # 設置背景顏色
        
        # 日期標籤
        self.date_label = Label(self, font=("Helvetica", 50), bg="lightyellow", fg="black")
        self.date_label.pack(pady=10)
        
        # 時間標籤
        self.time_label = Label(self, font=("Helvetica", 100, "bold"), bg="lightyellow", fg="black")
        self.time_label.pack(pady=10)

        #星期幾標籤
        self.weekday_label = Label(self, font=("Helvetica", 40), bg="lightyellow", fg="black")
        self.weekday_label.pack(pady=5)
        
        # 啟動時鐘更新
        self.update_clock()
    
    #計算星期幾
    def calculate_weekday(self, year, month, day):
        """計算給定日期是星期幾"""
        if month < 3:
            month += 12
            year -= 1
        k = year % 100
        j = year // 100
        f = day + (13 * (month + 1)) // 5 + k + (k // 4) + (j // 4) - (2 * j)
        weekday = f % 7
        return ["星期六", "星期日", "星期一", "星期二", "星期三", "星期四", "星期五"][weekday]
        

    def update_clock(self):
        """更新時鐘顯示"""
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y/%m/%d")
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        year, month, day = map(int, current_date.split('/'))
        calculate_weekday = self.calculate_weekday(year, month, day)
        self.weekday_label.config(text=calculate_weekday)
        self.after(1000, self.update_clock)  # 每秒更新一次

# 測試程式
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Digital Clock Test")
    root.geometry("300x150")
    
    clock = DigitalClock(root)
    clock.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()