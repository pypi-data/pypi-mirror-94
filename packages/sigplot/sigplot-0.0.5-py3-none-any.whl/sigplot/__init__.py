import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from . import correlation
from . import sinusoids


def write_to_video(name, anim):
    write = animation.writers['ffmpeg']
    writer = write(fps=20, metadata=dict(artist='Me'), bitrate=15000)
    anim.save(name, writer=writer)


def fourier_series(fig, x, fs, interval, frames):
    t = np.linspace(0, int(len(x) / fs), len(x))
    xrange = abs(max(x) - min(x))
    maximum = max(x) + xrange / 2
    minimum = min(x) - xrange / 2
    plt.axes(xlim=(t[0], t[-1]), ylim=(minimum, maximum))
    plt.plot(t, x, linewidth=0.5, color='red')

    anime = sinusoids.draw(fig, t, x, fs, interval, frames)
    plt.show()
    return anime


def correlate(fig, a, x, fs):
    offset = np.zeros(len(a) + int(0.5 * fs))
    h = np.concatenate([offset, a, offset])
    t = np.linspace(0, 10, len(h))
    plt.axes(xlim=(t[0], t[-1]), ylim=(-10, 10))
    plt.plot(t, h)

    anime = correlation.draw(fig, t, h, x, (len(h) - len(x)))
    plt.show()
    return anime


def convolve(fig, a, x, fs):
    return correlate(fig, a, np.flip(x), fs)
