import matplotlib.pyplot as plt

import numpy as np

import timeit

from OOP import num_diff as nd


class LogisticRightHandSide:
    def __init__(self, alpha, r):
        self.alpha = alpha
        self.R = r

    def __call__(self, u):
        return self.alpha * u * (1 - u / self.R)


class ComputationalMethod:
    def __init__(self, f, init_val, num_blocks, t_start, t_end):
        self.f = f
        self.u0 = init_val
        self.numBlocks, self.numPoints = num_blocks, num_blocks + 1
        self.dt = (float(t_end) - float(t_start)) / self.numBlocks
        self.index = 0.

        self.solutionArray = np.zeros(self.numPoints)
        self.timeArray = np.linspace(t_start, t_end, self.numPoints)

        self.tStart, self.tEnd = float(t_start), float(t_end)

        print('Объект класса ' + self.__class__.__name__ + ' создан.')

    def Solve(self):
        print('Начало рассчёта методом %s' % self.__class__.__name__)
        start = timeit.default_timer()
        self.solutionArray[0] = self.u0

        for i in range(self.numBlocks):
            self.index = i
            u_old = self.solutionArray[i]
            self.solutionArray[i + 1] = self.GetNextStep(u_old)

            if (i + 1) % (self.numBlocks // 10) == 0:
                t = self.timeArray[i + 1]
                print('%.2f%% вычислений завершено' % (100. * float(t) / (self.tEnd - self.tStart)))

        elapsed_time = float(timeit.default_timer() - start)
        print('Время расчета: %.2e сек.' % elapsed_time)

    def GetNextStep(self, u_old):
        raise NotImplementedError

    def SetPlot(self):
        plt.plot(self.timeArray, self.solutionArray, '-o',
                 label=str(self.__class__.__name__))


class ExplicitEuler(ComputationalMethod):
    def GetNextStep(self, u_old):
        return u_old + self.dt * self.f(u_old)


class Heun(ComputationalMethod):
    def GetNextStep(self, u_old):
        f = self.f
        prev = u_old + self.dt * f(u_old)
        return u_old + self.dt / 2. * (f(u_old) + f(prev))


class RK4(ComputationalMethod):
    def GetNextStep(self, u_old):
        f, dt = self.f, self.dt
        k1 = f(u_old)
        k2 = f(u_old + dt / 2. * k1)
        k3 = f(u_old + dt / 2. * k2)
        k4 = f(u_old + dt * k3)
        return u_old + dt / 6. * (k1 + 2. * k2 + 2. * k3 + k4)


class ImplicitTrapezium(ComputationalMethod):
    def GetNextStep(self, u_old):
        return u_old + self.dt / 2. * \
               (self.f(u_old) + self.f(self.GetNext(u_old)))

    def GetNext(self, u_old):
        F = lambda x: x - self.solutionArray[self.index] \
                      - self.dt / 2. * \
                      (self.f(x) + self.f(self.solutionArray[self.index]))
        curr = prev = u_old
        error = 1.
        while error > 1e-3:
            der = nd.DerivativeNum3(F, h=1e-3)
            curr = prev - F(prev) / der(prev)
            prev = curr
            error = np.fabs(curr - prev)
        return curr


alpha = 0.2
R = 100.
numBlocks = 30
tStart = 0.
tEnd = 80.
initVal = 2.

func = LogisticRightHandSide(alpha, R)

cmp_mtds = [ExplicitEuler, Heun, RK4, ImplicitTrapezium]

plt.figure(figsize=(11, 7))
plt.rc('font', size=20)

for m in cmp_mtds:
    method = m(func, initVal, numBlocks, tStart, tEnd)
    method.Solve()
    method.SetPlot()

plt.grid(False)
plt.title('Динамика популяции')
plt.xlabel('Время')
plt.ylabel('Популяция')
plt.legend()
plt.show()
