from pip._internal.cli.main import main
import tkinter
from os import _exit
from time import sleep
from tkinter.messagebox import showwarning, askyesno, showerror
from tkinter.filedialog import askopenfilename
a = ["install"]
b = None

def __main__():
    win = tkinter.Tk()
    win.title("文件安装|FasterPip")
    win.geometry("350x130+100+100")
    win.iconbitmap(None)

    def view():
        global b
        if b != None:
            c = b + '          按 "否定" 键更改安装文件。'
            d = askyesno("Installation file:", c)
            if d == False:
                b = askopenfilename(title="选择文件", defaultextension=True, filetypes=[("Source(tar.gz)","*.tar.gz"),("Source(zip)", "*.zip"), ("Wheel", "*.whl")])
        else:
            b = askopenfilename(title="选择文件", defaultextension=True, filetypes=[("Source(tar.gz)","*.tar.gz"),("Source(zip)", "*.zip"), ("Wheel", "*.whl")])

    def install():
        if b == None:
            showerror("安装错误:", '请按“选择”键选择安装源文件。')
        else:
            a.append(b)
            print("尝试命令: pip " + str(a))
            main(a)
            print("文件将在 5 秒后退出。")
            sleep(5)
            _exit(1)
    
    tkinter.Label(win, text="文件:", font=("楷体", 15)).place(x=5, y=5)
    tkinter.Button(win, text="选择", font=("楷体", 14), command=view).place(x=60, y=2)
    tkinter.Button(win, text="现在安装", font=("楷体", 15), command=install).place(x=130, y=1)
    win.mainloop()

