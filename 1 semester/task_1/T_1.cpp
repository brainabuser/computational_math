#include <iostream>

#include <cmath>

using namespace std;

int main() {
    long double x = 1.0;
    long double y = x - (x * x + tan(x) * tan(x) - 1) / (2 * x + 1 / (cos(x) * cos(x)));
    long double delta = 0.000001;
    while (fabs(y - x) > delta) {
        x = y;
        y = x - (x * x + tan(x) * tan(x) - 1) / (2 * x + 1 / (cos(x) * cos(x)));;
    }
    cout << "First root: (" << y << ", " << tan(y) << ")" << endl;
    cout << "Second root: (" << -y << ", " << -tan(y) << ")" << endl;
    return 0;
}