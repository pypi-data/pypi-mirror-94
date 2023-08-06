import os
import dill
import numpy as np
import pandas as pd

# from hyperactive import Hyperactive, LongTermMemory, Dashboard

from .long_term_memory import LongTermMemory


def objective_function(opt):
    score = opt["x1"] * opt["x1"]
    return -score


def func1():
    """stuff"""


def func2():
    pass


search_space = {
    "x1": list(np.arange(-3, 1, 1)),
    "x2": [[1, 2], [2, 1]],
    "x3": [func1, func2],
}
columns = ["x1", "x2", "x3", "score"]
df_array = [
    [-1, [1, 2], func1, 0.5],
    [-2, [2, 1], func1, 0.5],
    [-3, [1, 2], func2],
    0.5,
]
dataframe = pd.DataFrame(df_array, columns=columns)


mem = LongTermMemory("test_model_name")

mem.save(dataframe, objective_function)
dataframe_reload = mem.load()


obj_list = list(dataframe["x3"].values)
obj_list_reload = list(dataframe_reload["x3"].values)


func1_byte = dill.dumps(func1)
func1_reloaded_byte = dill.dumps(func1_reloaded)

print("\n func1 \n", func1)
print("\n func1_reloaded \n", func1_reloaded)

print("Objects equal:", func1 == func1_reloaded)
print("Object byte equal:", func1_byte == func1_reloaded_byte)


func1_new = dill.loads(func1_byte)
func1_reloaded_new = dill.loads(func1_reloaded_byte)

print("\n func1_new \n", func1_new)
print("\n func1_reloaded_new \n", func1_reloaded_new)
