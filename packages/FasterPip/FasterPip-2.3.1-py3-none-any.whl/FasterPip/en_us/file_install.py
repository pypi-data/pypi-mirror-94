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
    win.title("file_install|FasterPip")
    win.geometry("350x130+100+100")
    win.iconbitmap(None)

    def view():
        global b
        if b != None:
            c = b + '          Press "No" to edit the file.'
            d = askyesno("Installation file:", c)
            if d == False:
                b = askopenfilename(title="chose a file", defaultextension=True, filetypes=[("Source(tar.gz)","*.tar.gz"),("Source(zip)", "*.zip"), ("Wheel", "*.whl")])
        else:
            b = askopenfilename(title="chose a file", defaultextension=True, filetypes=[("Source(tar.gz)","*.tar.gz"),("Source(zip)", "*.zip"), ("Wheel", "*.whl")])

    def install():
        if b == None:
            showerror("Install error:", 'Please press "View!" button to choose a file.')
        else:
            a.append(b)
            print("Trying command: pip " + str(a))
            main(a)
            print("Program will exit after 5 second.")
            sleep(5)
            _exit(1)
    
    tkinter.Label(win, text="File:", font=("楷体", 15)).place(x=5, y=5)
    tkinter.Button(win, text="View!", font=("楷体", 14), command=view).place(x=60, y=2)
    tkinter.Button(win, text="Install now!", font=("楷体", 15), command=install).place(x=130, y=1)
    win.mainloop()

