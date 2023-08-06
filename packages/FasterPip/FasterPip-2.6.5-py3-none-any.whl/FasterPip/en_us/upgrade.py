from os import _exit
import tkinter
from tkinter import ttk
from pip._internal.cli.main import main
from tkinter.messagebox import showwarning
from time import sleep
a = None
b = None
f = []

def __main__():
    win = tkinter.Tk()
    win.title("upgrade|FasterPip")
    win.geometry("350x130+100+100")
    win.iconbitmap(None)
    
    tkinter.Label(win, text="Download ", font=("楷体", 15)).place(x=5, y=1)
    tkinter.Label(win, text="website:", font=("楷体", 15)).place(x=5, y=20)
    tkinter.Label(win, text="Modle name:", font=("楷体", 15)).place(x=5, y=45)
    def go(*args):
        global a, b
        a = comvalue.get()  
    e1 = tkinter.StringVar()
    e2 = tkinter.Entry(win, textvariable=e1, font=("楷体", 15), width=15).place(x=115, y=43)
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
        print("Trying command:" + e)
        f.append("install")
        f.append("--upgrade")
        f.append(b)
        f.append("-i")
        f.append(c)
        main(args=f)
        print("Program will exit after 5 second.")
        sleep(5)
        _exit(1)
    
    tkinter.Button(win, text="Upgrade now!", font=("楷体", 15), command=og).place(x=100, y=90)
    win.mainloop()
