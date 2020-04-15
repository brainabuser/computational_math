import sympy as smp

import matplotlib.pyplot as plt

import math as m


class Derivative:
    def __init__(self, f, h, list):
        self.args = []
        self.f = f
        self.h = h
        self.coeffs = list

    def SetCoeffs(self, list):
        self.coeffs = list

    def __call__(self, x):
        if len(self.args) == 0:
            raise NotImplementedError
        f, h = self.f, self.h
        coeffs = self.coeffs
        args = self.args
        result = 0
        for coeff, args in zip(coeffs, args):
            result += coeff * f(x + h * args)
        return result / h


class DerivativeNum1(Derivative):
    def __init__(self, f, h):
        super().__init__(f, h, [1, -1])
        self.args = [1, 0]


class DerivativeNum2(Derivative):
    def __init__(self, f, h):
        super().__init__(f, h, [1, -1])
        self.args = [0, -1]


class DerivativeNum3(Derivative):
    def __init__(self, f, h):
        super().__init__(f, h, [1 / 2, -1 / 2])
        self.args = [1, -1]


class DerivativeNum4(Derivative):
    def __init__(self, f, h):
        super().__init__(f, h, [4 / 6, -4 / 6, -1 / 12, 1 / 12])
        self.args = [1, -1, 2, -2]


class DerivativeNum5(Derivative):
    def __init__(self, f, h):
        super().__init__(f, h, [3 / 4, -3 / 4, -3 / 20, 3 / 20, 1 / 60, -1 / 60])
        self.args = [1, -1, 2, -2, 3, -3]


if __name__ == '__main__':
    xSym = smp.Symbol('x')

    functionsSym = [
        smp.sin(xSym ** 2), smp.cos(smp.sin(xSym)),
        smp.exp(smp.cos(smp.sin(xSym))), smp.ln(xSym + 3),
        smp.sqrt(xSym + 3)
    ]

    functions = [smp.lambdify(xSym, f) for f in functionsSym]

    x0 = 5

    derivativesAnalyticalSym = [smp.diff(f, xSym) for f in functionsSym]

    # Анализ сходимости формул численного дифф.
    derivativesAnalytical = [smp.lambdify(xSym, f) \
                             for f in derivativesAnalyticalSym]

    derivativesNumerical = [
        DerivativeNum1,
        DerivativeNum2,
        DerivativeNum3,
        DerivativeNum4,
        DerivativeNum5
    ]

    steps = [2 ** (-n) for n in range(0, 21)]

    for i in range(4):
        plt.figure(i, figsize=(13, 6.7))
        for f, derivativeAnalytical in zip(functions, derivativesAnalytical):
            errors = []
            for h in steps:
                derivative = derivativesNumerical[i](f, h)
                error = m.fabs(derivative(x0) - derivativeAnalytical(x0))
                errors.append(error)
            plt.title('Анализ сходимости ' + derivativesNumerical[i].__name__)
            plt.xlabel('Шаг сетки')
            plt.ylabel('Погрешность')
            plt.loglog(steps, errors, '-o', linewidth=4, markersize=10)
    plt.show()
