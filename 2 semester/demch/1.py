import numpy as np

import csv

A = -5.
B = 2.


# General solution constants
def get_c1():
    return A / 10 - B / 4


def get_c2():
    return A / 10 + B / 4


print('Type required node amount')
n = int(input())

# Set up grid
x = np.linspace(0., 1., n + 1)

size = x.size

# Grid functions
f1 = np.empty(size)
f2 = np.empty(size)

f1[0] = A
f2[0] = B

step = 1. / n
for i in range(1, size):
    f1[i] = f1[i - 1] + step * (101 * f1[i - 1] + 250 * f2[i - 1])
    f2[i] = f2[i - 1] + step * (40 * f1[i - 1] + 101 * f2[i - 1])

# Node values
nodes = np.linspace(0., 1., 11)

# Analytical functions
y1 = 5. * get_c1() * np.exp(nodes) + 5. * get_c2() * np.exp(201 * nodes)
y2 = -2. * get_c1() * np.exp(nodes) + 2. * get_c2() * np.exp(201 * nodes)

nodes_indexes = int(n / 10)

ones = np.fabs((f1[::nodes_indexes] - y1))
twos = np.fabs((f2[::nodes_indexes] - y2))

absolute_errors = [max(one, two) for one, two in zip(ones, twos)]

ones /= y1
twos /= y2

relative_errors = [max(one, two) for one, two in zip(ones, twos)]

with open('1.csv', mode='w') as file:
    names = ['x', 'y1(x)',
             'y2(x)', 'y1[x]',
             'y2[x]', 'a_error',
             'r_error'
             ]
    writer = csv.writer(file, delimiter=',')
    writer.writerow(names)
    for i in range(11):
        writer.writerow(np.array([nodes[i], y1[i], y2[i],
                                  f1[i], f2[i],
                                  absolute_errors[i],
                                  relative_errors[i]]
                                 ).round(4))
