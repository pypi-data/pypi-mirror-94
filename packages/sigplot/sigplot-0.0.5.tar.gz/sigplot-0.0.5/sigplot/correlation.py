from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def draw(fig, t, h, x, frames):
    class Correlation:
        def __init__(self, ct, ch, cx):
            self.lines = [plt.plot([], [])[0] for _ in range(2)]
            for line in self.lines:
                line.set_data([], [])
            self.t = ct
            self.h = ch
            self.x = cx
            self.y = np.zeros(len(ct))

    def animate(i, corr):

        length = len(corr.t)

        r_len = length - i - len(corr.x)
        x_pad = np.concatenate([np.zeros(i), x, np.zeros(r_len)])

        if i == 0:
            corr.y = np.zeros(length)

        corr.lines[0].set_data(t, x_pad)
        corr.y[i] = np.sum(np.multiply(h, x_pad)) / 50
        corr.lines[1].set_data(t, corr.y)
        return corr.lines

    cor = Correlation(t, h, x)
    anim = FuncAnimation(fig,
                         animate,
                         fargs=[cor],
                         frames=frames,
                         interval=1,
                         blit=True)
    return anim
