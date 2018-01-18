#
#  Learning utilitions
#

from sklearn.tree import *
from sklearn.multioutput import *
from sklearn.ensemble import *
from sklearn.model_selection import *
from sklearn.metrics import *
from sklearn.pipeline import *
from sklearn.preprocessing import *
from sklearn.neighbors import *
from sklearn.svm import *
from sklearn.linear_model import *
from sklearn.gaussian_process import *
from sklearn.neural_network import *

from LearningData import *


# Define scoring functions
def multitask_scorer(sfunc, y_t, y_p):
    ys=[(y_t[:,i].flatten(),y_p[:, i].flatten()) for i in range(y_t.shape[1])]
    kwargs = {}
    if sfunc in have_averaging:
        kwargs["average"] = None
    if sfunc in for_regr:
        kwargs["multioutput"] = "raw_values"
    return np.array([sfunc(y, y_, **kwargs) for y, y_ in ys])

def multitask_acc(y_t, y_p):
    return multitask_scorer(accuracy_score, y_t, y_p)

def mean_relative_error(y_true, y_pred, **kwargs):
    return mean_absolute_error(y_true, y_pred, **kwargs) / y_true

# Define models to evaluate
models_c = [
    # "GradientBoostingClassifier",
    "AdaBoostClassifier",
    "RandomForestClassifier",
    "DecisionTreeClassifier",
    "KNeighborsClassifier",
    # "MLPClassifier",
    "SVC",
    "GaussianProcessClassifier",
    "LogisticRegression",
    # "SGDClassifier",
]
models_r = [
    "RandomForestRegressor",
    "AdaBoostRegressor",
    "DecisionTreeRegressor",
    "KNeighborsRegressor",
    "SGDRegressor",
]
models_lib = {
    "AdaBoostClassifier": MultiOutputClassifier(AdaBoostClassifier()),
    "AdaBoostRegressor": MultiOutputClassifier(AdaBoostClassifier()),
    "RandomForestClassifier": MultiOutputClassifier(RandomForestClassifier()),
    "RandomForestRegressor": MultiOutputRegressor(RandomForestRegressor()),
    "DecisionTreeClassifier": MultiOutputRegressor(DecisionTreeClassifier()),
    "DecisionTreeRegressor": MultiOutputRegressor(DecisionTreeRegressor()),
    "KNeighborsRegressor": MultiOutputRegressor(KNeighborsRegressor()),
    "KNeighborsClassifier": MultiOutputRegressor(KNeighborsClassifier()),
    "MLPClassifier": MultiOutputRegressor(MLPClassifier()),
    "SVC": MultiOutputRegressor(SVC()),
    "MultiTaskLasso": MultiTaskLasso(),
    "SGDClassifier": MultiOutputClassifier(SGDClassifier()),
    "SGDRegressor": MultiOutputRegressor(SGDRegressor()),
    "LogisticRegression": MultiOutputRegressor(LogisticRegression()),
    "GradientBoostingClassifier":
        MultiOutputClassifier(GradientBoostingClassifier()),
    "GaussianProcessClassifier": MultiOutputClassifier(
        GaussianProcessClassifier(n_restarts_optimizer=5)),
}

for key in models_lib:
    models_lib[key] = Pipeline(steps=[
        ("scale", RobustScaler()),
        ("model", models_lib[key]),
    ]),

scorers_c = [
    "multitask_acc",
    "f1_score",
    "recall_score",
    "precision_score",
]
scorers_r = [
    "mean_absolute_error",
    "mean_relative_error",
    "r2_score",
    "mean_squared_error"
]
sfuncs_lib = {
    "multitask_acc": multitask_acc,
    "f1_score": f1_score,
    "recall_score": recall_score,
    "precision_score": precision_score,
    "mean_absolute_error": mean_absolute_error,
    "mean_relative_error": mean_relative_error,
    "r2_score": r2_score,
    "mean_squared_error": mean_squared_error,
    "mean_squared_log_error": mean_squared_log_error,
    "explained_variance_score": explained_variance_score,
}

have_averaging = [f1_score, precision_score, recall_score]
for_regr=[mean_absolute_error,mean_relative_error,r2_score,mean_squared_error,
          mean_squared_log_error, explained_variance_score]


def do_cv_learning_curve(X, Y, models, ns_samples, ns_eval_samples, cv=10):
    res = []
    for i in range(len(models)):
        model = models_lib[models[i]][0]
        res += [[]]
        for j in range(len(ns_samples)):
            res[-1] += [[]]
            for k in range(ns_eval_samples[j]):
                indices = np.random.choice(X.shape[0], ns_samples[j])
                res[-1][-1] += [ (cross_val_predict(model, X[indices],
                    Y[indices], cv=cv), indices) ]
    return res

def score_learning_curve(Y,Y_pr, models, ns_samples, ns_eval_samples, scorers):
    scores = []
    for i in range(len(models)):
        scores += [[]]
        for l in range(len(scorers)):
            scorer = sfuncs_lib[scorers[l]]
            scores[-1] += [[]]
            for j in range(len(ns_samples)):
                scores[-1][-1] += [[]]
                for k in range(ns_eval_samples[j]):
                    indices = Y_pr[i][j][k][1]
                    Y_pr_ = Y_pr[i][j][k][0]
                    Y_ = Y[indices]
                    scores[-1][-1][-1] += [
                        scorer(Y_, Y_pr_, multioutput="raw_values") if scorer \
                        in for_regr else (scorer(Y_, Y_pr_, average=None) if \
                        scorer in have_averaging else scorer(Y_, Y_pr_)) ]
    return scores


