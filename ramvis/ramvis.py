import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy

import gym
from gym import wrappers

OUTDIR = './random-agent-results'


env = gym.make('Pong-ram-v0')
env = wrappers.Monitor(env, directory=OUTDIR, force=True)

np.random.seed(0)
'''
print("env.action_space")
print(env.action_space)
print("env.observation_space")
print(env.observation_space)
print("env.observation_space.high")
print(env.observation_space.high)
print("env.observation_space.low")
print(env.observation_space.low)
'''

total_frames = 0 
max_frames = 100

list_of_arrays = []
list_of_frames = []
for i_episode in range(1):
    observation = env.reset()
    for t in range(100):
        # env.render()
        # print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if (total_frames < max_frames):
            list_of_arrays.append(observation.reshape(16,8))
            list_of_frames.append(env.render(mode = 'rgb_array'))
            total_frames += 1
        if done: 
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()

sum_array = np.zeros((16, 8))

array_of_arrays = np.array(list_of_arrays)
mean_array = np.mean(array_of_arrays, axis=0)
mean_array_int = mean_array.astype(int)

difference_array_list = [abs(array - mean_array) for array in list_of_arrays]

fps = 2
duration = total_frames//fps
print("Duration: " + str(duration))

fig, axes = plt.subplots(1,2)

def plot_arrays(index):
    plt.title("Index: " + str(index))
    grid = difference_array_list[index]
    plt.subplot(1, 2, 1)
    plt.imshow(grid, interpolation='none', cmap='viridis')
    frame = list_of_frames[index]
    plt.subplot(1, 2, 2)
    plt.imshow(frame, interpolation='none', cmap='viridis')

def make_frame(t):
    index = int(t*fps)
    plot_arrays(index)
    return mplfig_to_npimage(fig)

animation =mpy.VideoClip(make_frame, duration=duration)
#animation.write_gif((OUTDIR + "/sinc_mpl.gif"), fps=fps)
animation.write_videofile((OUTDIR + "/sinc_mpl.mp4"), fps=fps)
