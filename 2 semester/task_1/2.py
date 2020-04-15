import numpy as np
import matplotlib.pyplot as plt

# Показатель адиабаты
gamma = 5 / 3
# Плотность газа слева и справа
ro_l = 13
ro_r = 1.3
# Давление слева и справа
p_l = 10e5
p_r = 1e5
# Скорости
u_l = 0
u_r = 0

# Ограничения
L = 10
T = 0.2

# Задаем сетку
c = np.sqrt(gamma * p_l / ro_r)
h = 0.1
tau = h / c
print(tau)
h_dim = int(2 * L / h + 1)
t_dim = int(T / tau + 1)
w = np.zeros((h_dim, t_dim, 3))
ans = np.zeros((h_dim, t_dim, 3))
x = np.linspace(-L, L, h_dim)
w[:int(h_dim / 2) + 1, 0] = [ro_l, 0, p_l / (gamma - 1)]
w[-int(h_dim / 2):, 0] = [ro_r, 0, p_r / (gamma - 1)]

for i_t in range(0, t_dim - 1):
    for i_h in range(1, h_dim - 1):
        # w = {ro, ro*u, ro*epsilon}
        ro = w[i_h, i_t, 0]
        u = w[i_h, i_t, 1] / ro
        epsilon = w[i_h, i_t, 2] / ro
        p = (gamma - 1) * ro * epsilon
        c = np.sqrt(gamma * p / ro)
        a = np.array([[0, 1, 0],
                      [-u ** 2, 2 * u, gamma - 1],
                      [-gamma * u * epsilon, gamma * epsilon, u]])
        omega_t = np.array([[-u * c, c, gamma - 1],
                            [-c ** 2, 0, gamma - 1],
                            [u * c, -c, gamma - 1]])
        abs_lambda = np.abs(np.array([[u + c, 0, 0],
                                      [0, u, 0],
                                      [0, 0, u - c]]))
        temp = 1 / 2 / c**2
        omega_t_inv = np.array([[temp, -2 * temp, temp],
                                [(u + c) * temp, - 2 * u * temp, (u - c) * temp],
                                [1 / 2 / (gamma - 1), 0, 1 / 2 / (gamma - 1)]])
        lambda_dash = omega_t_inv @ abs_lambda @ omega_t
        w[i_h, i_t + 1] = w[i_h, i_t] - \
            a @ (w[i_h + 1, i_t] - w[i_h - 1, i_t]) * tau / 2 / h + \
            lambda_dash @ (w[i_h + 1, i_t] - 2 * w[i_h, i_t] + w[i_h - 1, i_t]) * tau / 2 / h

    w[0, i_t + 1] = w[1, i_t + 1]
    w[h_dim - 1, i_t + 1] = w[h_dim - 2, i_t + 1]

fig, axs = plt.subplots(3)
f_1 = axs[0].plot(x, w[:, -1, 0])
f_2 = axs[1].plot(x, w[:, -1, 1])
f_3 = axs[2].plot(x, w[:, -1, 2])
axs[0].set_ylim(0, 14)
axs[1].set_ylim(0, 1500)
axs[2].set_ylim(0, 18e5)

for i in range(t_dim):
    f_1[0].set_ydata(w[:, i, 0])
    f_2[0].set_ydata(w[:, i, 1])
    f_3[0].set_ydata(w[:, i, 2])
    plt.pause(0.02)

plt.show()