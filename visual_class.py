import tkinter as tk
from tkinter import Tk, Text
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import messagebox

import crawler
from crawler import *
class MainGUI:
    def __init__(self):
        self.label = []
        self.root = tk.Tk()
        self.root.title("落谷题库")
        self.root.geometry("800x400")
        self.root.resizable(width=False, height=False)
        self.create_widgets()

    def create_widgets(self):
        # "难度选择:"标签
        difficultyLabel = tk.Label(self.root, text="难度选择:")
        difficultyLabel.grid(column=0, row=0)
        # 难度选择框
        difficulty = tk.StringVar()
        difficultyChosen = ttk.Combobox(self.root, width=12, textvariable=difficulty)
        difficultyChosen['values'] = (
        '难度', '入门', '普及-', '普及/提高-', '普及+/提高', '提高+/省选-', '省选/NOI-', 'NOI/NOI+/CTSC')
        difficultyChosen.grid(column=0, row=1)
        difficultyChosen.current(0)

        # 爬取题数：
        climb_num = tk.Label(self.root, text="爬取题数(<=50)：")
        climb_num.grid(column=2, row=0)

        # 爬取题数输入框
        climb_num_entered = tk.Entry(self.root, width=5)
        climb_num_entered.insert(0, "10")
        climb_num_entered.grid(column=2, row=1)

        # 显示按钮
        def show():
            pass
        show_button = ttk.Button(self.root, text="显示", width=10, command=show)
        show_button.grid(column=1, row=3)
        # 话痨
        bb = tk.Label(self.root, text="搜索完，然后点击完了确定，过一会儿再点这里，稍微卡一下，就能显示了")
        bb.grid(column=0, row=3)
        bb2 = tk.Label(self.root, text="还没搞定让这个程序重复爬取，目前只能重启了")
        bb2.grid(column=0, row=4)
        # “关键词：”标签
        keyLabel = tk.Label(self.root, text="关键词：")
        keyLabel.grid(column=1, row=0)

        # 关键词输入框
        keyEntered = tk.Entry(self.root, width=30)
        keyEntered.insert(0, "关键词请以空格分隔")

        def on_entry_focus_in(event):
            if keyEntered.get() == "关键词请以空格分隔":
                keyEntered.delete(0, "end")  # 清空文本框内容

        def on_entry_focus_out(event):
            if not keyEntered.get():
                keyEntered.insert(0, "关键词请以空格分隔")  # 恢复占位符文本

        keyEntered.bind("<FocusIn>", on_entry_focus_in)
        keyEntered.bind("<FocusOut>", on_entry_focus_out)
        keyEntered.grid(column=1, row=1)

        def search():
            dif_check = difficultyChosen.get()
            key_check = keyEntered.get().split()
            num_check = climb_num_entered.get()
            for i in range(len(key_check)):
                self.label.append(key_check[i])
            messagebox.showinfo(title='查询成功', message='点击确认后请稍等片刻')
            crawler.crawl(dif_check, self.label, num_check)
            insert_data(crawler.problem_num, crawler.problem_title, crawler.problem_difficulty)

        action = ttk.Button(self.root, text="搜索", width=10, command=search)
        action.grid(column=3, row=1)

        tree = Treeview(self.root, show="headings", columns=("序列号", "题号", "标题", "难度"))
        tree.column("序列号", width=50, anchor='center')
        tree.column("题号", width=150, anchor='center')
        tree.column("标题", width=250, anchor='center')
        tree.column("难度", width=150, anchor='center')
        tree.heading("序列号", text="序列号")
        tree.heading("题号", text="题号")
        tree.heading("标题", text="标题")
        tree.heading("难度", text="难度")
        tree.grid(column=0, row=2, columnspan=3, sticky="nsew")

        scrollBar = ttk.Scrollbar(self.root, orient="vertical", command=tree.yview) # 竖直滚动条
        scrollBar.grid(column=3, row=2, sticky="ns")    # columnspan=3, sticky=NSEW
        tree.configure(yscrollcommand=scrollBar.set)    # 设置滚动条

        def insert_data(problem_num, problem_title, problem_difficulty):
            for i in range(len(problem_num)):
                item = [str(i+1), problem_num[i], problem_title[i], problem_difficulty[i]]
                tree.insert("", "end", values=item)
                # 绑定点击事件
                tree.bind('<Double-1>', show_saved_content)

        def show_saved_content(event):
            # 获取选中行的数据
            selected_item = tree.focus()
            selected_data = tree.item(selected_item)['values']

            # 获取Markdown文本内容（假设保存在列表的第三个元素）
            markdown_content = crawler.problem_details[int(selected_data[0])-1]

            # 在弹出窗口中展示Markdown文本内容（你可以使用自己喜欢的GUI库）
            # 这里给出一个简单的示例使用 tkinter 实现窗口展示

            # 创建窗口
            window = Tk()

            # 创建文本框
            text_box = Text(window)
            text_box.insert('1.0', markdown_content)
            text_box.pack()

            # 在界面底部添加一个按钮，打开新窗口展示题解
            def show_solution():
                # 获取Markdown文本内容
                markdown_content = crawler.problem_solution[int(selected_data[0]) - 1]

                # 创建窗口
                window = Tk()

                # 创建文本框
                text_box = Text(window)
                text_box.insert('1.0', markdown_content)
                text_box.pack()

                # 运行窗口循环
                window.mainloop()

            # 创建按钮
            button = tk.Button(window, text="查看题解", command=show_solution)
            button.pack()

            # 运行窗口循环
            window.mainloop()

    def select(self):
        label = self.label
        return label
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    gui = MainGUI()
    gui.run()