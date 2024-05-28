# -*- coding: utf-8 -*-
"""
Created on Thu May  2 08:32:18 2024

@author: s2147128
"""

import numpy as np
import matplotlib.pyplot as plt
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
    min_fraction = min(counts.values()) / grid.size
    return min_fraction

# Parameters
N = 50  # Size of the grid
p1 = p2 = 0.5
p3_values = np.arange(0, 0.11, 0.01)
steady_state_steps = 500
measurement_steps = 100
results = []

for p3 in p3_values:
    grid = initialize_random_grid(N)
    for _ in range(steady_state_steps):
        update_random_grid(grid, p1, p2, p3)
    fractions = [measure_minority_fraction(grid) for _ in range(measurement_steps)]
    results.append((np.mean(fractions), np.var(fractions)))

means, variances = zip(*results)

# Plot the results
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(p3_values, means, marker='o')
plt.title('Mean Minority Phase Fraction')
plt.xlabel('$p_3$')
plt.ylabel('Mean Fraction')

plt.subplot(1, 2, 2)
plt.plot(p3_values, variances, marker='o')
plt.title('Variance of Minority Phase Fraction')
plt.xlabel('$p_3$')
plt.ylabel('Variance')

plt.tight_layout()
plt.show()
