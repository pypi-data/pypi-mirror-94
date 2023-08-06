import numpy as np 


def standardise(X):
    """
    Standardise a dataset column-wise to unary Gaussian.
    Example
    -------
    >>> X = np.random.randn(10, 2)
    >>> Xtransform, Xmean, Xstd = standardise(X)
    
    """
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)
    return (X-mu)/sigma, mu, sigma


def unstandardise(X, mu, sigma):
    """
    Reproject data back onto its original scale.
    Example
    -------
    >>> X = unstandardise(Xtransform, Xmean, Xstd)
    """
    return (X*sigma)+mu

