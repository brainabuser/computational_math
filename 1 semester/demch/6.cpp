#include <iostream>

#include <cmath>

using namespace std;

long double computef1(long double x, long double y);

int main() {
    cout << "Enter the value of error" << endl;
    long double error;
    cin >> error;
    long double step = 1.0;
    int size;
    do {
        size = (int) (2.9 / step);
        auto *y = new long double[size];
        auto *x = new long double[size];
        x[0] = 0.0;
        y[0] = 1.4142135623730951 + error;
        long double max_error = 0.0;
        for (int i = 1; i < size; ++i) {
            x[i] = x[i - 1] + step;
            y[i] = y[i - 1] +
                   step * computef1(x[i - 1] + step / 2.0, y[i - 1] + step / 2.0 * computef1(x[i - 1], y[i - 1]));
        }
        for (int i = 0; i < size; ++i) {
            max_error = max(fabsl(y[i] - 1.4142135623730951), max_error);
        }
        cout << endl << "partition_value = " << size << endl << "max_error = " << max_error << endl;
        delete[] x;
        delete[] y;
        step /= 2.0;
    } while (size < 20971520);
    return 0;
}

long double computef1(long double x, long double y) {
    return 10 * (y - 1.4142135623730951) / pow((x - 3.0), 2);
}