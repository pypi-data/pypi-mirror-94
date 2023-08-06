from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def draw(fig, t, x, fs, interval, frames):
    class FourierSeries:
        def __init__(self, ft, fx, ffs):
            self.lines, = (plt.plot([], [], lw=3))
            self.lines.set_data([], [])
            self.t = ft
            self.x = fx
            self.y = []
            self.fs = ffs

    def animate(i, args):
        cos = np.cos(2 * np.pi * i * args.t * args.fs / len(x))
        sin = np.sin(2 * np.pi * i * args.t * args.fs / len(x))
        a = np.sum(np.multiply(args.x, cos)) / (len(args.t))
        b = np.sum(np.multiply(args.x, sin)) / (len(args.t))
        if i == 0:
            args.y = a * np.ones(len(args.t))
        else:
            args.y = np.add(args.y, 2 * a * cos)
            args.y = np.add(args.y, 2 * b * sin)
        args.lines.set_data(t, args.y)
        return args.lines,

    fourier = FourierSeries(t, x, fs)
    anim = FuncAnimation(fig,
                         animate,
                         fargs=[fourier],
                         frames=frames,
                         interval=interval,
                         blit=True)
    return anim
