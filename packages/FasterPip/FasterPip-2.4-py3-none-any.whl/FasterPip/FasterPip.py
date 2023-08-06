from en_us.web_install import __main__ as en_web_install
from zh_cn.web_install import __main__ as zh_web_install
from en_us.file_install import __main__ as en_file_install
from zh_cn.file_install import __main__ as zh_file_install

def helpmain():
    a = 'Visit URL:"https://github.com/mstouk57g/FasterPipblob/main/README.md"'
    return a
def run(language="en_us", mode="web_install"):
    def men(mode="web_install"):
        if mode == "web_install":
            en_web_install()
        elif mode == "file_install":
            en_file_install()
        else:
            raise RuntimeError("FasterPip doesn't support the mode what you input.")
        
    def mzh(mode="web_install"):
        if mode == "web_install":
            zh_web_install()
        elif mode == "file_install":
            zh_file_install()
        else:
            raise RuntimeError("FasterPip 不支持您所输入的模式。")
        
    if language == "en_us":
        men(mode=mode)
    elif language == "zh_cn":
        mzh(mode=mode)
    else:
        raise RuntimeError("FasterPip doesn't support the language what you input.")

if __name__ == "__main__":
    run(language="en_us", mode="web_install")

































