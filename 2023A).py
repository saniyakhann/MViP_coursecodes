# -*- coding: utf-8 -*-
"""
Created on Thu May  2 08:22:00 2024

@author: s2147128
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation

def initialize_grid(N):
    grid = np.zeros((N, N), dtype=int)  # Use integers instead of strings
    for i in range(N):
        for j in range(N):
            angle = np.arctan2(i - N / 2, j - N / 2) + np.pi
            if 0 <= angle < 2 * np.pi / 3:
                grid[i, j] = 0  # 'R' -> 0
            elif 2 * np.pi / 3 <= angle < 4 * np.pi / 3:
                grid[i, j] = 1  # 'P' -> 1
            else:
                grid[i, j] = 2  # 'S' -> 2
    return grid

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

def update_grid(grid):
    N = len(grid)
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            if grid[i, j] == 0 and count_neighbors(grid, i, j, 1) >= 3:
                new_grid[i, j] = 1  # Rock to Paper
            elif grid[i, j] == 1 and count_neighbors(grid, i, j, 2) >= 3:
                new_grid[i, j] = 2  # Paper to Scissors
            elif grid[i, j] == 2 and count_neighbors(grid, i, j, 0) >= 3:
                new_grid[i, j] = 0  # Scissors to Rock
    return new_grid

def plot_grid(grid):
    cmap = ListedColormap(['red', 'blue', 'green'])
    plt.imshow(grid, cmap=cmap)
    plt.colorbar()

N = 60  # Size of the grid
grid = initialize_grid(N)

# Plot initial state
plt.figure(figsize=(6, 6))
plot_grid(grid)
plt.show()

# Update the grid
fig, ax = plt.subplots()
cmap = ListedColormap(['red', 'blue', 'green'])

def animate(frame):
    global grid
    grid = update_grid(grid)
    ax.clear()
    ax.imshow(grid, cmap=cmap)
    ax.set_title(f"Step {frame + 1}")

ani = animation.FuncAnimation(fig, animate, frames=100, interval=200)
plt.show()

