import sympy as smp
import numpy as np
import matplotlib.pyplot as plt
import math as m


class AntiDerivative:
    def __init__(self, f, left, num):
        self.f = f
        self.leftBorder = left
        self.numBlocks = num
        self.coeffs = []
        self.grid = []
        self.h = None

    def SetCoeffs(self):
        raise NotImplementedError

    def SetGrid(self, right_border):
        raise NotImplementedError

    def __call__(self, x):
        self.SetCoeffs()
        self.SetGrid(x)
        funcs = [self.f(point) for point in self.grid]
        return self.h * np.dot(self.coeffs, funcs)


class AntiDerivativeNum1(AntiDerivative):
    def SetCoeffs(self):
        self.coeffs = np.ones(self.numBlocks + 1)

    def SetGrid(self, right_border):
        self.h = (right_border - self.leftBorder) / self.numBlocks
        self.grid = np.linspace(self.leftBorder + self.h, right_border,
                                self.numBlocks + 1)


class AntiDerivativeNum2(AntiDerivative):
    def SetCoeffs(self):
        self.coeffs = np.ones(self.numBlocks + 1)

    def SetGrid(self, right_border):
        self.h = (right_border - self.leftBorder) / self.numBlocks
        self.grid = np.linspace(self.leftBorder, right_border,
                                self.numBlocks + 1)


class AntiDerivativeNum3(AntiDerivative):
    def SetCoeffs(self):
        self.coeffs = np.ones(self.numBlocks + 1)

    def SetGrid(self, right_border):
        self.h = (right_border - self.leftBorder) / self.numBlocks
        self.grid = np.linspace(self.leftBorder + self.h / 2, right_border,
                                self.numBlocks + 1)


class AntiDerivativeNum4(AntiDerivative):
    def SetCoeffs(self):
        self.coeffs = np.ones(self.numBlocks + 1)
        self.coeffs[0] = 1. / 2
        self.coeffs[-1] = 1. / 2

    def SetGrid(self, right_border):
        self.h = (right_border - self.leftBorder) / self.numBlocks
        self.grid = np.linspace(self.leftBorder, right_border,
                                self.numBlocks + 1)


class AntiDerivativeNum5(AntiDerivativeNum1):
    def SetCoeffs(self):
        if self.numBlocks % 2 != 0:
            self.numBlocks -= 1
        self.coeffs = 1. / 3 * np.ones(self.numBlocks + 1)
        for index in range(1, -1):
            if index % 2 == 0:
                self.coeffs[index] *= 4.
            else:
                self.coeffs[index] *= 2.

    def SetGrid(self, right_border):
        self.h = (right_border - self.leftBorder) / self.numBlocks
        self.grid = np.linspace(self.leftBorder, right_border,
                                self.numBlocks + 1)


# Пределы интегрирования
a = 0.
b = 2.

xSym = smp.Symbol('x')

functionsSym = [
    smp.sin(xSym ** 2), smp.cos(smp.sin(xSym)),
    smp.exp(smp.cos(smp.sin(xSym))), smp.ln(xSym + 3),
    smp.sqrt(xSym + 3)
]

functions = [smp.lambdify(xSym, f) for f in functionsSym]

integralsAnalyticalSym = [smp.integrate(fSym, (xSym, a, b)) for fSym in functionsSym]

# Анализ сходимости формул численного интегрирования
integralsAnalytical = [float(i) for i in integralsAnalyticalSym]

integralsNumerical = [
    AntiDerivativeNum1,
    AntiDerivativeNum2,
    AntiDerivativeNum3,
    AntiDerivativeNum4,
    AntiDerivativeNum5
]

steps = [2 ** n for n in range(1, 15)]

for i in range(4):
    plt.figure(i, figsize=(13, 6.7))
    for f, integralAnalytical in zip(functions, integralsAnalytical):
        errors = []
        for s in steps:
            integral = integralsNumerical[i](f, a, s)
            error = m.fabs(integral(b) - integralAnalytical)
            errors.append(error)
        plt.title('Анализ сходимости ' + integralsNumerical[i].__name__)
        plt.xlabel('Шаг сетки')
        plt.ylabel('Погрешность')
        plt.loglog(steps, errors, '-o', linewidth=4, markersize=10)
plt.show()
