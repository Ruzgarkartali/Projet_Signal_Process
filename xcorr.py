import numpy as np

def xcorr(x, y, normed=True, maxlags=10, bias='biased'):
    """
    Compute the correlation between x and y.

    Args:
        x (list or array): First signal
        y (list or array): Second signal
        normed (bool, optional): If True, the correlation output is normalised in range [0,1]. Defaults to True.
        maxlags (int, optional): Maximum lag to be returned. Defaults to 10.
        bias (str, optional): Bias on the correlation (Either 'unbiased' or 'biased'). Defaults to 'biased'.

    Returns:
        np.ndarray: corresponding lags
        np.ndarray: resulting correlated signal
    """
    if y is None:
        y = x

    # Pad shorter array if signals are different lengths
    else:
        if x.size > y.size:
            pad_amount = x.size - y.size
            y = np.append(y, np.repeat(0, pad_amount))
        elif y.size > x.size:
            pad_amount = y.size - x.size
            x = np.append(x, np.repeat(0, pad_amount))

    Nx = len(x)
    if Nx != len(y):
        raise ValueError('x and y must be equal length')

    c = np.correlate(x, y, mode=2)

    if normed:
        c = c/np.sqrt(np.dot(x, x) * np.dot(y, y))

    if maxlags is None:
        maxlags = Nx - 1

    if maxlags >= Nx or maxlags < 1:
        raise ValueError('maglags must be None or strictly '
                            'positive < %d' % Nx)

    lags = np.arange(-maxlags, maxlags + 1)
    c = c[Nx - 1 - maxlags:Nx + maxlags]/Nx
    
    if bias == 'unbiased':
        for i in range(len(lags)):
            c[i] = c[i] * Nx / (Nx-np.abs(lags[i]))
        
    return lags, c