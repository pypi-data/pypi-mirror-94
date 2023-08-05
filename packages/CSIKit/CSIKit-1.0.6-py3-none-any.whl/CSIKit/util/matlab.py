import numpy as np
np.seterr(divide="ignore")

def dbinv(x):
    return np.power(10, x/10)

def db(x, metric="voltage"):
    if metric == "voltage":
        return 20 * np.log10(x)
    elif metric == "pow":
        return 10 * np.log10(x)