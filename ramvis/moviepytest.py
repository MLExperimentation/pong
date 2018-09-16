import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy

duration = 2
fps = 2
total_frames = duration*fps

np.random.seed(0)

fig, axes = plt.subplots()

def generate_random_array():
    grid = np.random.rand(4, 4)
    plt.imshow(grid, interpolation='none', cmap='viridis')

def make_frame(t):
    generate_random_array()
    plt.title("Time: " + str(t))
    return mplfig_to_npimage(fig)

animation =mpy.VideoClip(make_frame, duration=duration)
animation.write_gif("sinc_mpl.gif", fps=fps)

