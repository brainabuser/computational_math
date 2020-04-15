#include <iostream>

using namespace std;

long double newtonCoeff(long double *x, long double *f_x, const int &begin, const int &end);

void printArray(long double *array, const int &size);

void readArrays(long double *x, long double *y, const int &size);

int main() {
    long double x[10] = {1910.0, 1920.0, 1930.0, 1940.0, 1950.0, 1960.0, 1970.0, 1980.0, 1990.0, 2000.0};
    long double y[10] = {92'228'496, 106'021'537, 123'202'624, 132'164'569, 151'325'798,
                         179'323'175, 203'211'926, 226'545'805, 248'709'873, 281'421'906};
    int size = 10;
//    cout << "Enter the size of both x and y arrays:" << endl;
//    cin >> size;
//    cout << "Enter " << size << " pairs of values of x and y:" << endl;
//    readArrays(x, y, size);
    long double *coefficients = new long double[size];
    long double derivative = 0.0;
    for (int i = 0; i < size; ++i) {
        long double sum = 0.0;
        for (int j = 0; j < i; ++j) {
            long double temp = 1.0;
            for (int k = 0; k < j; ++k) {
                if (k != j) {
                    temp *= 1.0 - x[k];
                }
            }
            sum += temp;
        }
        coefficients[i] = newtonCoeff(x, y, 0, i);
        derivative += coefficients[i] * sum;
    }
    cout << "Array of Newton`s polynom coefficients:" << endl;
    printArray(coefficients, size);
    cout << "Required derivative value:" << endl;
    cout << derivative << endl;
    return 0;
}

void readArrays(long double *x, long double *y, const int &size) {
    for (int i = 0; i < size; ++i) {
        cin >> x[i] >> y[i];
    }
}

long double newtonCoeff(long double *x, long double *f_x, const int &begin, const int &end) {
    return (end == begin) ? f_x[begin] : (newtonCoeff(x, f_x, begin, end - 1) - newtonCoeff(x, f_x, begin + 1, end)) /
                                         (x[begin] - x[end]);
}

void printArray(long double *array, const int &size) {
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
