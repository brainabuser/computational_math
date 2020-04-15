#include <iostream>

#include <vector>

#include <cmath>

using namespace std;

const long double a5 = -1000030000.2;
const long double a4 = -999999.9998;
const long double a3 = -1000029000.17;
const long double a2 = -999998.9998;
const long double a1 = 1000.03;
const long double a0 = 1.0;

long double alpha = fabs(a5) / (fabs(a5) + fabs(a3));
long double beta = 1.0 + fabs(a5) / fabs(a0);

vector<long double> f_coefficients = {a0, a1, a2, a3, a4, a5};

long double compute_polynom_value(const vector<long double> &v, const long double &point);

int get_roots_number(const vector<long double> &v);

bool is_opposite_sign(const long double &begin, const long double &end);;

void print_vector(const vector<long double> &v);

int main() {
    cout << "alpha = " << alpha << endl;
    cout << "beta = " << beta << endl;
    //Метод Декарта:
    cout << "The method of Descartes:" << endl;
    print_vector(f_coefficients);
    int number_of_roots = get_roots_number(f_coefficients);
    cout << number_of_roots << endl;
    //Метод Бюдана-Фурье
    //Вычисляем значения производных по 5 порядка включительно
    vector<long double> f1_coefficients = {5 * a0, 4 * a1, 3 * a2, 2 * a3, a4};
    vector<long double> f2_coefficients = {20 * a0, 12 * a1, 6 * a2, 2 * a3};
    vector<long double> f3_coefficients = {60 * a0, 24 * a1, 6 * a2};
    vector<long double> f4_coefficients = {120 * a0, 24 * a1};
    vector<long double> f5_coefficients = {120 * a0};
    //Заполняем массив производных
    vector<vector<long double>> derivatives = {
            f_coefficients,
            f1_coefficients,
            f2_coefficients,
            f3_coefficients,
            f4_coefficients,
            f5_coefficients
    };
    //Создаем и заполняем массивы значений производных в конечных точках
    vector<long double> alpha_values;
    vector<long double> beta_values;
    for (size_t i = 0; i < derivatives.size(); ++i) {
        alpha_values.push_back(compute_polynom_value(derivatives.at(i), alpha));
        beta_values.push_back(compute_polynom_value(derivatives.at(i), beta));
    }
    cout << "The method of Budan-Fourier:" << endl;
    print_vector(alpha_values);
    print_vector(beta_values);
    //Получаем количество корней из формулировки теоремы
    number_of_roots = get_roots_number(alpha_values) - get_roots_number(beta_values);
    cout << number_of_roots << endl;
    //Теорема Штурма
    vector<long double> alpha_values1 = {
            -1250662438.0290627,
            -1001778999.8561493,
            -38921877641.09132,
            1021458423.17013,
            -980523631.13702,
            -204134490.45198238
    };
    vector<long double> beta_values1 = {
            1.000151015150004e+45,
            5.0006040514797356e+36,
            5.600600844628423e+32,
            2.0409681572152153e+24,
            -979951345711750.8,
            -204134490.45198238
    };
    cout << "The method of Sturm:" << endl;
    print_vector(alpha_values1);
    print_vector(beta_values1);
    number_of_roots = get_roots_number(alpha_values1) - get_roots_number(beta_values1);
    cout << number_of_roots << endl;
    //Поиск минимального отрезка существования корней
    cout << "Enter the value of the fineness:" << endl;
    long double f;
    cin >> f;
    const long double step = (beta - alpha) / f;
    long double interval_begin = alpha;
    //
    long double interval_middle = (alpha + beta) / 2;
    long double interval_end = beta;
    while (interval_end - interval_begin > step) {
        if (!is_opposite_sign(compute_polynom_value(f_coefficients, interval_begin),
                              compute_polynom_value(f_coefficients, interval_middle))) {
            interval_begin = interval_middle;
        } else {
            interval_end = interval_middle;
        }
        interval_middle = (interval_begin + interval_end) / 2;
    }
    cout << "Interval of the existence of the root:" << endl << "[" << interval_begin << ", " << interval_end << "]"
         << endl;
    cout << compute_polynom_value(f_coefficients, interval_middle) << endl;
    return 0;
}

long double compute_polynom_value(const vector<long double> &v, const long double &point) {
    long double value = 0.0;
    for (size_t i = 0; i < v.size(); ++i) {
        value += v.at(i) * pow(point, v.size() - i);
    }
    return value;
}

int get_roots_number(const vector<long double> &v) {
    int result = 0;
    long double prev = v.at(0);
    for (size_t i = 1; i < v.size(); ++i) {
        if ((prev > 0.0 && v.at(i) < 0.0) || (prev < 0.0 && v.at(i) > 0.0)) {
            ++result;
            prev = v.at(i);
        }
    }
    return result;
}

bool is_opposite_sign(const long double &begin, const long double &end) {
    return ((begin >= 0.0 && end <= 0.0) || (begin <= 0.0 && end >= 0.0));
}

void print_vector(const vector<long double> &v) {
    cout << "[";
    bool first = true;
    for (const auto &item : v) {
        if (first) {
            cout << item;
            first = false;
        } else {
            cout << ", " << item;
        }
    }
    cout << "]" << endl;
}