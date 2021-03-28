import numpy as np
import scipy.optimize as sco
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import time

def f_function(x, *f_args):
    """Calculate the result of function f(x) = p(x) + kcos(x).

    Keyword arguments:
    x (float): input value of function
    f_args (int, list(float), float): arguments of function, in order:
        n: degree of polinomial part of f
        p_coef: list of coefficients of the polinomial part of f
        k: coefficient of cosine part of f

    Returns:
    float: Result of f(x)
    """
    n, p_coef, k = f_args

    result = k * np.cos(x)
    for i in range(n+1):
        result += p_coef[i]*np.power(x, i)

    return result

def root_calculator(f, x0, i_max, x_tol, f_args):
    """Calculate the roots of function f

    Keyword arguments:
    f (function): function f
    x0 (float): initial iteration value
    i_max (int): max number of iteration
    x_tol (float): iteration tolerance
    f_args (tuple): extra arguments of f

    Returns:
    float: root of function f
    dictionary: dictionary with extra informations
    """
    root, infodict, _, _ = sco.fsolve(f, x0, args = f_args, xtol = x_tol, maxfev = i_max, full_output=True)
    return root, infodict

def plot_error(f, f_args, i_number, x0):
    """Calculate and plot absolute error

    Keyword arguments:
    f (function): function f
    f_args (tuple): arguments of function f
    i_number (int): number of iterations done
    x0 (float): initial iteration value

    Returns:
    float: absolute error
    string: name of generated graph
    """
    real_result = sco.fsolve(f, x0, args=f_args)
    xn = x0
    errors = []
    x_axis = []

    plt.style.use('dark_background')

    for i in range(i_number):
        xn = sco.fsolve(f, xn, args=f_args, maxfev=1)
        errors.append(np.abs(xn - real_result))
        x_axis.append(i+1)
        i += 1
    
    plt.plot(errors)
    plt.title("Absolute error per iteration")
    plt.xlabel("Number of iteration")
    plt.ylabel("Absolute error")
    graph_name = "graph" + str(time.time()) + ".png"

    for filename in os.listdir('static/img'):
        if filename.startswith('graph'):
            os.remove('static/img/' + filename)

    plt.savefig('static/img/' + graph_name)
    plt.clf()

    return np.abs(xn - real_result), graph_name

def calculate(initial_value, max_iterations, tolerance, args):
    """Start calculations

    Keyword arguments:
    initial_value (float): initial value of iterations
    max_iterations (int): max number of iterations to do
    tolerance (float): tolerance of 
    args (tuple): extra arguments of function f

    Returns:
    float: root of function
    float: absolute error
    dictionary: extra informations
    string: name of generated graph
    """
    root, infodict = root_calculator(f_function, initial_value, max_iterations, tolerance, args)
    error, graph_name = plot_error(f_function, args, infodict["nfev"], 2)
    return root, error, infodict["nfev"], graph_name

if __name__ == "__main__":
    args = (2, [1, -2, 1], 0)
    root, infodict = root_calculator(f_function, 1.5, 100, 0.0000001, args)
    plot_error(f_function, args, infodict["nfev"], 2)

    args = (2, [1, -5, 1], 0)
    root, infodict = root_calculator(f_function, 1.5, 100, 0.0000001, args)
    plot_error(f_function, args, infodict["nfev"], 2)
    