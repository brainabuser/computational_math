import matplotlib.pyplot as plt

import numpy as np

import timeit


class LogisticRightHandSide:
    def __init__(self, h, b_l, b_r, kappa):
        self.h, self.kappa = h, kappa
        num_points = int(1 / h) + 1
        self.A = np.zeros((num_points, num_points))
        flat_a = self.A.ravel()
        flat_a[1::num_points + 1] = 1
        flat_a[num_points::num_points + 1] = 1
        flat_a[::num_points + 1] = -2
        self.F = np.zeros(num_points)
        self.F[0] = b_l
        self.F[-1] = b_r

    def __call__(self, u):
        return self.kappa / self.h ** 2 * (np.dot(self.A, u) + self.F)


class ComputationalMethod:
    def __init__(self, f, h, tau, t_start, t_end):
        self.f, self.h_dim = f, int(1 / h) + 1
        self.t_dim = int((t_end - t_start) / tau) + 1
        self.dt = tau
        self.solutionArray = np.zeros((self.t_dim, self.h_dim))
        self.timeArray = np.linspace(t_start, t_end, self.t_dim)
        self.spaceArray = np.linspace(0, 1, self.h_dim)

        self.tStart, self.tEnd = float(t_start), float(t_end)

        print('Объект класса ' + self.__class__.__name__ + ' создан.')

    def Solve(self):
        print('Начало рассчёта методом %s' % self.__class__.__name__)
        start = timeit.default_timer()
        u0 = np.zeros(self.h_dim)
        for i in range(self.h_dim):
            if (self.spaceArray[i] >= 0.4) and (self.spaceArray[i] <= 0.6):
                u0[i] = 1.
        self.solutionArray[0] = u0

        for t in range(self.t_dim - 1):
            u_old = self.solutionArray[t]
            self.solutionArray[t + 1] = self.GetNextStep(u_old)

            if (t + 1) % ((self.t_dim - 1) // 10) == 0:
                t = self.timeArray[t + 1]
                print('%.2f%% вычислений завершено' % (100. * float(t) / (self.tEnd - self.tStart)))

        elapsed_time = float(timeit.default_timer() - start)
        print('Время расчета: %.2e сек.' % elapsed_time)

    def GetNextStep(self, u_old):
        raise NotImplementedError

    def SetPlot(self):
        print(self.solutionArray[-1])
        plt.plot(self.spaceArray, self.solutionArray[-1], '-o',
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


b_l = 0.
b_r = 0.
kappa = 0.1
h = 1. / 25
tau = h ** 2 / (200 * kappa)
tStart = 0.
tEnd = 0.04

func = LogisticRightHandSide(h, b_l, b_r, kappa)

cmp_mtds = [ExplicitEuler, Heun, RK4]

plt.figure(figsize=(11, 7))
plt.rc('font', size=20)

for m in cmp_mtds:
    method = m(func, h, tau, tStart, tEnd)
    method.Solve()
    method.SetPlot()

plt.grid(False)
plt.title('Динамика популяции')
plt.xlabel('Пространство')
plt.ylabel('Популяция')
plt.legend()
plt.show()
