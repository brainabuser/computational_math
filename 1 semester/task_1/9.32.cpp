#include <iostream>

using namespace std;

long double newtonCoeff(int *x, const int &begin, const int &end, int *f_x);

void printArray(long double *array, const int &size);

int main() {
    int years[10] = {1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000};
    int population[10] = {92'228'496, 106'021'537, 123'202'624, 132'164'569, 151'325'798,
                          179'323'175, 203'211'926, 226'545'805, 248'709'873, 281'421'906};
    long double coefficients[10];
    for (int i = 0; i < 10; ++i) {
        coefficients[i] = newtonCoeff(years, 0, i, population);
    }
    int ex_year = 2010;
    long double expected = 0.0;
    for (int i = 0; i < 10; ++i) {
        long double product = 1.0;
        for (int j = 0; j < i; ++j) {
            product *= (ex_year - years[j]);
        }
        expected += coefficients[i] * product;
    }
    cout << "Array of Newton`s polynom coefficients:" << endl;
    printArray(coefficients, 10);
    cout << "Expected population in 2010th year in the USA:" << endl;
    cout << "Approximately " << (long long)expected << " people" << endl;
    long double inclines[9];
    for (int i = 0; i < 9; ++i) {
        inclines[i] = (long double) (population[i + 1] - population[i]) / (years[i + 1] - years[i]);
    }
    cout << endl << "Array of spline coefficients(inclines):" << endl;
    printArray(inclines, 9);
    return 0;
}

long double newtonCoeff(int *x, const int &begin, const int &end, int *f_x) {
    return (end == begin) ? f_x[begin] : (newtonCoeff(x, begin, end - 1, f_x) - newtonCoeff(x, begin + 1, end, f_x)) /
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
