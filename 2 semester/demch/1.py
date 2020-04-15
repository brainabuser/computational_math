import matplotlib.pyplot as plt
import numpy as np

A = -5
B = 2


# General solution constants
def C1():
    return A / 10 - B / 4


def C2():
    return A / 10 + B / 4


step = 1

while True:
    step /= 10
    x = np.arange(0, 1., step)

    size = x.size

    # Analytic functions
    y1 = 5. * C1() * np.exp(x) + 5. * C2() * np.exp(201 * x)
    y2 = -2. * C1() * np.exp(x) + 2. * C2() * np.exp(201 * x)

    # Grid functions
    f1 = np.empty(size)
    f2 = np.empty(size)

    f1[0] = A
    f2[0] = B

    prev = 1e-6

    for i in range(1, size):
        f1[i] = f1[i - 1] + step * (101 * f1[i - 1] + 250 * f2[i - 1])
        f2[i] = f2[i - 1] + step * (40 * f1[i - 1] + 101 * f2[i - 1])

        error = max(np.fabs((f2[i] - y2[i]) / y2[i]), np.fabs((f1[i] - y1[i]) / y1[i]), prev)
        prev = error

    print(error)

    if error < 1e-6:
        break

# Making plots
plt.plot(x, f1, 'o-r')
plt.plot(x, f2, 'o-b')

plt.legend(['f1 = f(x)', 'f2 = f(x)'])

plt.show()
