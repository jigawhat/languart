#
#  Graphics library
#

from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from Utils import *


# Print mean scores for a subset of Y_labels over all increments
def print_learning_curve_mean_scores(models, scorers, scores, Y_l, to_pr=None):
    for i in range(len(models)):
        print("\t" + models[i])
        for l in range(len(scorers)):
            res = deepcopy(scores[i][l])
            for j in range(len(res)):
                res[j] = np.mean(res[j], axis=0)
            if len(to_pr) > 1:
                res = np.array(res)[:,[Y_l.index(o) for o in to_pr]]
                res = np.mean(res, axis=1)
            elif len(to_pr) == 1:
                res = np.array(res)[:,Y_l.index(to_pr[0])]
            else:
                res = np.mean(res, axis=1)
            pr(scorers[l] + ": " + str(fm_nums(res, 3)))

def graph_learning_curve(models, scorers, scores, ns_samples, Y_labels):
    fig = plt.gcf()
    n_rows = int(np.ceil(len(scorers) / 2)) * len(models)
    fig.set_size_inches(16, .3 + (4.5 * n_rows))
    plt.suptitle("Learning curves", size=15)
    # fig.savefig('test2png.png', dpi=100)
    m, handles = 0, []
    for i in range(len(models)):
        print("\t" + models[i])
        for l in range(len(scorers)):
            res = deepcopy(scores[i][l])
            for j in range(len(res)): res[j] = np.mean(res[j], axis=0)
            ax = plt.subplot(n_rows, 2, m + 1)
            m += 1
            plt.ylabel(models[i] + ' ' + scorers[l])
            plt.xlabel("N training samples")
            ax.set_xticks(ns_samples)
            ax.grid(alpha=0.5)
            r = list(zip(*res))
            for n in range(len(Y_labels)):
                p = plt.plot(ns_samples, r[n])
                if l == 0 and i == 0: handles += [ mpatches.Patch(
                    color=p[0].get_color(), label=Y_labels[n]) ]
    plt.legend(handles=handles, bbox_to_anchor=(1.05, 1))
    plt.show()


