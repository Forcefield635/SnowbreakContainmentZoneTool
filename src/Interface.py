from tkinter import *
import main1 as ma
text_content = """
123
"""


class Application(Tk):
    def __init__(self):
        super().__init__()
        # self.attributes('-topmost', True)
        self.config(bg='#ffffff')

        self.title("My_window")
        self.geometry("1200x720")
        # self.update()

        self.create_widgets()
        self.create_leftinfo()
        self.create_topinfo()
        self.create_continfo()

    def create_widgets(self):
        self.leftframe = Frame(self.master, width=200, bg='white', relief=GROOVE, borderwidth=5)
        self.leftframe.pack(side=LEFT, fill=BOTH, padx=5, pady=0, expand=NO)

        self.topframe = Frame(self.master, height=150, bg='lightblue', relief=GROOVE, borderwidth=5)
        self.topframe.pack(padx=0, pady=0, fill=X, expand=NO)

        self.contentframe = Frame(self.master, bg='white', relief=GROOVE, borderwidth=5)
        self.contentframe.pack(padx=0, pady=0, fill=BOTH, expand=YES)

    def left_btn_click(self, type=None):
        self.curType = type
        self.curTypeLab.config(text=type)
        self.update_content_text()
        return

    def create_leftinfo(self):
        btn0 = Button(self.leftframe, text='qwer', fg="black", bg='white', height=1, width=12,
                      activebackground='lightyellow',
                      font=("楷体", 16, "bold"))
        btn0.bind('<Enter>', lambda event: event.widget.config(bg='#d3d3d3'))
        btn0.bind('<Leave>', lambda event: event.widget.config(bg='white'))
        btn0.pack(side=TOP, padx=2, pady=(2, 2), fill=X)
        for index, item in enumerate(ma.type_names_ch):
            btn = Button(self.leftframe, text=item, fg="black", bg='white', height=1, width=15,
                         activebackground='lightyellow',
                         font=("楷体", 16, "bold"))
            btn.pack(side=TOP, padx=2, pady=(2, 2), fill=X)
            btn['command'] = lambda type=ma.type_names_ch[index]: self.left_btn_click(type=type)
            btn.bind('<Enter>', lambda event: event.widget.config(bg='#d3d3d3'))
            btn.bind('<Leave>', lambda event: event.widget.config(bg='white'))

    def create_topinfo(self):

        curTypeLab0 = Label(self.topframe, text="当前记录:", fg="black", bg="#add8e6", borderwidth=2,
                            font=("楷体", 17, "bold"))
        curTypeLab0.pack(side=LEFT, padx=1, pady=1, fill=X)
        self.curType = ma.type_names_ch[0]
        self.curTypeLab = Label(self.topframe, text=self.curType, fg="black", bg="#add8e6", borderwidth=2,
                                font=("楷体", 17, "bold"))
        self.curTypeLab.pack(side=LEFT, padx=1, pady=1, fill=X)

        btn2 = Button(self.topframe, text="清理记录", fg="black", activebackground="#add8e6", height=1, width=10,
                      font=("楷体", 17, "bold"))
        btn2.bind('<Button-1>', self.test)
        btn2.pack(side=RIGHT, padx=1, pady=1, fill=X)

        btn3 = Button(self.topframe, text="刷新", fg="black", activebackground="#add8e6", height=1, width=10,
                      font=("楷体", 17, "bold"))
        btn3.bind('<Button-1>', self.update_content_text)
        btn3.pack(side=RIGHT, padx=1, pady=1, fill=X)

        btn1 = Button(self.topframe, text="查询记录", fg="black", activebackground="#add8e6", height=1, width=10,
                      font=("楷体", 17, "bold"))
        btn1.bind('<Button-1>', self.queryRecords)
        btn1.pack(side=RIGHT, padx=1, pady=1, fill=X)

    def getnamefromtype(self):
        index = 0
        for i, item in enumerate(ma.type_names_ch):
            if self.curType == item:
                index = i
                break
        return f"../data/{ma.type_names[index]}.txt"

    def create_continfo(self):
        countinfofram = Frame(self.contentframe)
        countinfofram.pack(side=LEFT, fill=BOTH, expand=YES)
        self.counttext = Text(countinfofram, width=20, height=5, bg='white', font=("楷体", 14, "bold"))
        self.counttext.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=2)
        self.update_count_text()

        scrollbar = Scrollbar(self.contentframe)
        scrollbar.config(orient=VERTICAL)
        self.titletext = Text(self.contentframe, width=53, height=1, bg='white', font=("楷体", 14, "bold"))
        self.titletext.insert(1.0, '序号 名称\t\t类型\t时间\t\t 星级\n')
        self.detailedtext = Text(self.contentframe, width=20, height=5, bg='white', font=("楷体", 14, "bold"))
        self.detailedtext.config(yscrollcommand=scrollbar.set)
        self.update_content_text()
        scrollbar = Scrollbar(self.contentframe, orient="vertical", command=self.detailedtext.yview)
        self.detailedtext.config(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.titletext.pack(side=TOP, fill=BOTH, padx=5)
        self.detailedtext.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=2)

        # self.text2 = Text(self.frame2, width=20, height=5, bg='lightyellow', relief=GROOVE)
        # self.text2.pack(side=LEFT, fill=BOTH, expand=YES)
        # self.text2.insert(1.0, text_content)
        # scrollbar.pack(side="right", fill="y")

    def update_content_text(self, event=None):
        filename = self.getnamefromtype()
        str,str2 = ma.test1(filename)
        self.counttext.delete('1.0', END)
        self.counttext.insert(END, str)

        self.detailedtext['state'] = 'normal'
        self.detailedtext.delete('1.0', END)
        self.detailedtext.insert(END, str2)

        # filename = self.getnamefromtype()
        # with open(filename, 'r', encoding='utf-8') as f:
        #     for i, line in enumerate(f):
        #         # line = line.strip()
        #         line = line.replace(',', '\t\t', 1)
        #         line = line.replace(',', '\t')
        #         # print(i, line)
        #         self.detailedtext.insert(END, f'%-3d  {line}' % (i + 1))
        #         # self.text.insert(END, line)
        self.detailedtext['state'] = 'disabled'
        print(f"更新内容为{filename}")

    def update_count_text(self):
        pass
    def setLabal(self):
        pass

    def test(self, event=None):
        print("test!", event)

    def queryRecords(self, event=None):
        curType = self.curType
        for index, item in enumerate(ma.type_names_ch):
            if curType == item:
                break
        else:
            print("未找到对应记录类型 " + curType)
            return
        print(f"开始查询{ma.type_names[index]}的记录")
        ret = ma.generateRecordByType(ma.type_names[index])
        if ret != 0:
            print("查询失败")
            return
        self.update_content_text()

    @classmethod
    def start_loop(cls):
        root = cls()
        root.mainloop()


def on_enter(event, button):
    button.config(bg='red')


if __name__ == '__main__':
    Application.start_loop()
