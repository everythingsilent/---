from UI import promptWindow
from PyQt5.QtWidgets import *

import time
from threading import Thread


def sleep_prompt(window, t):
    time.sleep(t)
    window.close()


app = QApplication([])

# 0 清醒 1 轻度 2 中度 3 重度
prompt_window = promptWindow.PromptWindow(2)
prompt_window.show()

closePromptWindow = Thread(target=sleep_prompt, args=(prompt_window, 4))
closePromptWindow.start()

app.exec_()
