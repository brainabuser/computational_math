#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

double getR_K_member(const double &x, const double &y, const double &z, const double &t);

double getR_K_member(const double &z, const double &t);

int main() {
    ofstream output(R"(D:\CLionsProjects\computational_math\task_2\T_4\Output.csv)");
    ofstream output0(R"(D:\CLionsProjects\computational_math\task_2\T_4\Output0.csv)");
    cout << "Enter the error value" << endl;
    double error;
    cin >> error;
    cout << "Enter the y`(0) = z(0) value" << endl;
    double z0;//Начальное значение пристрелочного параметра
    cin >> z0;
    double t = 0.001 / M_PI;//Шаг по 'x'
    cout << "t = " << t << endl;
    size_t size = M_PI / t + 1;
    vector<double> x(size), y(size), z(size);//Разностные схемы y, z
    x[0] = y[0] = 0.0;
    z[0] = z0;
    //Проводим 'пристрелку' для z0 и z0 + t(шаг)
    size_t x_size = x.size();
    for (size_t i = 0; i < x_size - 1; ++i) {
        x[i + 1] = x[i] + t;
        z[i + 1] = z[i] + getR_K_member(x[i], y[i], z[i], t);
        y[i + 1] = y[i] + getR_K_member(z[i], t);
    }
    for (size_t i = 0; i < x_size; ++i) {
        output0 << x[i] << ';' << y[i] << endl;
    }
    double needed_alpha;
    //Для z0 + t
    z[0] += t;
    double prev_last_elem = y[size - 1], last_elem, y1 = M_PI * M_PI;
    do {
        x_size = x.size();
        for (size_t i = 0; i < x_size - 1; ++i) {
            x[i + 1] = x[i] + t;
            z[i + 1] = z[i] + getR_K_member(x[i], y[i], z[i], t);
            y[i + 1] = y[i] + getR_K_member(z[i], t);
        }
        last_elem = y[size - 1];
        needed_alpha = z[0];
        cout << needed_alpha << endl;
        z[0] -= (prev_last_elem - y1) / (last_elem - prev_last_elem) * t;
        prev_last_elem = last_elem;
    } while (abs(last_elem - y1) > error);
    for (size_t i = 0; i < x_size; ++i)n {
        output << x[i] << ';' << y[i] << endl;
    }
    return 0;
}

double getF2(const double &x, const double &y, const double &z) {
    return (x * x - 2) * (y * cos(x) - z) + pow(M_E, x) * x * x * cos(x) + 2.0 * (1.0 + pow(x, 3) + pow(x, 2)) -
           pow(x, 4);
}

double getF1(const double &z) {
    return z;
}

double getR_K_member(const double &x, const double &y, const double &z, const double &t) {
    double result = 0.0;
    vector<double> bk(4);
    bk[0] = getF2(x, y, z);
    bk[1] = 2 * getF2(x + t / 2.0, y + t / 2.0 * bk[0], z);
    bk[2] = 2 * getF2(x + t / 2.0, y + t / 2.0 * bk[1], z);
    bk[3] = getF2(x + t, y + t * bk[2], z);
    size_t bk_size = bk.size();
    for (size_t j = 0; j < bk_size; ++j) {
        result += 1.0 / 6.0 * t * bk[j];
    }
    return result;
}

double getR_K_member(const double &z, const double &t) {
    double result = 0.0;
    vector<double> bk(4);
    bk[0] = getF1(z);
    bk[1] = 2 * getF1(z);
    bk[2] = 2 * getF1(z);
    bk[3] = getF1(z);
    size_t bk_size = bk.size();
    for (size_t j = 0; j < bk_size; ++j) {
        result += 1.0 / 6.0 * t * bk[j];
    }
    return result;
}