
import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from barcode import EAN13
from barcode.writer import ImageWriter
from PIL import ImageTk, Image
class BarcodeGeneratorApp:
   def __init__(self, master):
       self.master = master
       master.title("二维码 & 条形码生成器")
       # 初始化图像变量
       self.qr_image = None
       self.bar_image = None
       # 二维码部分
       qr_frame = tk.Frame(master, padx=20, pady=20)
       qr_frame.pack(side=tk.LEFT)
       self.qr_label = tk.Label(qr_frame)
       self.qr_label.pack()
       self.qr_entry = tk.Entry(qr_frame)
       self.qr_entry.pack(pady=(0, 10))
       qr_gen_button = tk.Button(qr_frame, text="生成二维码", command=self.generate_qr_code)
       qr_gen_button.pack()
       qr_save_button = tk.Button(qr_frame, text="保存二维码", command=self.save_qr)
       qr_save_button.pack()
       # 条形码部分
       bar_frame = tk.Frame(master, padx=20, pady=20)
       bar_frame.pack(side=tk.RIGHT)
       self.bar_label = tk.Label(bar_frame)
       self.bar_label.pack()
       self.bar_entry = tk.Entry(bar_frame)
       self.bar_entry.pack(pady=(0, 10))
       bar_gen_button = tk.Button(bar_frame, text="生成条形码", command=self.generate_bar_code)
       bar_gen_button.pack()
       bar_save_button = tk.Button(bar_frame, text="保存条形码", command=self.save_bar)
       bar_save_button.pack()
   def generate_qr_code(self):
       data = self.qr_entry.get()
       if data:
           img = qrcode.make(data)
           img.save("qr_code.png")
           self.qr_image = Image.open("qr_code.png")
           self.qr_image.thumbnail((200, 200))
           qr_photo = ImageTk.PhotoImage(self.qr_image)
           self.qr_label.config(image=qr_photo)
           self.qr_label.image = qr_photo
       else:
           messagebox.showwarning("警告", "请输入内容以生成二维码！")
   def generate_bar_code(self):
       data = self.bar_entry.get()
       if data.isdigit() and (len(data) == 12 or len(data) == 13):
           ean = EAN13(data, writer=ImageWriter())
           filename = ean.save("bar_code.png")  # 确保保存为png文件
           self.bar_image = Image.open(filename)
           self.bar_image.thumbnail((200, 100))
           bar_photo = ImageTk.PhotoImage(self.bar_image)
           self.bar_label.config(image=bar_photo)
           self.bar_label.image = bar_photo
       else:
           messagebox.showwarning("警告", "请输入有效的12或13位数字以生成条形码！")
   def save_qr(self):
       if self.qr_image:
           file_path = filedialog.asksaveasfilename(defaultextension=".png")
           if file_path:
               self.qr_image.save(file_path)
               messagebox.showinfo("成功", "二维码已保存！")
   def save_bar(self):
       if self.bar_image:
           file_path = filedialog.asksaveasfilename(defaultextension=".png")
           if file_path:
               self.bar_image.save(file_path)
               messagebox.showinfo("成功", "条形码已保存！")
if __name__ == "__main__":
   root = tk.Tk()
   app = BarcodeGeneratorApp(root)
   root.mainloop()