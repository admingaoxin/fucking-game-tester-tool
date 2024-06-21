import tkinter as tk
from tkinter import ttk
import pyperclip
import os
from datetime import datetime

# 定义一个用于存储剪贴板内容的文件路径
clipboard_file_path = "clipboard_contents.txt"

# 从文件中加载剪贴板内容到列表
def load_clipboard_contents():
    if os.path.exists(clipboard_file_path):
        with open(clipboard_file_path, "r", encoding="utf-8") as file:
            return file.read().split("\n----------------------\n")
    else:
        return []

# 将列表内容保存到文件
def save_clipboard_contents(contents):
    with open(clipboard_file_path, "w", encoding="utf-8") as file:
        file.write("\n----------------------\n".join(contents))

# 定义函数，用于更新列表框的内容，将新的剪贴板内容添加到列表中。
def update_listbox():
    global last_item  # 使用全局变量来存储上一次的剪贴板内容
    new_item = pyperclip.paste()  # 获取当前剪贴板的内容
    if new_item != last_item:  # 只有当内容发生变化时才处理
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间戳
        item_with_timestamp = f"{timestamp}: {new_item}"  # 将时间戳和内容组合
        X.append(item_with_timestamp)
        listbox.insert(tk.END, item_with_timestamp)  # 在列表框末尾添加新项目
        listbox.insert(tk.END, "----------------------")  # 添加分隔线
        listbox.yview(tk.END)  # 自动滚动到列表框的底部
        save_clipboard_contents(X)  # 保存更新后的内容到文件
        last_item = new_item  # 更新上一次的剪贴板内容
    root.after(1000, update_listbox)  # 每1000毫秒（1秒）调用一次此函数，不断更新

# 定义函数，用于处理列表框中元素的双击事件，将选中的内容复制到剪贴板。
def copy_to_clipboard(event):
    selected_item = listbox.get(listbox.curselection())  # 获取当前选中的列表项
    if selected_item:
        pyperclip.copy(selected_item.split(": ", 1)[1])  # 将选中的内容（去除时间戳）复制到剪贴板

# 创建主窗口
root = tk.Tk()
root.title("ClipboardManager")  # 设置窗口标题
root.geometry("500x500")  # 设置窗口大小
root.configure(bg="#f0f0f0")  # 设置窗口背景颜色

# 创建一个框架组件，用于放置其他界面元素
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=10, pady=10)  # 放置框架并设置边距

# 在框架内创建一个标签，显示文本提示
label = tk.Label(frame, text="Clipboard Contents:", bg="#f0f0f0")
label.grid(row=0, column=0)  # 使用grid布局管理器放置标签

# 创建一个滚动条
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # 放置滚动条在窗口的右侧，填充Y方向

# 创建一个列表框，用于显示剪贴板的内容
listbox = tk.Listbox(root, width=150, height=150, yscrollcommand=scrollbar.set)
listbox.pack(pady=10)  # 放置列表框并设置垂直边距

scrollbar.config(command=listbox.yview)  # 设置滚动条控制列表框的垂直滚动

# 加载剪贴板历史记录到列表
X = load_clipboard_contents()
last_item = ""  # 初始化上一次剪贴板内容为空
if X:
    last_item = X[-1].split(": ", 1)[1]  # 获取最后一项内容，忽略时间戳
for item in X:
    listbox.insert(tk.END, item)
    listbox.insert(tk.END, "----------------------")

# 调用函数，开始更新列表框内容
update_listbox()

# 绑定双击左键事件到copy_to_clipboard函数，实现双击复制功能
listbox.bind("<Double-Button-1>", copy_to_clipboard)

# 运行主事件循环，等待用户交互
root.mainloop()