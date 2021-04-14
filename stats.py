import os
import matplotlib.pyplot as plt
import numpy as np


def run_stats(file_path, name):
    data = np.fromfile(file_path, dtype=int, sep=" ")
    # print(data)
    fig, ax = plt.subplots()
    ax.hist(data)
    ax.set_xlabel("Score")
    ax.set_ylabel("Times achieved score")
    ax.set_title(name)
    plt.show()


location = os.getcwd()
score_files = os.listdir(os.path.abspath(os.path.join(location, "scores")))

for score_file in score_files:
    path = os.path.abspath(os.path.join(location, "scores", score_file))
    run_stats(path, score_file)
