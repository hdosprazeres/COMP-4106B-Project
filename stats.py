import os
import matplotlib.pyplot as plt
import numpy as np


def run_stats(file_path, name):
    data = np.fromfile(file_path, dtype=int, sep=" ")
    # print(data)
    fig, ax = plt.subplots()
    ax.hist(data, color='c', edgecolor='k')
    ax.set_xlabel("Score")
    ax.set_ylabel("Times achieved score")
    ax.set_title(name)
    plt.axvline(data.min(), color='k', linestyle='dashed', linewidth=1)
    plt.axvline(data.mean(), color='k', linestyle='dashed', linewidth=1)
    plt.axvline(data.max(), color='k', linestyle='dashed', linewidth=1)
    min_ylim, max_ylim = plt.ylim()
    plt.text(data.min()+1, max_ylim*0.9, 'Min: {:.2f}'.format(data.min()))
    plt.text(data.mean()+1, max_ylim*0.9, 'Mean: {:.2f}'.format(data.mean()))
    plt.text(data.max()-7, max_ylim*0.9, 'Max: {:.2f}'.format(data.max()))
    plt.show()


location = os.getcwd()
score_files = os.listdir(os.path.abspath(os.path.join(location, "scores")))

for score_file in score_files:
    path = os.path.abspath(os.path.join(location, "scores", score_file))
    run_stats(path, score_file)
