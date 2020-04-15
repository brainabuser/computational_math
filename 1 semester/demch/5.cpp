#include <iostream>

#include <cmath>

using namespace std;

const long double error = 0.000001;

const long double B = M_PI / 2.0;

const long double A = 0.0;

long double trapezoid();

long double gaussian();

int main() {
    cout << "Trapezoid integral value is " << trapezoid() << endl;
    cout << "Gaussian integral value is " << gaussian() << endl;
    return 0;
}

long double computeFunction(const long double &point) {
    return cos(1000 * point) / (1.0 + pow(point, 3));
}

long double computeIntegral(const int &fineness) {
    long double step = M_PI / 2.0 / (fineness - 1);
    int size = fineness;
    auto *x = new long double[size];
    auto *f_x = new long double[size];
    x[0] = 0.0;
    f_x[0] = computeFunction(x[0]);
    for (int i = 1; i < size; ++i) {
        x[i] = x[i - 1] + step;
        f_x[i] = computeFunction(x[i]);
    }
    long double integral = step / 2.0 * (f_x[0] + f_x[size - 1]);
    for (int i = 1; i < size - 1; ++i) {
        integral += step * f_x[i];
    }
    delete[] x;
    delete[] f_x;
    return integral;
}

long double trapezoid() {
    int fineness = 2;
    long double error_value = (computeIntegral(2 * fineness) - computeIntegral(fineness)) / 3.0;
    while (fabsl(error_value) > error) {
        ++fineness;
        error_value = (computeIntegral(2 * fineness) - computeIntegral(fineness)) / 3.0;
    }
    return computeIntegral(fineness);
}

long double gaussianMember(const long double &left, const long double &right) {
    long double x[2] = {-0.7745967, 0.7745967};
    long double c[2] = {1, 1};
    long double r_coeff = (right - left) / 2.0;
    long double s_coeff = (right + left) / 2.0;
    long double member = 0.0;
    long double actual_node;
    for (int i = 0; i < 2; ++i) {
        actual_node = s_coeff + r_coeff * x[i];
        member += c[i] * computeFunction(actual_node);
    }
    return r_coeff * member;
}

long double gaussian() {
    long double integral = 0.0;
    for (int i = 0; i < 100; ++i) {
        long double a = A + i * (B - A) / 100.0;
        long double b = A + (i + 1) * (B - A) / 100.0;
        integral += gaussianMember(a, b);
    }
    return integral;
}