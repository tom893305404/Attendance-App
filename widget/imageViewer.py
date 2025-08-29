import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageViewer(tk.Frame):
    def __init__(self, master=None, width=300, height=300, **kwargs):
        super().__init__(master, **kwargs)
        self.width = width
        self.height = height
        self.image_label = tk.Label(self, bg="black")
        self.image_label.pack(fill="both", expand=True)

        self.image = None  # 保存原始圖片
        self.tk_image = None  # Tkinter 版本的圖片

    def show_image(self, path):
        """顯示指定路徑的圖片，並自動縮放"""
        self.image = Image.open(path)
        self._update_display()

    def _update_display(self):
        if self.image is None:
            return
        img_resized = self.image.copy()
        img_resized.thumbnail((self.width, self.height))
        self.tk_image = ImageTk.PhotoImage(img_resized)
        self.image_label.config(image=self.tk_image)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("圖片顯示 Widget")

    viewer = ImageViewer(root, width=400, height=400)
    viewer.pack(fill="both", expand=True)

    # 測試：選擇一張圖片
    def load_image():
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif *.bmp")]
        )
        if file_path:
            viewer.show_image(file_path)

    btn = tk.Button(root, text="選擇圖片", command=load_image)
    btn.pack()

    root.mainloop()
