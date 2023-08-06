import numpy as np

def _residual_square_sum(actuals, expected):
    return np.sum((actuals - expected)**2)
    
def _f_statistic(rss_restricted,rss_mini, no_samples, no_parameters, no_hypoth_para):
    from scipy.stats import f
    nom = (rss_restricted - rss_mini) * (no_samples - no_parameters)
    denom = rss_mini * (no_hypoth_para)
    F = nom / denom

    dfn = no_hypoth_para
    dfd = no_samples - no_parameters
    p = 1 - f.cdf(F, dfn, dfd)

    return F, p

def _t_statistic(linear_condition, optimized_paras, actual_paras, unbiased_sample_var, no_samples, no_paras, derivative):
    from scipy.stats import t

    a = linear_condition

    nom = np.matmul(a.T,optimized_paras) - np.matmul(a.T, actual_paras)
    denom = unbiased_sample_var * np.sqrt(np.matmul(np.matmul(a.T, np.linalg.inv(derivative)). a))
    T = nom / denom

    df = no_samples - no_paras
    if T < 0:
        p = t.cdf(T, df)
    else:
        p = 1 - t.cdf(T, df)
    
    return T, p

def _calculate_no_para(graph):
    no_para = 0
    for inter in graph:
        if 'linear' in inter.spec:
            no_para += 2
        
        if 'cat' in inter.spec:
            no_para += len(inter.state.categories) + 1

    return no_para

def _amount_of_weights_on_variables_in_graph(graph):
    count = 0
    for inter in graph:
        if 'out' in inter.spec:
            break

        if 'linear' in inter.spec:
            count += 1
        
        if 'cat' in inter.spec:
            count += len(inter.state.categories)
    return count

def _get_no_samples(graph, data):
    target = graph.target
    return data[target].shape[0]

def graph_f_score(graph,data):
    """
    This computes the F-statistic associated to a feyn graph under the null hypothesis.
    The null hypothesis is that every weight on each feature and category is equal to zero.
    
    If the hypothesis is true then the F-score is distributed by F(q, n - p), 
    the Fisher distribution of q and n-p degrees of freedom. Here:
    * q is the amount of weights we assume is equal to zero 
    * n is the amount of samples in data
    * p amount of parameters in the graph. The F score is calculated by:
    nom = {sum((data[target].mean - data[target])**2) - (graph.mse(data) * n)} * (n-p)
    denom = (graph.mse(data) * n) * q
    F = nom / denom

    Arguments:
        graph {[feyn.Graph]} -- Graph to test null hypothesis.
        data {[dic of numpy arrays or pandas dataframe]} -- Data to test significance of graph on.

    Returns:
        tuple -- The F score of hypothesis and p value
    """

    target = graph.target
    no_samples = _get_no_samples(graph,data)

    rss_mini = graph.mse(data) * no_samples
    target_sample_mean = data[target].mean()
    rss_restricted = _residual_square_sum(data[target], target_sample_mean)
    
    no_para = _calculate_no_para(graph)
    no_hypoth_para = _amount_of_weights_on_variables_in_graph(graph)

    f_score, p_value = _f_statistic(rss_restricted, rss_mini, no_samples, no_para, no_hypoth_para)

    return f_score, p_value

def plot_graph_p_value(graph, data, title = 'Significance of graph', ax=None):
    """
    Plots the probability density function of the Fisher distribution
    under the null hypothesis.
    The null hypothesis is that every weight on each feature and category is equal to zero.
    
    If the hypothesis is true then the F-score is distributed by F(q, n - p), 
    the Fisher distribution of q and n-p degrees of freedom. Here:
    * q is the amount of weights we assume is equal to zero 
    * n is the amount of samples in data
    * p amount of parameters in the graph.
    
    This also plots vertical lines intercepting the x-axis at the F scores under each hypothesis.

    Arguments:
        graph {[feyn.Graph]} -- Graph to calculate p-values of under the null hypothesis
        data {[dic of numpy arrays or pandas dataframe]} -- Data to test significance of graph on. 

    Keyword Arguments:
        title {str} -- [Title of axes] (default: {'Significance of graph'})
        ax {[matplotlib.Axes]} -- (default: {None})

    Returns:
        [matplotlibe.Axes] -- Plots of Fischer distributions and associated F scores
    """
    from scipy.stats import f
    import matplotlib.pyplot as plt

    if ax is None:
        ax = plt.subplot()

    f_score, p_value = graph_f_score(graph, data)

    no_para = _calculate_no_para(graph)
    no_samples = _get_no_samples(graph,data)

    dfn = _amount_of_weights_on_variables_in_graph(graph)

    dfd = no_samples - no_para

    #F-distr under the hypothesis where weights are equal to zero
    x_axis_var = np.linspace(f.ppf(0.01, dfn, dfd), f.ppf(0.99, dfn, dfd), 100)
    f_pdf = f.pdf(x_axis_var, dfn, dfd)
    x_threshold = x_axis_var[x_axis_var > f_score]

    ax.set_title(title)
    ax.set_ylabel("Probability density")
    ax.set_xlabel('F')

    ax.plot(x_axis_var, f_pdf, alpha = 0.5, label = f'F{dfn,dfd}')

    # Plot F scores
    ax.fill_between(x_threshold, f.pdf(x_threshold, dfn, dfd), alpha=0.3, label = f'p-value, features: {p_value: .4f}' )
    ax.axvline(f_score, ls = '--', lw = 2, label = f'F-score, features: {f_score: 4f}')
    ax.legend()

    return ax