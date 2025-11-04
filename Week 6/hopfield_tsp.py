import numpy as np

n_cities = 10
A, B, C, D = 500, 500, 200, 500  
dt = 0.01                         # time step
steps = 5000                      # total iterations
tau = 1.0                         # time constant
gain = 0.5                        # sigmoid gain

# to generate city co-ordinates
np.random.seed(0)
cities = np.random.rand(n_cities, 2) * 100

# Distance matrix
dist = np.zeros((n_cities, n_cities))
for i in range(n_cities):
    for j in range(n_cities):
        dist[i, j] = np.linalg.norm(cities[i] - cities[j])

u = 0.5 * np.random.randn(n_cities, n_cities)
v = 1 / (1 + np.exp(-gain * u))

for t in range(steps):
    # Compute row and column sums
    row_sum = np.sum(v, axis=1)
    col_sum = np.sum(v, axis=0)

    # Compute update rule 
    du = (-A * (row_sum[:, None] - 1)
          - B * (col_sum[None, :] - 1)
          - C * np.sum(np.roll(v, -1, axis=1) + np.roll(v, 1, axis=1), axis=1)[:, None]
          - D * (dist @ np.roll(v, -1, axis=1))
          ) / tau

    u += du * dt
    v = 1 / (1 + np.exp(-gain * u))  # sigmoid activation

tour = np.argmax(v, axis=0)
tour = np.append(tour, tour[0])  # close the loop

tour_distance = 0
for i in range(n_cities):
    tour_distance += dist[tour[i], tour[i+1]]

print("TSP Hopfield Network Solution:")
print("Tour (city order):", tour)
print("Total tour distance:", round(tour_distance, 2))
print("\nTour matrix (1 = city visited at that step):")
tour_matrix = np.zeros_like(v)
for j in range(n_cities):
    tour_matrix[tour[j], j] = 1
print(tour_matrix.astype(int))
