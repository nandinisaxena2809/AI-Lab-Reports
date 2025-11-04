import numpy as np

N = 8  # 8x8 chessboard
neurons = N * N

# ------------------------------
# Construct weight matrix
# ------------------------------
W = np.zeros((neurons, neurons))

# Apply row and column constraints
for i in range(N):
    for j in range(N):
        for k in range(N):
            for l in range(N):
                if (i, j) != (k, l):
                    idx1 = i * N + j
                    idx2 = k * N + l
                    if i == k or j == l:  # same row or same column
                        W[idx1, idx2] -= 2

# Bias encourages one rook per row/column
b = np.ones(neurons) * (N / 2)

# Initialize random binary pattern
x = np.random.choice([0, 1], size=neurons)

# ------------------------------
# Energy minimization
# ------------------------------
def energy(W, x, b):
    return -0.5 * x @ W @ x - b @ x

prev_energy = energy(W, x, b)
for epoch in range(5000):
    for i in range(neurons):
        h = W[i] @ x + b[i]
        x[i] = 1 if h > 0 else 0
    E = energy(W, x, b)
    if np.isclose(E, prev_energy, atol=1e-5):
        break
    prev_energy = E

# ------------------------------
# Postprocess: enforce one per row/column manually
# (Hopfield helps convergence close to this constraint)
# ------------------------------
board = x.reshape(N, N)
for i in range(N):
    # keep only the strongest activation in each row
    max_j = np.argmax(board[i])
    board[i] = np.zeros(N)
    board[i, max_j] = 1

# fix columns: one rook per column
for j in range(N):
    col_sum = board[:, j].sum()
    if col_sum == 0:
        # if column empty, fill next empty row
        empty_rows = [r for r in range(N) if board[r].sum() == 0]
        if empty_rows:
            board[empty_rows[0], j] = 1
    elif col_sum > 1:
        # keep only one rook (first)
        rows = np.where(board[:, j] == 1)[0]
        board[rows[1:], j] = 0

# ------------------------------
# Output
# ------------------------------
print("Eight-Rook Solution (1 = rook, 0 = empty):")
print(board.astype(int))
print("\nCheck row sums:", board.sum(axis=1))
print("Check column sums:", board.sum(axis=0))
