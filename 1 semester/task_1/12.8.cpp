#include <iostream>
#include <cmath>

using namespace std;

long double find_original_f_root(const long double &point, const long double &delta);

long double find_reverse_f_root(const long double &point, const long double &delta);

int main() {
    long double x_0;
    const long double delta = 0.001;
    cout << "Enter x_0 value:" << endl;
    cin >> x_0;
    //Ищем левый корень
    long double left_root = find_original_f_root(x_0, delta);
    //Ищем правый корень
    long double right_root = find_reverse_f_root(x_0, delta);
    cout << "Left root is " << left_root << endl;
    cout << "Right root is " << right_root << endl;
    long double f_width = right_root - left_root;
    cout << "The \"width\" of function is " << f_width << endl;
    return 0;
}


long double find_original_f_root(const long double &point, const long double &delta) {
    long double prev, next;
    next = point;
    do {
        prev = next;
        //Реккурентная формула для исходной функции
        next = pow(2.0, -3.0 / 2) * exp(pow(prev, 2.0) - 1.0 / 2);
    } while (fabs(next - prev) >= delta);
    return next;
}

long double find_reverse_f_root(const long double &point, const long double &delta) {
    long double prev, next;
    next = point;
    do {
        prev = next;
        //Реккурентная формула для обратной функции
        next = sqrt(log(pow(2.0, 3.0 / 2) * pow(M_E, 1.0 / 2) * prev));
    } while (fabs(next - prev) >= delta);
    return next;
}