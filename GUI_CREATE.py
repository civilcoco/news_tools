import tkinter as tk
import cv2
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
from Game import SlidePuzzleGame
# 设置计时器
import time

# import subprocess
# import os
# import platform

class NewsGUI:
    def __init__(self, scraper):
        self.bg_image_path = 'img/bkg.png'
        self.btn_image_path = 'img/主背景.png'
        self.image_links = []
        self.current_image_index = 0
        self.scraper = scraper
        self.min_length = 4  # 默认4为下限
        self.top_n = 10  # 默认展示10个热门话题
        self.end_video_path = "vedio/结束动画.mp4"  # 添加你的视频文件路径
        self.start_video_path = "vedio/myop.mp4"  # 添加你的视频文件路径
        self.start_time = time.time()  # 记录窗口启动时间

    def create_gui(self):
        self.root = tk.Tk()  # 注意这里我们使用 self.root 替代 root
        self.setMain_bkg()
        self.root.title("新闻每一天")

        self.top_n_label = tk.Label(self.root, text="设置热点新闻数量（默认10）：", font=("Arial", 14),bg="lightgoldenrod")
        self.top_n_label.grid(row=6, column=0, pady=10, padx=10, sticky="w")

        self.top_n_entry = tk.Entry(self.root, font=("Arial", 12),bg="lightgray")
        self.top_n_entry.grid(row=7, column=0, padx=10, sticky="we")

        set_top_n_button = tk.Button(self.root, text="设定热点数量", command=self.set_top_n, font=("Arial", 12),bg="lightblue")
        set_top_n_button.grid(row=8, column=0, pady=10, padx=10, sticky="we")

        label = tk.Label(self.root, text="输入关键词以搜索", font=("Arial", 14),bg="lightgoldenrod")
        label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.entry = tk.Entry(self.root, font=("Arial", 12),bg="lightgray")
        self.entry.grid(row=1, column=0, padx=10, sticky="we")

        button_frame = tk.LabelFrame(self.root, text="工具栏", font=("Arial", 12),bg="lightgoldenrod")
        button_frame.grid(row=2, column=0, pady=10, padx=10, sticky="we")

        hot_topic_button = tk.Button(button_frame, text="热点新闻展示", command=self.display_hot_topics,
                                     font=("Arial", 12),bg="lightblue")
        hot_topic_button.pack(side="left", padx=10)

        search_button = tk.Button(button_frame, text="搜索新闻标题", command=self.display_search_results,
                                  font=("Arial", 12),bg="lightblue")
        search_button.pack(side="left", padx=10)

        self.min_length_label = tk.Label(self.root, text="设置关键词下限字数（默认4）：", font=("Arial", 14),bg="lightgoldenrod")
        self.min_length_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

        self.min_length_entry = tk.Entry(self.root, font=("Arial", 12),bg="lightgray")
        self.min_length_entry.grid(row=4, column=0, padx=10, sticky="we")

        set_min_length_button = tk.Button(self.root, text="设定字数", command=self.set_min_length, font=("Arial", 12),bg="lightblue")
        set_min_length_button.grid(row=5, column=0, pady=10, padx=10, sticky="we")

        self.result = tk.Text(self.root, font=("Arial", 12),bg="lightgray")
        self.result.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")
        # # 配置链接样式
        # self.result.tag_configure("hyperlink", foreground="blue", underline=True)
        # # 配置链接点击事件
        # self.result.tag_bind("hyperlink", "<Button-1>", self.open_hyperlink)
        # 添加滚动条
        scrollbar = tk.Scrollbar(self.root, command=self.result.yview)
        scrollbar.grid(row=9, column=1, sticky="ns")
        self.result.config(yscrollcommand=scrollbar.set)
        # 查看链接中的图片
        image_button = tk.Button(button_frame, text="查看链接中的图片", command=self.open_image_window,
                                 font=("Arial", 12),bg="lightblue")
        image_button.pack(side="left", padx=10)
        # 益智小游戏
        game_button = tk.Button(button_frame, text="益智小游戏", command=self.open_game, font=("Arial", 12),bg="lightblue")
        game_button.pack(side="left", padx=10,)
        # 添加结束按钮
        end_button = tk.Button(button_frame, text="结束", command=self.end_program, font=("Arial", 12),bg="lightblue")
        end_button.pack(side="left", padx=10)

        # 让 Text widget 在窗口调整大小时自动扩展
        self.root.grid_rowconfigure(9, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.start_program()
        self.root.mainloop()


    def setMain_bkg(self):
        # 加载背景图片
        bg_image = Image.open(self.bg_image_path)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # 让图片铺满整个窗口

    def display_search_results(self):
        keyword = self.entry.get()
        results = self.scraper.search_news(keyword)

        self.result.delete(1.0, tk.END)
        for title, href in results.items():
            self.result.insert(tk.END, f"标题：{title}\n链接：{href}\n\n")

    def display_hot_topics(self):
        hot_topics = self.scraper.get_hot_topics(self.top_n, self.min_length)

        self.result.delete(1.0, tk.END)
        i = 0
        for word, count in hot_topics:
            i += 1
            self.result.insert(tk.END, f'top{i}:{word}，出现次数:{count}\n')

    def set_min_length(self):
        self.min_length = int(self.min_length_entry.get())

    def set_top_n(self):
        self.top_n = int(self.top_n_entry.get())

        # 添加结束程序的方法

    def end_program(self):
        # 清空窗口
        self.result.delete(1.0, tk.END)
        # 播放结束动画
        self.play_end_video(self.end_video_path)


    # 开场动画
    def start_program(self):
        # 播放开始动画
        self.play_start_video(self.start_video_path)

    def open_image_window(self):
        self.image_window = tk.Toplevel(self.root)
        self.image_window.title("查看链接中的图片")

        self.image_entry = tk.Entry(self.image_window, font=("Arial", 12))
        self.image_entry.pack(padx=10, pady=10)

        submit_button = tk.Button(self.image_window, text="提交链接", command=self.fetch_image_links, font=("Arial", 12))
        submit_button.pack(pady=10)

        self.prev_button = tk.Button(self.image_window, text="上一张", command=self.show_previous_image, font=("Arial", 12))
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.image_window, text="下一张", command=self.show_next_image, font=("Arial", 12))
        self.next_button.pack(side=tk.RIGHT, padx=10)

    def fetch_image_links(self):
        url = self.image_entry.get()
        self.image_links = self.scraper.fetch_image_links(url)
        self.current_image_index = 0
        self.show_image_by_index(self.current_image_index)

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image_by_index(self.current_image_index)

    def show_next_image(self):
        if self.current_image_index < len(self.image_links) - 1:
            self.current_image_index += 1
            self.show_image_by_index(self.current_image_index)

    def show_image_by_index(self, index):
        img_data = self.scraper.fetch_image_single(self.image_links[index])
        if img_data:
            self.show_image(img_data)
        else:
            print("Failed to fetch the image data.")

    def show_image(self, img_data):
        # 清除原来的图片
        for widget in self.image_window.winfo_children():
            if isinstance(widget, tk.Label) and hasattr(widget, 'image'):
                widget.destroy()

        # 使用 BytesIO 创建一个文件对象
        img_data = BytesIO(img_data)

        # 使用 Pillow 打开图片文件
        img = Image.open(img_data)
        # 创建一个 PhotoImage 对象，用于在 Tkinter 窗口中显示
        photo = ImageTk.PhotoImage(img)

        # 在窗口中创建一个 Label，用于显示图片
        img_label = tk.Label(self.image_window, image=photo)
        img_label.image = photo  # 保持对 PhotoImage 对象的引用
        img_label.pack()
    def play_end_video(self, video_path):
        # 使用 OpenCV 打开视频
        cap = cv2.VideoCapture(video_path)

        # 在当前窗口显示视频
        self.video_label = tk.Label(self.root)
        self.video_label.place(x=0, y=0, relwidth=1, relheight=1)  # 覆盖整个窗口

        def update_frame():
            # 读取下一帧
            ret, frame = cap.read()
            if ret:
                # Resize the frame to fit the window
                frame = cv2.resize(frame, (self.root.winfo_width(), self.root.winfo_height()))

                # 将 OpenCV 图像转换为 Tkinter 图像并显示
                image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.video_label.configure(image=image)
                self.video_label.image = image
                self.root.after(20, update_frame)
            else:
                # 视频播放完毕，移除视频 Label
                cap.release()
                self.video_label.place_forget()  # 移除视频标签
                # 这里加入关闭主窗口的动作
                self.root.destroy()

        update_frame()


    def play_start_video(self, video_path):
        # 使用 OpenCV 打开视频
        cap = cv2.VideoCapture(video_path)

        # 在当前窗口显示视频
        self.video_label = tk.Label(self.root)
        self.video_label.place(x=0, y=0, relwidth=1, relheight=1)  # 覆盖整个窗口

        def update_frame():
            # 读取下一帧
            ret, frame = cap.read()
            if ret:
                # Resize the frame to fit the window
                frame = cv2.resize(frame, (self.root.winfo_width(), self.root.winfo_height()))

                # 将 OpenCV 图像转换为 Tkinter 图像并显示
                image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.video_label.configure(image=image)
                self.video_label.image = image
                self.root.after(20, update_frame)
            else:
                # 视频播放完毕，移除视频 Label
                cap.release()
                self.video_label.place_forget()  # 移除视频标签

        update_frame()

    def open_game(self):
        game_window = tk.Toplevel(self.root)
        game_window.title("数字滑块游戏")
        # 创建游戏对象
        game = SlidePuzzleGame(game_window , 3)
        game.update_runtime()  # 启动运行时间更新


    # def play_video(self, path):
    #     if platform.system() == "Windows":
    #         os.startfile(path)
    #     elif platform.system() == "Darwin":
    #         subprocess.call(("open", path))
    #     else:
    #         subprocess.call(("xdg-open", path))
    # def open_hyperlink(self, event):
    #     # 获取点击的位置
    #     click_position = self.result.index("@{},{} linestart".format(event.x, event.y))
    #
    #     # 获取该位置的行内容，即链接
    #     hyperlink = self.result.get(click_position, "{} lineend".format(click_position))
    #
    #     # 使用 strip 方法去掉链接前后的空白字符
    #     hyperlink = hyperlink.strip()
    #
    #     # 使用默认的 web 浏览器打开链接
    #     webbrowser.open(hyperlink)
    #
    #     subprocess.Popen(["chrome", hyperlink])
