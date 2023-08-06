from os import system, _exit
from pip._internal.cli.main import main
import tkinter
from time import sleep
from tkinter import ttk
a = None
b = None
f = []

def __main__():
    win = tkinter.Tk()
    win.title("网络安装|FasterPip")
    win.geometry("350x130+100+100")
    
    tkinter.Label(win, text="下载网站:", font=("楷体", 15)).place(x=5, y=5)
    tkinter.Label(win, text="模块名称:", font=("楷体", 15)).place(x=5, y=30)
    def go(*args):
        global a, b
        a = comvalue.get()  
    e1 = tkinter.StringVar()
    e2 = tkinter.Entry(win, textvariable=e1, font=("楷体", 15), width=15).place(x=105, y=30)
    comvalue=tkinter.StringVar()
    comboxlist=ttk.Combobox(win,textvariable=comvalue)
    comboxlist.place(x=105, y=5)
    comboxlist.pack()
    comboxlist["values"]=("1","2","3","4","5","6","PyPI","TestPyPI")
    comboxlist.current(6)
    comboxlist.bind("<<ComboboxSelected>>",go)
    
    def og(*args):
        b = e1.get() 
        d = {"PyPI":"https://pypi.org/simple/",
            "TestPyPI":"https://test.pypi.org/simple/",
            "6":"https://pypi.douban.com/simple/",
            "2":"https://mirrors.aliyun.com/pypi/simple/",
            "4":"https://pypi.hustunique.com/simple/",
            "3":"https://pypi.sdutlinux.org/simple/",
            "5":"https://pypi.mirrors.ustc.edu.cn/simple/",
            "1":"https://pypi.tuna.tsinghua.edu.cn/simple"}
        if a == None:
            c = "https://pypi.org"
        else:
              c = d.get(a)
        e = "python -m pip install " + b +" -i " + c
        print("尝试命令:" + e)
        f.append("install")
        f.append("--upgrade")
        f.append(b)
        f.append("-i")
        f.append(c)
        main(args=f)
        print("文件将在 5 秒后退出。")
        _exit(1)
    
    tkinter.Button(win, text="更新模块", font=("楷体", 15), command=og).place(x=100, y=90)
    win.mainloop()

