import numpy as np

def bic(mse, nsamples, paramcount):
    return nsamples * np.log(mse) + paramcount * np.log(nsamples)

def aic(mse, nsamples, paramcount):
    return nsamples * np.log(mse) + 2 * paramcount