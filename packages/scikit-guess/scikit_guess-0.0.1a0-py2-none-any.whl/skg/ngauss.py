r"""
N-dimensional, unnormalized Gaussian fit.

This method is adapded from the references to apply to any number of
dimensions.

.. math::

   f(\vec{x}) = a e^{-\frac{1}{2} \left(\vec{x} - \vec{\mu}\right)^T \Sigma^{-1} \left(\vec{x} - \vec{\mu}\right)}

Here, :math:`\Sigma` is the covariance matrix that describes the
ellipsoid of the Gaussian. If this were a density function, the
amplitude ``a`` would be fixed at
:math:`\frac{1}{\sqrt{\left(2 \pi\right)^k det \Sigma}}`.

This function is specially suited for work with images. A wrapper to
facilitate image inputs is therefore provided.
"""

from __future__ import absolute_import, division

from numpy import array, cumsum, diff, empty, exp, sqrt
from scipy.linalg import lstsq

from ._util import preprocess


__all__ = ['ngauss_fit', 'ngauss_from_images']


def ngauss_fit(x, y, sorted=True):
    r"""
    Gaussian bell curve fit of the form
    :math:`a e^{-\frac{1}{2}\left(\frac{x - \mu}{\sigma}\right)^2}`.

    This implementation is based on an extentsion the approximate
    solution to integral equation :eq:`gauss-pdf-eq`, presented in
    :ref:`ref-reei` and extended in :ref:`reei-supplement-extended`.

    Parameters
    ----------
    x : array-like
        The x-values of the data points. The fit will be performed on a
        raveled version of this array.
    y : array-like
        The y-values of the data points corresponding to `x`. Must be
        the same size as `x`. The fit will be performed on a raveled
        version of this array.
    sorted : bool
        Set to True if `x` is already monotonically increasing or
        decreasing. If False, `x` will be sorted into increasing order,
        and `y` will be sorted along with it.

    Return
    ------
    a, mu, sigma : ~numpy.ndarray
        A three-element array containing the estimated amplitude, mean
        and standard deviation, in that order.

    References
    ----------
    .. [1] S. M. Anthony and S. Granick, "Image Analysis with Rapid and Accurate Two-Dimensional Gaussian Fitting"
       http://groups.mrl.illinois.edu/granick/publications/pdf%20files/2009/Image_Analysis_with_2D_Gaussian_Fit_la900393v.pdf
    .. [2] X. Wan, G. Wang, X. Wei, J. Li, and G. Zhang, "Star Centroiding Based on Fast Gaussian Fitting for Star Sensors"
       https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6163372/
    """
    x, y = preprocess(x, y, sorted)

    d = 0.5 * diff(x)
    xy = x * y

    # Did a timeit. This is the fastest way I could find to fill the matrix
    M = empty(xy.shape + (2,), dtype=xy.dtype)
    M[0, :] = 0
    cumsum((y[1:] + y[:-1]) * d, out=M[1:, 0])
    cumsum((xy[1:] + xy[:-1]) * d, out=M[1:, 1])

    Y = y - y[0]

    (A, B), *_ = lstsq(M, Y, overwrite_a=True, overwrite_b=True)

    mu, sigma = -A / B, sqrt(-1.0 / B)

    # Timeit shows that this is faster than a2 = model(x, 1.0, mu, sigma)
    m = exp(-0.5 * ((x - mu) / sigma)**2)
    amp = y.dot(m) / m.dot(m)

    out = array([amp, mu, sigma])

    return out


def ngauss_from_image(img):
     ...


def model(x, a, mu, sigma):
    r"""
    Compute :math:`y = a e^{-\frac{1}{2}\left(\frac{x - \mu}{\sigma}\right)^2}`.

    Parameters
    ----------
    x : array-like
        The value of the model will be the same shape as the input.
    a : float
        The amplitude at :math:`x = \mu`.
    mu : float
        The mean.
    sigma : float
        The standard deviation.

    Return
    ------
    y : array-like
        An array of the same shape as `x`, containing the model
        computed for the given parameters.
    """
    return a * exp(-0.5 * ((x - mu) / sigma)**2)


ngauss_fit.model = model

