from fraction import Fract
from task import Task
import numpy as np
import eel


@eel.expose
def solve(n, m, c, a, c_l=[]):
    task = Task(n, m, c, a, c_l)
    return task.solve()


eel.init("web", allowed_extensions=[".js", ".html"])
eel.start("index.html")
