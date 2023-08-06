from os import system, _exit

def __main__():
    print('This program needs modle "pip-rivew".You should check whether your computer has installed this modle.')
    a = input('[L]-list  [I]-install"pip-review"  [N]-next  [E]-exit : ')
    if a == "L" or "l":
        system("python -m pip list")
    elif a == "I":
        system("python -m pip install pip-review")
    elif a == "E":
        _exit(1)
    elif a == "N":
        b = input("trusted host:")
        if b == None or "" or " ":
            system("pip-review --local --interactive")
        else:
            c = "pip-review --local --interactive --trusted-host " + b
            system(c)
    else:
        raise RuntimeError("Undefind input.")
