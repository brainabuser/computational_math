#include <iostream>

#include <cmath>

using namespace std;

long double trapezoid(const int &fineness);

int main() {
    int fineness;
    cout << "Enter fineness value:" << endl;
    cin >> fineness;
    cout << "Integral value is " << trapezoid(fineness) << endl;
    cout << "Error value is " << fabs((trapezoid(fineness) - trapezoid(fineness / 2)) / -3.0) << endl;
    return 0;
}

long double trapezoid(const int &fineness) {
    const int size = fineness;
    long double step = 3.0 / (fineness - 1);
    long double *x = new long double[size];
    x[0] = 0.0;
    long double *f_x = new long double[size];
    f_x[0] = sin(100 * x[0]) * exp(-pow(x[0], 2.0)) * cos(2 * x[0]);
    long double integral = 0.0;
    for (int k = 1; k < 3 / step; ++k) {
        x[k] = x[k - 1] + step;
        f_x[k] = sin(100 * x[k]) * exp(-pow(x[k], 2.0)) * cos(2 * x[k]);
        integral += step / 2.0 * (f_x[k] + f_x[k - 1]);
    }
    delete[] x;
    delete[] f_x;
    return integral;
}