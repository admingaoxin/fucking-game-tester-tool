import tkinter as tk
from tkinter import filedialog, simpledialog, ttk, messagebox
from PIL import Image, ImageTk, ImageGrab, ImageEnhance
import cv2
import numpy as np
import pyautogui
import time
import random
import threading
import logging
import os
import json
import time

class ImageRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图像识别与点击")
        self.image_list = []  # 存储 (图像路径, 步骤名称, 相似度, 键盘输入)
        self.screenshot_area = None  # 用于存储截图区域
        self.rect = None  # 用于存储 Canvas 上的矩形
        self.start_x = None
        self.start_y = None
        self.canvas = None
        self.running = False  # 控制脚本是否在运行
        self.thread = None  # 用于保存线程
        self.hotkey = '<F1>'  # 默认热键
        self.similarity_threshold = 0.8  # 默认相似度阈值
        self.delay_time = 0.1  # 默认延迟时间
        self.loop_count = 1  # 默认循环次数
        self.init_ui()
        self.init_logging()
        self.load_config()

    def init_ui(self):
        # 主框架布局
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧布局：上传图片、截图、运行脚本按钮
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # 批量上传图片按钮
        self.batch_upload_button = tk.Button(self.left_frame, text="上传图像", command=self.batch_upload_images)
        self.batch_upload_button.pack(pady=5)

        # 框选截图按钮（微信风格截图）
        self.screenshot_button = tk.Button(self.left_frame, text="框选截图", command=self.prepare_capture_screenshot)
        self.screenshot_button.pack(pady=5)

        # 删除选中图片按钮
        self.delete_button = tk.Button(self.left_frame, text="删除图片", command=self.delete_selected_image)
        self.delete_button.pack(pady=5)

        # 运行/停止脚本按钮
        self.toggle_run_button = tk.Button(self.left_frame, text="开始运行", command=self.toggle_script)
        self.toggle_run_button.pack(pady=5)

        # 保存配置按钮
        self.save_config_button = tk.Button(self.left_frame, text="保存配置", command=self.save_config)
        self.save_config_button.pack(pady=5)

        # 设置热键按钮
        # self.set_hotkey_button = tk.Button(self.left_frame, text="设置热键", command=self.set_hotkey)
        # self.set_hotkey_button.pack(pady=5)

        # 手动加载配置按钮
        self.load_config_button = tk.Button(self.left_frame, text="加载配置", command=self.load_config_manually)
        self.load_config_button.pack(pady=5)

        # 循环次数输入框
        self.loop_count_label = tk.Label(self.left_frame, text="循环次数:")
        self.loop_count_label.pack(pady=5)
        self.loop_count_entry = tk.Entry(self.left_frame)
        self.loop_count_entry.insert(0, str(self.loop_count))
        self.loop_count_entry.pack(pady=5)

        # 右侧布局：图像列表显示
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 使用 Treeview 来显示图片和等待时间
        self.tree = ttk.Treeview(self.right_frame, columns=("图片", "步骤名称", "相似度", "键盘输入"), show='headings')
        self.tree.heading("图片", text="图片")
        self.tree.heading("步骤名称", text="步骤名称")
        self.tree.heading("相似度", text="相似度")
        self.tree.heading("键盘输入", text="键盘输入")
        self.tree.column("图片", width=200)  # 调整图片列宽度
        self.tree.column("步骤名称", width=100)  # 调整步骤名称列宽度
        self.tree.column("相似度", width=100)  # 调整相似度列宽度
        self.tree.column("键盘输入", width=100)  # 调整键盘输入列宽度
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.tree.bind('<Double-1>', self.edit_image_name)  # 左键双击编辑步骤名称
        self.tree.bind('<Double-3>', self.edit_similarity_threshold)  # 右键双击编辑相似度
        self.tree.bind('<Double-2>', self.edit_keyboard_input)  # 中键双击编辑键盘输入
        self.tree.image_refs = []  # 保持对图像的引用，防止被垃圾回收

        # 绑定热键
        self.root.bind(self.hotkey, self.toggle_script)

    def init_logging(self):
        logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def batch_upload_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.png")])
        if file_paths:
            for file_path in file_paths:
                self.image_list.append((file_path, os.path.basename(file_path), 0.8, ""))
            self.update_image_listbox()

    def prepare_capture_screenshot(self):
        # 隐藏主窗口
        self.root.withdraw()
        time.sleep(0.5)

        # 创建一个全屏幕的透明窗口，用于捕获框选区域
        self.top = tk.Toplevel(self.root)
        self.top.attributes('-fullscreen', True)
        self.top.attributes('-alpha', 0.3)  # 透明度设置

        # 在窗口上创建 Canvas
        self.canvas = tk.Canvas(self.top, cursor="cross", bg='grey')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 绑定鼠标事件
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        # 记录起始点坐标
        self.start_x = event.x
        self.start_y = event.y
        # 如果有之前的矩形，删除
        if self.rect:
            self.canvas.delete(self.rect)
        # 创建新的矩形框
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red',
                                                 width=2)

    def on_mouse_drag(self, event):
        # 动态更新矩形框的大小
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        # 记录终点坐标
        end_x = event.x
        end_y = event.y

        # 获取截图区域
        bbox = (min(self.start_x, end_x), min(self.start_y, end_y), max(self.start_x, end_x), max(self.start_y, end_y))

        # 使用规则 "JT******.png" 命名截图文件
        timestamp = f"JT{random.randint(100000, 999999)}.png"
        screenshot_path = timestamp

        # 截图指定区域
        screenshot = ImageGrab.grab(bbox)
        screenshot.save(screenshot_path)

        # 更新图像列表
        self.image_list.append((screenshot_path, timestamp, 0.8, ""))
        self.update_image_listbox()

        # 关闭全屏透明窗口
        self.top.destroy()
        self.root.deiconify()

    def update_image_listbox(self):
        # 清空旧的列表项
        for row in self.tree.get_children():
            self.tree.delete(row)

        # 插入新项，显示图片路径和等待时间
        for img_path, img_name, similarity_threshold, keyboard_input in self.image_list:
            # 加载图像并创建缩略图
            image = Image.open(img_path)
            image.thumbnail((50, 50))  # 调整缩略图大小
            photo = ImageTk.PhotoImage(image)

            # 插入图像和等待时间
            self.tree.insert("", tk.END, values=(img_path, img_name, similarity_threshold, keyboard_input), image=photo)
            self.tree.image_refs.append(photo)  # 保持对图像的引用，防止被垃圾回收

    def edit_image_name(self, event):
        # 左键双击列表项，编辑步骤名称
        selected_item = self.tree.selection()[0]
        selected_index = self.tree.index(selected_item)
        selected_image = self.image_list[selected_index]

        # 弹出对话框修改步骤名称
        new_image_name = simpledialog.askstring("修改步骤名称", "请输入新的步骤名称：", initialvalue=selected_image[1])
        if new_image_name is not None:
            self.image_list[selected_index] = (selected_image[0], new_image_name, selected_image[2], selected_image[3])
            self.update_image_listbox()

    def edit_similarity_threshold(self, event):
        # 右键双击列表项，编辑相似度
        selected_item = self.tree.selection()[0]
        selected_index = self.tree.index(selected_item)
        selected_image = self.image_list[selected_index]

        # 弹出对话框修改相似度
        new_similarity_threshold = simpledialog.askfloat("修改相似度", "请输入新的相似度（0.1 - 1.0）：",
                                                         initialvalue=selected_image[2], minvalue=0.1, maxvalue=1.0)
        if new_similarity_threshold is not None:
            self.image_list[selected_index] = (
            selected_image[0], selected_image[1], new_similarity_threshold, selected_image[3])
            self.update_image_listbox()

    def edit_keyboard_input(self, event):
        # 中键双击列表项，编辑键盘输入
        selected_item = self.tree.selection()[0]
        selected_index = self.tree.index(selected_item)
        selected_image = self.image_list[selected_index]

        # 弹出对话框修改键盘输入
        new_keyboard_input = simpledialog.askstring("修改键盘输入", "请输入新的键盘输入：",
                                                    initialvalue=selected_image[3])
        if new_keyboard_input is not None:
            self.image_list[selected_index] = (
            selected_image[0], selected_image[1], selected_image[2], new_keyboard_input)
            self.update_image_listbox()

    def delete_selected_image(self):
        # 删除选中的图片
        selected_item = self.tree.selection()
        if selected_item:
            selected_index = self.tree.index(selected_item[0])
            del self.image_list[selected_index]
            self.update_image_listbox()

    def toggle_script(self, event=None):
        if not self.running:
            self.start_script_thread()
            self.toggle_run_button.config(text="停止运行")
        else:
            self.stop_script()
            self.toggle_run_button.config(text="开始运行")

    def start_script_thread(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_script, daemon=True)
            self.thread.start()

    def run_script(self):
        # 获取循环次数
        self.loop_count = int(self.loop_count_entry.get())
        current_loop = 0

        # 按顺序执行所有图片的模板匹配并点击
        while self.running and current_loop < self.loop_count:
            for img_path, img_name, similarity_threshold, keyboard_input in self.image_list:
                if not self.running:
                    break
                while self.running:
                    if self.match_and_click(img_path, similarity_threshold):
                        if keyboard_input:
                            pyautogui.write(keyboard_input)
                        break
                    time.sleep(self.delay_time)  # 等待延迟时间后重试
            current_loop += 1

    def stop_script(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()  # 等待线程结束
        print("脚本已停止")
        logging.info("脚本已停止")

    def match_and_click(self, template_path, similarity_threshold):
        # 截取当前屏幕
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # 读取模板图像
        template = cv2.imread(template_path, 0)
        if template is None:
            print(f"无法读取图像: {template_path}")
            logging.error(f"无法读取图像: {template_path}")
            return False

        # 转换截图为灰度图像
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # 进行模板匹配
        result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= similarity_threshold)

        # 如果找到了相似区域，模拟点击
        found = False
        for pt in zip(*loc[::-1]):
            # 计算点击点的位置
            click_x = pt[0] + template.shape[1] // 2
            click_y = pt[1] + template.shape[0] // 2
            # 模拟点击
            pyautogui.click(click_x, click_y)
            found = True
            break  # 点击一次后跳出

        if not found:
            print(f"未找到匹配区域: {template_path}")
            logging.warning(f"未找到匹配区域: {template_path}")
            return False

        return True

    def set_hotkey(self):
        # 设置热键
        new_hotkey = simpledialog.askstring("设置热键", "请输入新的热键（例如：<F1>）：", initialvalue=self.hotkey)
        if new_hotkey is not None:
            self.hotkey = new_hotkey
            self.root.bind(self.hotkey, self.toggle_script)
            print(f"热键已设置为: {self.hotkey}")
            logging.info(f"热键已设置为: {self.hotkey}")

    def save_config(self):
        config = {
            "image_list": self.image_list,
            "hotkey": self.hotkey,
            "screenshot_area": self.screenshot_area,
            "similarity_threshold": self.similarity_threshold,
            "delay_time": self.delay_time,
            "loop_count": self.loop_count
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)
        print("配置已保存")
        logging.info("配置已保存")

    def load_config(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.image_list = config.get("image_list", [])
                self.hotkey = config.get("hotkey", '<F1>')
                self.screenshot_area = config.get("screenshot_area", None)
                self.similarity_threshold = config.get("similarity_threshold", 0.8)
                self.delay_time = config.get("delay_time", 0.1)
                self.loop_count = config.get("loop_count", 1)
                self.loop_count_entry.delete(0, tk.END)
                self.loop_count_entry.insert(0, str(self.loop_count))
                self.root.bind(self.hotkey, self.toggle_script)
                self.update_image_listbox()
            print("配置已加载")
            logging.info("配置已加载")

    def load_config_manually(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                config = json.load(f)
                self.image_list = config.get("image_list", [])
                self.hotkey = config.get("hotkey", '<F1>')
                self.screenshot_area = config.get("screenshot_area", None)
                self.similarity_threshold = config.get("similarity_threshold", 0.8)
                self.delay_time = config.get("delay_time", 0.1)
                self.loop_count = config.get("loop_count", 1)
                self.loop_count_entry.delete(0, tk.END)
                self.loop_count_entry.insert(0, str(self.loop_count))
                self.root.bind(self.hotkey, self.toggle_script)
                self.update_image_listbox()
            print("配置已加载")
            logging.info("配置已加载")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRecognitionApp(root)
    root.mainloop()