from flask import Flask
from flask import render_template
from flask import request
from root_calculator import calculate

app = Flask(__name__)

def str_to_float(string):
    try:
        return float(string)
    except:
        return 0

def str_to_non_negative_float(string):
    try:
        number = float(string)
        if number < 0:
            number = 0
        return number
    except:
        return 0

def str_to_non_negative_integer(string):
    try:
        number = int(string)
        if number < 0:
            number = 0
        return number
    except:
        return 0

def str_to_positive_integer(string):
    try:
        number = int(string)
        if number < 1:
            number = 1
        return number
    except:
        return 1

@app.route('/')
def main_page():
    return render_template('index.html', graph='img/default.png')

@app.route('/', methods=['POST'])
def get_data():
    p_degree = str_to_non_negative_integer(request.form['p_degree'])
    initial_value = str_to_float(request.form['initial_value'])
    max_iterations = str_to_non_negative_integer(request.form['max_iterations'])
    tolerance = str_to_non_negative_float(request.form['tolerance'])

    coefficients = []
    for i in range(p_degree+1):
        cur_name = "a" + str(i)
        coefficients.append(str_to_float(request.form.get(cur_name)))
    
    k = str_to_float(request.form.get('k'))

    result, error, iterations, graph_name = calculate(initial_value, max_iterations, tolerance, (p_degree, coefficients, k))

    return render_template('index.html', html_x_result=str(result[0]), html_error_result=str(error[0]), html_iterations_result=str(iterations), graph='img/' + graph_name)   


if __name__ == "__main__":
    app.run(debug=True)