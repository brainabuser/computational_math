from OOP import num_diff as snd

import numpy as np

import sympy as smp


class NSpace:
    def __init__(self, h, n_dim, left, right):
        self.h = h
        self.n_dim = n_dim
        self.points = np.arange(left, right, h)

    def get_norm(self, f):
        result = np.amax(abs(f(self.points)))
        obj = snd.DerivativeNum3(f, self.h)
        temp = np.amax(abs(obj(self.points)))
        for i in range(self.n_dim):
            result += temp
            temp = np.amax(abs(obj(temp)))
        return result

    def get_metrics(self, f1, f2):
        dif = lambda x: f1(x) - f2(x)
        return np.sqrt(self.get_norm(dif))


xSym = smp.Symbol('x')

functionsSym = [
    5 / (2 + 3 * xSym ** 2), 2 / (5 + smp.cos(xSym)),
    (3 + 4 * xSym ** 2) ** 1 / 3,
    2 / smp.sqrt(smp.pi) * smp.exp(-xSym ** 2)
]

functions = [smp.lambdify(xSym, f) for f in functionsSym]

h = 10e-3
a = 0.
b = 2.

# Подсчёт норм
spaces = [NSpace(h, i, a, b) for i in range(3)]

for s, i in zip(spaces, range(3)):
    for f, fs in zip(functions, functionsSym):
        print('Норма функции ' + str(fs) +
              ' в пространстве с' + str(i) +
              ' равна ' + str(s.get_norm(f))
              )

# Подсчёт расстояний между функциями

for s, i in zip(spaces, range(3)):
    j = 1
    for f, fs in zip(functions, functionsSym):
        for f1, fs1 in zip(functions[j:], functionsSym[j:]):
            res = s.get_metrics(f1, f)
            print('Расстояние между ' + str(fs) +
                  ' и ' + str(fs1) +
                  ' равно ' + str(res) +
                  ' в пространстве с' + str(i)
                  )
        j = j + 1
