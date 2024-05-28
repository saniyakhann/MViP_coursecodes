# -*- coding: utf-8 -*-
"""
Created on Thu May  2 08:24:43 2024

@author: s2147128
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import random

def initialize_random_grid(N):
    states = ['R', 'P', 'S']
    return np.random.choice(states, (N, N))

def count_neighbors(grid, i, j, state):
    count = 0
    N = len(grid)
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = (i + di) % N, (j + dj) % N
            if grid[ni, nj] == state:
                count += 1
    return count

def update_random_grid(grid, p1, p2, p3):
    N = len(grid)
    # Choose a random cell to update
    i, j = np.random.randint(N), np.random.randint(N)
    if grid[i, j] == 'R' and count_neighbors(grid, i, j, 'P') >= 1:
        if random.random() < p1:
            grid[i, j] = 'P'
    elif grid[i, j] == 'P' and count_neighbors(grid, i, j, 'S') >= 1:
        if random.random() < p2:
            grid[i, j] = 'S'
    elif grid[i, j] == 'S' and count_neighbors(grid, i, j, 'R') >= 1:
        if random.random() < p3:
            grid[i, j] = 'R'

def plot_grid(grid):
    cmap = ListedColormap(['red', 'blue', 'green'])
    plt.imshow(grid, cmap=cmap)
    plt.colorbar()

# Parameters
N = 60  # Size of the grid
p1, p2, p3 = 0.3, 0.3, 0.3  # Probabilities of state changes
grid = initialize_random_grid(N)

# Animation
fig, ax = plt.subplots()
cmap = ListedColormap(['red', 'blue', 'green'])

def animate(frame):
    update_random_grid(grid, p1, p2, p3)
    ax.clear()
    ax.imshow(grid, cmap=cmap)
    ax.set_title(f"Step {frame + 1}")

ani = animation.FuncAnimation(fig, animate, frames=300, interval=100)
plt.show()
