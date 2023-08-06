from .types import NPArray
from multipledispatch import dispatch
from typing import Tuple, Optional


def plot_predictions(test_points: NPArray,
                     mean: NPArray,
                     variance: NPArray,
                     ax,
                     train_points: Optional[Tuple[NPArray, NPArray]] = None,
                     legend: bool = False,
                     title: str = None):
    if train_points:
        ax.plot(train_points[0], train_points[1], 'o', label='Training data', color='tab:blue')
    ax.plot(test_points, mean, label='Predictive mean', color='tab:orange')
    ax.plot(test_points.squeeze(),
            mean.squeeze() - 1.96 * variance.squeeze(),
            mean.squeeze() + 1.96 * variance.squeeze(),
            color='tab:blue',
            alpha=0.4,
            label='Predictive variance')
    ax.plot(test_points, mean + 1.96 * variance, color="tab:blue", linestyle="--")
    ax.plot(test_points, mean - 1.96 * variance, color="tab:blue", linestyle="--")
    if legend:
        ax.legend(loc='best')
    if title:
        ax.set_title(title)
    return ax
