import numpy as np
import scipy.optimize as sco

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
    args (tuple): extra arguments of f
    """
    root, infodict, _, _ = sco.fsolve(f, x0, args = f_args, xtol = x_tol, maxfev = i_max, full_output=True)
    return root, infodict

def plot_error(f, f_args, i_number, x0):
    real_result = sco.fsolve(f, x0, args=f_args)
    xn = x0

    for i in range(i_number):
        xn = sco.fsolve(f, xn, args=f_args, maxfev=1)
        i += 1
    
    return np.abs(xn - real_result)

def calculate(initial_value, max_iterations, tolerance, args):
    root, infodict = root_calculator(f_function, initial_value, max_iterations, tolerance, args)
    error = plot_error(f_function, args, infodict["nfev"], 2)
    return root, error

if __name__ == "__main__":
    args = (3, [3, -7, -1, 8], 8)
    root, infodict = root_calculator(f_function, -1, 100, 0.0000001, args)
    print(root)
    plot_error(f_function, args, infodict["nfev"], 2)
    