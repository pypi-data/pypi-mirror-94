__all__ = [
    "weighted_polynomial_reg",
    "extrapolate_power_law",
    "gaussian_smoothing",
    "conv_vwf",
    "polynomial",
]


def weighted_polynomial_reg(X, Y, w, degree=1):

    # 3rd party import
    import numpy as np
    from sklearn.preprocessing import PolynomialFeatures, normalize
    from sklearn.linear_model import LinearRegression

    X = X.reshape(-1, 1)
    Y = Y.reshape(-1, 1)
    w = w.reshape(-1, 1)

    poly_reg = PolynomialFeatures(degree=degree)
    X_poly = poly_reg.fit_transform(X)  # Vandermonde Matrix

    # Solve Weighted Normal Equation
    A = np.linalg.inv(X_poly.T @ (w * X_poly))
    beta = (A @ X_poly.T) @ (w * Y)

    return beta


def polynomial(x, coeff):
    #Define Polynomial - Use Numpy for optimization
    y = 0
    for p, c in enumerate(coeff):
        y += c * x**p
    return y

def extrapolate_power_law(h, v):

    """
    h = list of heights for which we have measurements
    v = list of speeds at those heights
    hx = hub height at which you want to know the speed
    """

    # 3rd party import
    import numpy as np

    log_h = np.log(h)

    weights = [1, 1, 2]

    # linearise and perform a ls fit
    # weight the data at 50m more strongly
    log_h = np.log(h)

    fit = weighted_polynomial_reg(log_h, v, weights, degree=1)

    # extract our coefficients
    # v2 / v1 =  (h2 / h1) ^ alpha, therefore v2 = epsilon * h ^ alpha
    epsilon = np.exp(fit[0])
    alpha = fit[1]

    return epsilon, alpha


def gaussian_smoothing(mu, sig, x, y):

    """translation of the function convoluteFarmCurve = function(myCurve,
    myMean, mySD) ( VWF-EXTRAS.R) from R to Python.
    
    Args:
        mu (float) : gauss filter mean value
        sig (float) : gauss filter sigma
        x (nparray) : weed speed values
        y (nparray) : Power response
    Returns:
        y_convolve (np.array) : smoothed power curve
    
    """
    import numpy as np

    def gaussian(x, mu, sig):
        return (
            1.0
            / (np.sqrt(2.0 * np.pi) * sig)
            * np.exp(-np.power((x - mu) / sig, 2.0) / 2)
        )

    # zero padding
    x_filter = np.arange(-10, 45.01, 0.01)
    y_filter = np.concatenate((np.zeros(1000), y, np.zeros(1000)))

    # gaussian convolution
    w = 10
    convolver_x = np.arange(-w, w + 0.01, 0.01)
    convolver_y = gaussian(convolver_x, mu, sig)
    convolver_y = convolver_y / sum(convolver_y)
    y_convolve = np.convolve(y_filter, convolver_y, mode="same")
    y_convolve = y_convolve[
        min(np.argwhere(x_filter >= 0))[0] : min(np.argwhere(x_filter >= 35))[0]
    ]
    x_filter = x_filter[
        min(np.argwhere(x_filter >= 0))[0] : min(np.argwhere(x_filter >= 35))[0]
    ]

    return x_filter, y_convolve


def conv_vwf(ws, alpha, beta, power):

    """
    Smoothing procedure of a power curve using the procedure descibed in :
    https://ars.els-cdn.com/content/image/1-s2.0-S0360544216311811-mmc1.pdf
    
    Args:
        ws (nparray): a list of wind speed values w
        alpha (float): sigma = alpha * w + beta
        beta (float): sigma = alpha * w + beta
        power (nparray): manufacturer power curve (the wind speed sample interval is 
                        supposed to be equal to 0.01 m/s)
        
    Returns:
        power_conv (nparray): convolution of the power curve computed at at speed values ws
    """

    # Standard library import
    from collections import deque

    # 3rd party imports
    import numpy as np

    delta_w = 0.01  # should be an argument

    speed_widening = 10  # m/s
    n_zero_padd = int(speed_widening / delta_w)  # must be even

    power_conv = []
    for w in ws:
        sigma_square = beta + alpha * w  # note we will use sigma^2
        n_sigma_square = 4

        # kernel support we take int(sigma_square+1) to take care of sigma_square<1 which
        # would result in a zero size support
        kernel_support = np.arange(
            -int(n_sigma_square * int(sigma_square + 1)),
            int(n_sigma_square * int(sigma_square + 1)) + delta_w,
            delta_w,
        )  # m/s
        len_kernel = len(kernel_support)
        idx_max_gauss = int(len_kernel / 2)

        # kernel computation on [-n_sigma_square*sigma_square, +n_sigma_square*sigma_square]
        # with a step of delta_w (m/s)
        kernel = (
            1.0
            / np.sqrt(2.0 * np.pi * sigma_square)
            * np.exp(-np.power(kernel_support, 2.0) / (2 * sigma_square))
        )

        # power curve left and right zero padding
        power_ = np.concatenate((np.zeros(n_zero_padd), power, np.zeros(n_zero_padd)))
        len_power = len(power_)

        # we truncate or right padd the kernel with 0 so that len(kernel)=len(power)
        if len_kernel < len_power:
            kernel = np.concatenate((kernel, np.zeros(len_power - len_kernel)))
        else:
            kernel = kernel[0:len_power]

        # we righ rotate the kernel so that the location of its max is
        # at w + n_zero_padd * delta_w the shifted value of w
        kernel = deque(kernel)
        kernel.rotate(int((w + n_zero_padd * delta_w) / delta_w - idx_max_gauss))
        kernel = np.array(list(kernel))

        # we compute the convolution
        power_conv.append(np.dot(power_, kernel) * delta_w)

    return power_conv
