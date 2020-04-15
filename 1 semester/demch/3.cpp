#include <iostream>

#include <cmath>

using namespace std;

const long double error = 0.000001;

int main() {
    long double x1;
    cout << "Enter initial approximation value:" << endl;
    cin >> x1;
    cout << "Function value at " << x1 << ":" << endl;
    cout << (atan(pow(M_E, x1)) - M_PI / 4) << endl;
    cout << "Second derivative value at " << x1 << ":" << endl;
    cout << ((pow(M_E, x1) - (pow(M_E, 3 * x1))) / pow((pow(M_E, 2 * x1) + 1.0), 2)) << endl;
    long double x2 = x1 - (atan(pow(M_E, x1)) - M_PI / 4) * (pow(M_E, x1) + pow(M_E, -x1));
    while (fabs(x2 - x1) > error) {
        long double temp = x2;
        x2 = temp - (atan(pow(M_E, temp)) - M_PI / 4) * (pow(M_E, temp) + pow(M_E, -temp));
        x1 = temp;
    }
    cout << "The root of the \"arctg(e^x) - pi/4 = 0\" is " << x2 << endl;
    return 0;
}
