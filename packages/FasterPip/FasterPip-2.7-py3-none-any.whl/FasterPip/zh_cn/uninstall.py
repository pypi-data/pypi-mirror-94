from pip._internal.cli.main import main
from tkinter.messagebox import showwarning
import tkinter
a = ["uninstall"]

def __main__():
    win = tkinter.Tk()
    win.title("卸载|FasterPip")
    win.geometry("300x100+100+100")
    win.iconbitmap(None)

    def uninstall():
        c = e1.get()
        a.append(c)
        main(a)

    tkinter.Label(win, text="模块名称:", font=("楷体", 15)).place(x=5, y=1)
    e1 = tkinter.StringVar()
    e2 = tkinter.Entry(win, textvariable=e1, font=("楷体", 15), width=15).place(x=120, y=3)
    tkinter.Button(win, text="现在卸载!", font=("楷体", 15), command=uninstall).place(x=5, y=30)
    win.mainloop()

__main__()
