#导入tkinter库，用于创建GUI应用程序，ttk是tkinter的扩展模块，用于提供更现代的界面元素。
import tkinter as tk
from tkinter import ttk
#导入pyperclip库，可以用来复制和粘贴剪贴板内容。
import pyperclip


#定义函数，用于更新列表框的内容，将新的剪贴板内容添加到列表中。
def update_listbox():
    new_item = pyperclip.paste ()  # 获取当前剪贴板的内容
    if new_item not in X:  # 如果内容不在我们的列表中，则添加它
        X.append (new_item)
        listbox.insert (tk.END, new_item)  # 在列表框末尾添加新项目
        listbox.insert (tk.END, "----------------------")  #添加分隔线
        listbox.yview (tk.END)  # 自动滚动到列表框的底部
    root.after (1000, update_listbox)  # 每1000毫秒（1秒）调用一次此函数，不断更新


#定义函数，用于处理列表框中元素的双击事件，将选中的内容复制到剪贴板。
def copy_to_clipboard(event):
    selected_item = listbox.get (listbox.curselection ())  #获取当前选中的列表项
    if selected_item:
        pyperclip.copy (selected_item)  # 将选中的内容复制到剪贴板


#创建一个空列表，用于存储剪贴板内容。
X = []
# 创建主窗口
root = tk.Tk ()
root.title ("ClipboardManager")  # 设置窗口标题
root.geometry ("500x500")  # 设置窗口大小
root.configure (bg="#f0f0f0")  # 设置窗口背景颜色
#创建一个框架组件，用于放置其他界面元素
frame = tk.Frame (root, bg="#f0f0f0")
frame.pack (padx=10, pady=10)  # 放置框架并设置边距
# #在框架内创建一个标签，显示文本提示
label = tk.Label (frame, text="Clipboard Contents:", bg="#f0f0f0")
label.grid (row=0, column=0)  # 使用grid布局管理器放置标签
# 创建一个滚动条
scrollbar = tk.Scrollbar (root)
scrollbar.pack (side=tk.RIGHT,
                fill=tk.Y)  # 放置滚动条在窗口的右侧，填充Y方向
#创建一个列表框，用于显示剪贴板的内容
listbox = tk.Listbox (root, width=150, height=150, yscrollcommand=scrollbar.set)
listbox.pack (pady=10)  # 放置列表框并设置垂直边距
scrollbar.config (command=listbox.yview)  # 设置滚动条控制列表框的垂直滚动
# 调用函数，开始更新列表框内容
update_listbox ()
#绑定双击左键事件到copy_to_clipboard函数，实现双击复制功能
listbox.bind ("<Double-Button-1>",
              copy_to_clipboard)
# 运行主事件循环，等待用户交互
root.mainloop()
