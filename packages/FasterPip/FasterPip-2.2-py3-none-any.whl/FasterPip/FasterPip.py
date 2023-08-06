from en_us import web_install as en

def helpmain():
    a = 'Visit URL:"https://github.com/mstouk57g/FasterPipblob/main/README.md"'
    return a
def run(language="en_us", mode="web_install"):
    if language == "en_us":
        en()
    else:
        raise RuntimeError("FasterPip doesn't support the language what you input.")









































