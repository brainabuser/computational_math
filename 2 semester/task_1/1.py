import matplotlib.pyplot as plt

import numpy as np

import timeit


class ComputationalMethod:
    # Задание начальных данных в конструкторе абстрактного класса
    def __init__(self, h, cfl, t_end, h_end, h_start=0, t_start=0):
        self.t_start, self.t_end = t_start, t_end
        self.h = h
        self.time_stamps = [0, 5, 10, 15, 18]

        self.tau = cfl * h
        self.cfl = cfl
        self.timeArray = np.arange(t_start, t_end, self.tau)
        self.spaceArray = np.arange(h_start, h_end, self.h)
        self.solutionArray = np.zeros((self.timeArray.size, self.spaceArray.size))
        self.solution_stamps = []
        f = lambda x: np.sin(4 * np.pi * x / (h_end - h_start))
        self.solutionArray[0] = f(self.spaceArray)

        print('Объект класса ' + self.__class__.__name__ + ' создан.')

    def Solve(self):
        raise NotImplementedError

    def SetPlot(self, index):
        plt.plot(self.spaceArray, self.solutionArray[self.solution_stamps[index]],
                 label="T = " + str(self.time_stamps[index]))
        plt.tight_layout()
        plt.title('Метод ' + str(self.__class__.__name__) + '\nЧисло Куранта = '
                  + str(self.cfl))
        plt.xlabel('Пространство')
        plt.ylabel('Решение')
        plt.grid(True)


class ExplicitAngle(ComputationalMethod):
    def Solve(self):
        print('Начало рассчёта методом %s' % self.__class__.__name__)
        start = timeit.default_timer()

        self.solution_stamps = []
        self.solution_stamps.append(0)
        cnt = 1
        time_stamp = self.time_stamps[cnt]
        for t in range(self.timeArray.size - 1):
            for h in range(1, self.spaceArray.size):
                curr, prev = self.solutionArray[t][h], self.solutionArray[t][h - 1]
                self.solutionArray[t + 1][h] = self.GetNextStep(curr, prev)
            self.solutionArray[t + 1][0] = self.solutionArray[t + 1][-1]

            if self.timeArray[t + 1] >= time_stamp and cnt < 5:
                self.solution_stamps.append(t + 1)
                cnt = cnt + 1
                if cnt < 5:
                    time_stamp = self.time_stamps[cnt]

            if (t + 1) % (self.timeArray.size // 10) == 0:
                t = self.timeArray[t + 1]
                print('%.2f%% вычислений завершено' %
                      (100. * float(t) / (self.t_end - self.t_start)))

        self.solution_stamps.append(-1)
        elapsed_time = float(timeit.default_timer() - start)
        print('Время расчета: %.2e сек.' % elapsed_time)

    def GetNextStep(self, curr, prev):
        return curr - self.tau / self.h * (curr - prev)


class ExplicitLaxWendroff(ComputationalMethod):
    def GetNextStep(self, curr, prev, next):
        return curr - self.tau / (2 * self.h) \
               * (next - prev) + (self.tau / self.h) ** 2 / 2 \
               * (next - 2 * curr + prev)

    def Solve(self):
        print('Начало рассчёта методом %s' % self.__class__.__name__)
        start = timeit.default_timer()

        self.solution_stamps = []
        self.solution_stamps.append(0)
        cnt = 1
        time_stamp = self.time_stamps[cnt]
        for t in range(self.timeArray.size - 1):
            for h in range(1, self.spaceArray.size - 1):
                curr, prev = self.solutionArray[t][h], self.solutionArray[t][h - 1]
                next = self.solutionArray[t][h + 1]
                self.solutionArray[t + 1][h] = self.GetNextStep(curr, prev, next)

            self.solutionArray[t + 1][-1] = self.GetNextStep(
                self.solutionArray[t][-1],
                self.solutionArray[t][-2],
                self.solutionArray[t][0]
            )
            self.solutionArray[t + 1][0] = self.GetNextStep(
                self.solutionArray[t][0],
                self.solutionArray[t][-1],
                self.solutionArray[t][1]
            )

            if self.timeArray[t + 1] >= time_stamp and cnt < 5:
                self.solution_stamps.append(t + 1)
                cnt = cnt + 1
                if cnt < 5:
                    time_stamp = self.time_stamps[cnt]

            if (t + 1) % (self.timeArray.size // 10) == 0:
                t = self.timeArray[t + 1]
                print('%.2f%% вычислений завершено' %
                      (100. * float(t) / (self.t_end - self.t_start)))

        self.solution_stamps.append(-1)
        elapsed_time = float(timeit.default_timer() - start)
        print('Время расчета: %.2e сек.' % elapsed_time)


cmp_mtds = [ExplicitAngle, ExplicitLaxWendroff]

# Используем известные величины
h = 0.5
t_end = 18
h_end = 20

plotNum = 231
fig = plt.figure(figsize=(15, 7))

for m in cmp_mtds:
    for cfl in [0.6, 1, 1.01]:
        fig.add_subplot(plotNum)
        method = m(h=h, cfl=cfl, t_end=t_end, h_end=h_end)
        method.Solve()
        for i in range(len(method.solution_stamps)):
            method.SetPlot(i)
        plotNum = plotNum + 1
        plt.legend(loc='lower left')
plt.show()

#
# for m in cmp_mtds:
#     for cfl in [0.6, 1, 1.01]:
#         plt.figure(figsize=(11, 7))
#         plt.rc('font', size=20)
#         method = m(h=h, cfl=cfl, t_end=t_end, h_end=h_end)
#         method.Solve()
#         plt.title('Распределение по пр-ву, число Куранта = ' + str(cfl) + '\nМетод ' + method.__class__.__name__)
#         for i in range(len(method.solution_stamps)):
#             method.SetPlot(i)
#     plt.legend()
#     plt.show()
