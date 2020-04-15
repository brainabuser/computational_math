#include <iostream>

#include <cmath>

using namespace std;

long double computeConstantValue(const long double &delta) {
    long const double result = M_E * delta / (2 * sqrt(36 - 5 * M_E));
    return result;
}

int main() {
    cout << "Enter \"n\" value" << endl;
    int N;
    cin >> N;
    cout << "Enter error value" << endl;
    long double delta;
    cin >> delta;
    const long double FIRST_CONSTANT = computeConstantValue(delta);
    const long double SECOND_CONSTANT = -FIRST_CONSTANT;
    auto *y = new long double[N];
    const long double q1 = 1 / M_E * (-6 + sqrt(36 - 5 * M_E));
    const long double q2 = 1 / M_E * (-6 - sqrt(36 - 5 * M_E));
    for (int i = 0; i < N; ++i) {
        y[i] = FIRST_CONSTANT * pow(q1, i);
        y[i] += SECOND_CONSTANT * pow(q2, i);
        y[i] += 1 / (M_E + 17) * sin(M_PI / 9);
    }
    cout << "q1 = " << q1 << endl;
    cout << "q2 = " << q2 << endl;
    for (int i = 0; i < N; ++i) {
        cout << "y[" << i << "] = " << y[i] << endl;
    }
    delete[] y;
    return 0;
}