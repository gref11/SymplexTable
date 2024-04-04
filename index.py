from fraction import Fract
from task import Task
import numpy as np

# Пример
c = [1, 5, -2, 5, -1]
n = 5
m = 3
a = [[8, 3, -5, 1, -1, 0], [-20, -1, 0, -1, -1, -1], [12, 1, -2, 1, 1, -1]]

task = Task(n, m, c, a)
task.solve()