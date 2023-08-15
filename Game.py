import tkinter as tk
import random
import tkinter.messagebox as mb
from tkinter import Label
import time
# 导入messagebox.askokcancel
from tkinter import messagebox
def get_inv_count(array):
    # 获取逆序对数量
    inv_count = 0
    for i in range(len(array)):
        for j in range(i+1, len(array)):
            if array[i] != '' and array[j] != '' and array[i] > array[j]:
                inv_count += 1
    return inv_count

class SlidePuzzleGame:
    def __init__(self, master, size):

        # 创建一个消息框，解释游戏规则
        mb.showinfo("规则",
                    "数字滑块游戏的目标是通过移动数字方块，使得方块的排列从1-最后一个数字，空格在右下角。"
                    "你只能移动空格相邻的方块。祝您游戏愉快")

        self.start_time = time.time()  # 记录窗口启动时间
        self.label = Label(master)
        self.label.pack()
        self.master = master  # master 是父窗口
        self.frame = tk.Frame(master)  # 创建一个新的 frame
        self.frame.pack()  # 将 frame 添加到 master
        self.size = size  # 网格的大小（比如，3 表示 3x3 的网格）
        self.empty_spot = (size-1, size-1)  # 初始的空位在 (size-1, size-1)
        self.blocks = []  # blocks 存储了所有的方块
        self.create_widgets()  # 创建方块
        self.shuffle()  # 打乱方块


    def update_runtime(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        runtime_str = f"游戏时间: {minutes:02d}:{seconds:02d}"
        # 如果时间大于 1 分钟，弹出一个消息框，询问是否继续游戏
        if seconds >= 35:
            if messagebox.askokcancel("死局提醒", "已经过去了35秒，这说明你可能已经陷入了死局，是否继续游戏？"):
                self.start_time = time.time()
            else:
                self.master.destroy()
        self.label.config(text=runtime_str)

        self.master.after(1000, self.update_runtime)  # 每秒更新一次运行时间


    def create_widgets(self):
        self.blocks = []
        for i in range(self.size):  # 遍历每一行
            row = []
            for j in range(self.size):  # 遍历每一列
                if i == self.size-1 and j == self.size-1:
                    label = tk.Label(self.frame, width=10, height=5, text='')  # 创建一个空方块
                else:
                    label = tk.Label(self.frame, width=10, height=5, text=str(i*self.size+j+1), bg='white', relief='raised', bd=3)  # 创建一个有数字的方块
                label.grid(row=i, column=j, padx=2, pady=2)  # 将方块添加到 grid 中
                label.bind("<Button-1>", self.click_block)  # 绑定点击事件
                row.append(label)
            self.blocks.append(row)

    def shuffle(self):
        numbers = list(range(1, self.size * self.size)) + ['']
        while True:
            random.shuffle(numbers)
            empty_spot = numbers.index('')
            N = (self.size - 1) - empty_spot // self.size  # 计算空格距离底部的行数
            if N % 2 ^ get_inv_count(numbers) % 2 == 0:  # 确保N和逆序对数的奇偶性异或为0
                break
        for i in range(self.size):
            for j in range(self.size):
                self.blocks[i][j]['text'] = str(numbers[i * self.size + j])
                if self.blocks[i][j]['text'] == '':
                    self.empty_spot = (i, j)

    def move_block(self, i, j):
        if abs(i - self.empty_spot[0]) + abs(j - self.empty_spot[1]) == 1:
            self.blocks[i][j]['text'], self.blocks[self.empty_spot[0]][self.empty_spot[1]]['text'] = \
                self.blocks[self.empty_spot[0]][self.empty_spot[1]]['text'], self.blocks[i][j]['text']
            self.empty_spot = (i, j)
            if self.check_win():
                if self.size == 4:
                    mb.showinfo('恭喜!', '你赢了! 你已经通关了!')
                    self.master.destroy()
                else:
                    mb.showinfo('恭喜!', '你赢了! 让我们进入下一关')
                    self.frame.destroy()  # 销毁当前游戏的窗口
                    self.start_time = time.time()  # 重置游戏开始时间
                    SlidePuzzleGame(self.master, self.size + 1)  # 创建新的游戏

    def check_win(self):
        # 检查所有的方块是否都在正确的位置
        for i in range(self.size):
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    if self.blocks[i][j]['text'] != '':
                        return False
                elif self.blocks[i][j]['text'] != str(i * self.size + j + 1):
                    return False
        return True

    def click_block(self, event):
        # 当点击一个方块时，找到被点击的方块并尝试移动它
        label = event.widget
        for i in range(self.size):
            for j in range(self.size):
                if self.blocks[i][j] == label:
                    self.move_block(i, j)
                    return
