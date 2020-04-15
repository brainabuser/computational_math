#include <iostream>

#include <cmath>

using namespace std;

long double fact(int number);

long double power(const long double &a, const int &n);

long double sin_member(const int degree, const long double &point);

long double exp_member(const int degree, const long double &point);


int main() {
    long double m;
    long double point;
    cout << "Enter point value:" << endl;
    cin >> point;
    int i = -1;
    do {
        ++i;
        m = sin_member(i, point);
    } while (m >= 0.001);
    cout << "\"N\" value for sin, point with the value of " << point << " is " << i << endl;
    i = -1;
    do {
        ++i;
        m = exp_member(i, point);
    } while (m >= 0.001);
    cout << "\"N\" value for exp, point with the value of " << point << " is " << i << endl;
    return 0;
}

long double fact(int number) {
    return (number <= 1) ? 1 : number * fact(number - 1);
}

long double power(const long double &a, const int &n) {
    if (n == 1) {
        return a;
    } else if (n == 0) {
        return 1;
    }
    return (n % 2 == 0) ? power(a, n / 2) * power(a, n / 2) : a * power(a, n - 1);
}

long double sin_member(const int degree, const long double &point) {
    return power(point, 2 * degree + 1) / fact(2 * degree + 1);
}

long double exp_member(const int degree, const long double &point) {
    return power(point, degree) / fact(degree) * exp(point);
}