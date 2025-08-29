import tkinter as tk
from tkinter import ttk


class AttendanceTable(tk.Frame):
    def __init__(self, master=None, rows=15, **kwargs):
        super().__init__(master, **kwargs)

        # --- 先做雙層表頭 ---
        header_frame = tk.Frame(self)
        header_frame.pack(fill="x")

        # 第一列
        tk.Label(header_frame, text="日期", borderwidth=1, relief="solid", width=8, height=2).grid(row=0, column=0, rowspan=2)

        tk.Label(header_frame, text="上午", borderwidth=1, relief="solid", width=16).grid(row=0, column=1, columnspan=2)
        tk.Label(header_frame, text="下午", borderwidth=1, relief="solid", width=16).grid(row=0, column=3, columnspan=2)
        tk.Label(header_frame, text="加班", borderwidth=1, relief="solid", width=16).grid(row=0, column=5, columnspan=2)

        # 第二列
        tk.Label(header_frame, text="上班", borderwidth=1, relief="solid", width=8).grid(row=1, column=1)
        tk.Label(header_frame, text="下班", borderwidth=1, relief="solid", width=8).grid(row=1, column=2)
        tk.Label(header_frame, text="上班", borderwidth=1, relief="solid", width=8).grid(row=1, column=3)
        tk.Label(header_frame, text="下班", borderwidth=1, relief="solid", width=8).grid(row=1, column=4)
        tk.Label(header_frame, text="上班", borderwidth=1, relief="solid", width=8).grid(row=1, column=5)
        tk.Label(header_frame, text="下班", borderwidth=1, relief="solid", width=8).grid(row=1, column=6)

        # --- 真正的表格 (Treeview) ---
        self.tree = ttk.Treeview(self, columns=("date", "am_in", "am_out", "pm_in", "pm_out", "ot_in", "ot_out"),
                                 show="headings", height=rows)

        # 這裡不顯示表頭，因為我們用自製的
        self.tree.pack(fill="both", expand=True)

        # 插入日期行
        for i in range(1, rows + 1):
            self.tree.insert("", "end", values=(i, "", "", "", "", "", ""))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("考勤表")

    table = AttendanceTable(root, rows=15)
    table.pack(fill="both", expand=True)

    root.mainloop()
