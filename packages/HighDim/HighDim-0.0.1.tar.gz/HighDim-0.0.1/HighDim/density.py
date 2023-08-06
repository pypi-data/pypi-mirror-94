import numpy as np
from scipy.stats import beta

def _to_dirichlet(data):

    return 1/(1 + np.exp(-data))


def _num_dim(data):

    return data.shape[1]

def _dim_mean(data):

    data = _to_dirichlet(data)
    num_dim = _num_dim(data)

    mean_set = [ np.mean(data[:, dim]) for dim in range(num_dim)]

    return mean_set

def _dim_var(data):

    data = _to_dirichlet(data)
    num_dim = _num_dim(data)
    mus = _dim_mean(data)
    var_set = np.zeros_like(mus)

    for dim in range(num_dim):
        var_set[dim] = np.var(data[:,dim])

    return var_set

def _gamma_parameters(data):
    num_dim = _num_dim(data)
    mus = _dim_mean(data)
    vars = _dim_var(data)

    alphas = np.zeros_like(mus)
    betas = np.zeros_like(mus)

    for i in range(num_dim):
        nu = (mus[i]*(1-mus[i]))/vars[i] - 1
        alphas[i] = mus[i]*nu
        betas[i] = (1-mus[i])*nu

    return alphas, betas

def marginal_density(data, val):

    val = _to_dirichlet(val)
    alphas, betas = _gamma_parameters(data)
    num_dim = _num_dim(data)

    mdf = []

    for dim in range(num_dim):
        alpha = alphas[dim]
        marginal_beta = np.sum(alphas) - alphas[dim]

        pdf = beta.pdf(val, alpha, marginal_beta)

        mdf.append(pdf)

    return mdf


if __name__ == '__main__':

    #The domain of high dimensional data
    data = np.random.rand(100, 10)

    # The marginal density distribution of x
    x = 0.3

    # The marginal density distribution of x for each dimension
    distribution = marginal_density(data, x)

    print(distribution)



