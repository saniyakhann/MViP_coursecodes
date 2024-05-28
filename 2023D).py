# -*- coding: utf-8 -*-
"""
Created on Thu May  2 08:40:48 2024

@author: s2147128
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random

# Parameters
N = 50  # Size of the grid
p1 = 0.5  # Constant probability for p1
p2_values = np.linspace(0.01, 0.3, 15)  # Range and resolution for p2
p3_values = np.linspace(0.01, 0.3, 15)  # Range and resolution for p3
steady_state_steps = 500  # Steps to reach steady state
measurement_steps = 100  # Steps to measure the minority fraction

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
    for _ in range(N**2):  # Ensure every cell has a chance to update
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

def measure_minority_fraction(grid):
    counts = {'R': np.sum(grid == 'R'), 'P': np.sum(grid == 'P'), 'S': np.sum(grid == 'S')}
    return min(counts.values()) / grid.size

# Prepare to collect results
results = np.zeros((len(p2_values), len(p3_values)))

# Run simulation for each combination of p2 and p3
for i, p2 in enumerate(p2_values):
    for j, p3 in enumerate(p3_values):
        grid = initialize_random_grid(N)
        for _ in range(steady_state_steps):
            update_random_grid(grid, p1, p2, p3)
        fractions = [measure_minority_fraction(grid) for _ in range(measurement_steps)]
        results[i, j] = np.mean(fractions)

# Plot the results as a heatmap
plt.figure(figsize=(10, 8))
plt.imshow(results, cmap='viridis', interpolation='nearest', extent=[0.01, 0.3, 0.3, 0.01])
plt.colorbar(label='Average Fraction of Minority Phase')
plt.xlabel('$p_3$')
plt.ylabel('$p_2$')
plt.title('Heatmap of Minority Phase Fraction')
plt.gca().invert_yaxis()
plt.show()
