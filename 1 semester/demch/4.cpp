#include <iostream>

#include <cmath>

#include <iomanip>

using namespace std;

long double computeFunctionValue(const long double &point);

long double
computePolynomValue(long double *coeffs, const int &size, long double *x, const long double &point);

void printArray(long double *array, const int &size, const char *discription);

void reverseArray(long double *array, const int &size);

int main() {
    int n;
    cout << "Enter the needed amount of nodes" << endl;
    cin >> n;
    long double step = 2.0 / (n - 1);
    const int size = n;
    //Задаем сетку из узловых точек и значения функции в них
    auto *node_x = new long double[size];
    auto *f_x = new long double[size];
    node_x[0] = -1.0;
    f_x[0] = computeFunctionValue(node_x[0]);
    for (int i = 1; i < size; ++i) {
        node_x[i] = node_x[0] + i * step;
        f_x[i] = computeFunctionValue(node_x[i]);
    }
    //Заполняем нулями
    auto **t_matrix = new long double *[size];
    for (int i = 0; i < size; ++i) {
        t_matrix[i] = new long double[size + 2]();
    }
    //Заполняем первые два стобца узловыми точками и соответствующими значениями функции
    for (int i = 0; i < size; ++i) {
        t_matrix[i][0] = node_x[i];
        t_matrix[i][1] = f_x[i];
    }
    for (int i = 1; i < size; ++i) {
        for (int j = 2; j <= i + 1; ++j) {
            t_matrix[i][j] =
                    (t_matrix[i][j - 1] - t_matrix[i - 1][j - 1]) / (t_matrix[i][0] - t_matrix[i - j + 1][0]);
        }
    }
    //Заполняем массив коэффициентов интерполянта Ньютона
    auto *newton_coeffs = new long double[size];
    for (int i = 0; i < size; ++i) {
        newton_coeffs[i] = t_matrix[i][i + 1];
    }
    //Чистим память, выделенную под треугольную матрицу коэффициентов
    for (int i = 0; i < size; ++i) {
        delete[] t_matrix[i];
    }
    delete[] t_matrix;
    //Вычисляем значения интерполянта Ньютона в узлах и заполняем соответствующий массив
    auto *p_values = new long double[size];
    for (int i = 0; i < size; ++i) {
        p_values[i] = computePolynomValue(newton_coeffs, size, node_x, node_x[i]);
    }
    printArray(node_x, size, "Nodes at [-1, 1]:");
    printArray(newton_coeffs, size, "Coefficients of Newton`s interpolant:");
    printArray(f_x, size, "Values of function f(x) = sin(PI * (1 + x)) at nodes:");
    delete[] f_x;
    printArray(p_values, size, "Values of Newton`s interpolant at nodes:");
    delete[] p_values;
    const int n_size = 10000;
    step = 2.0 / (n_size - 1);
    //Задаем равномерную сетку
    auto *x = new long double[n_size];
    f_x = new long double[n_size];
    //Чебышевская сетка
    auto *c_x = new long double[n_size];
    auto *c_f_x = new long double[n_size];
    for (int k = 0; k < n_size; ++k) {
        c_x[k] = cos(M_PI * (2.0 * (k + 1.0) - 1.0) / (2.0 * n_size));
    }
    reverseArray(c_x, n_size);
    for (int k = 0; k < n_size; ++k) {
        c_f_x[k] = computeFunctionValue(c_x[k]);
    }
    //Равномерная сетка
    x[0] = -1.0;
    f_x[0] = computeFunctionValue(x[0]);
    for (int i = 1; i < n_size; ++i) {
        x[i] = x[0] + i * step;
        f_x[i] = computeFunctionValue(x[i]);
    }
    p_values = new long double[n_size];
    auto *c_values = new long double[n_size];
    for (int i = 0; i < n_size; ++i) {
        p_values[i] = computePolynomValue(newton_coeffs, size, node_x, x[i]);
        c_values[i] = computePolynomValue(newton_coeffs, size, node_x, c_x[i]);
    }
    delete[] node_x;
    delete[] x;
    delete[] c_x;
    delete[] newton_coeffs;
    //Ищем модуль максимального отклонения значения интерполянта от значения функции на равномерной сетке и сетки Чебышева
    long double p_max = 0.0;
    long double c_max = 0.0;
    for (int i = 0; i < n_size; ++i) {
        long double p_temp = fabsl(f_x[i] - p_values[i]);
        long double c_temp = fabsl(c_f_x[i] - c_values[i]);
        if (p_temp > p_max) {
            p_max = p_temp;
        }
        if (c_temp > c_max) {
            c_max = c_temp;
        }
    }
    delete[] f_x;
    delete[] c_f_x;
    delete[] p_values;
    delete[] c_values;
    cout << "Value of maximal deviation on uniform grid from the value of the original function is " << p_max << endl;
    cout << "Value of maximal deviation on Chebyshev`s grid from the value of the original function is " << c_max
         << endl;
    return 0;
}

long double computeFunctionValue(const long double &point) {
    return sin(M_PI * (1.0 + point));
}


void reverseArray(long double *array, const int &size) {
    int length = size / 2;
    for (int i = 0; i < length; ++i) {
        long double temp = array[i];
        array[i] = array[size - (i + 1)];
        array[size - (i + 1)] = temp;
    }
}

long double
computePolynomValue(long double *coeffs, const int &size, long double *x, const long double &point) {
    long double result = 0.0;
    for (int i = 0; i < size; ++i) {
        long double product = 1.0;
        for (int j = 0; j < i; ++j) {
            product *= (point - x[j]);
        }
        result += coeffs[i] * product;
    }
    return result;
}

void printArray(long double *array, const int &size, const char *discription) {
    cout << discription << endl;
    bool isFirst = true;
    cout << "[";
    for (int i = 0; i < size; ++i) {
        if (isFirst) {
            isFirst = false;
        } else {
            cout << ", ";
        }
        cout << array[i];
    }
    cout << "]\n\n";
}