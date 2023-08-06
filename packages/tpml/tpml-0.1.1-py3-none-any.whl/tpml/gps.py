from .types import NPArray
import numpy as np
import gpflow
from typing import Optional
from .printers import hline



def baseline_gpr(x: NPArray, y: NPArray, verbose: Optional[bool] = False):
    m = gpflow.models.GPR((x, y), kernel=gpflow.kernels.RBF(lengthscales = [np.sqrt(x.shape[1])] * x.shape[1]))
    opt = gpflow.optimizers.Scipy()
    res = opt.minimize(m.training_loss, m.trainable_variables, options=dict(maxiter=1000))
    if verbose:
        print(res)
        hline()
        print(m)
    return m