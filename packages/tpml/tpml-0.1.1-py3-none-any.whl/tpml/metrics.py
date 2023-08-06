import numpy as np
from .types import NPArray
from typing import Tuple
from gpflow.models.model import GPModel


def rmse(preds: NPArray, truth:NPArray):
    assert preds.ndim == truth.ndim, f"Arrays should be of equal dimension. Current dims: {preds.ndim} and {truth.ndim}"
    return np.sqrt(np.mean(np.square(preds - truth)))


def ece(mu: NPArray, truth: NPArray, n_bins: int = 10):
    if mu.ndim == 2 and mu.shape[1] == 1:
        mu = mu.squeeze()

    preds = np.where(mu < 0.5, 0, 1)
    accs = preds == truth.squeeze()

    bins = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bins[:-1]
    bin_uppers = bins[1:]
    cal_error = 0
    N = mu.shape[0]
    for bl, bu in zip(bin_lowers, bin_uppers):
        in_bin_idxs = np.where(np.logical_and(mu >= bl, mu < bu))[0]
        if in_bin_idxs.shape[0] > 0:
            in_bin_accs = accs[in_bin_idxs].mean()
            in_bin_confs = mu[in_bin_idxs].mean()
            cal_error += np.abs(in_bin_accs - in_bin_confs) * (in_bin_idxs.shape[0] / N)
    return cal_error


def accuracy(proba: NPArray, truth: NPArray, threshold: float = 0.5):
    """
    Compute accuracy for a binary classification task.
    """
    preds = np.where(proba >= threshold, 1, 0)
    acc = np.mean(preds == truth)
    return acc


def test_log_likelihood(model: GPModel, test_points: Tuple[NPArray, NPArray]):
    return np.mean(model.predict_log_density(test_points))