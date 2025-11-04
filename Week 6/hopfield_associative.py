import numpy as np

def hebb_train(patterns):
    n_patterns, N = patterns.shape
    W = np.zeros((N, N))
    for p in range(n_patterns):
        W += np.outer(patterns[p], patterns[p])
    np.fill_diagonal(W, 0)
    W /= N
    return W

def recall(W, pattern, steps=2000):
    x = pattern.copy()
    N = len(x)
    for _ in range(steps):
        i = np.random.randint(N)
        h = W[i].dot(x)
        x[i] = 1 if h >= 0 else -1
    return x

# Example: store 5 random patterns of size 100
N = 100
patterns = np.random.choice([1, -1], size=(5, N))
W = hebb_train(patterns)

# Test recall for pattern 0 (with noise)
test = patterns[0].copy()
flip_idx = np.random.choice(N, size=10, replace=False)
test[flip_idx] *= -1
recalled = recall(W, test)
print("Original pattern (first 20 bits):")
print(patterns[0][:20])

print("\nNoisy input (first 20 bits):")
print(test[:20])

print("\nRecalled pattern (first 20 bits):")
print(recalled[:20])

# Check if it recalled correctly
matches = np.sum(patterns[0] == recalled)
print(f"\nNumber of matching bits: {matches}/100")
