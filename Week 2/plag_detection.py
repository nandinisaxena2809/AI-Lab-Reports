import heapq
import re

# ---------- Text Preprocessing ----------
def preprocess(text):
    # Split into sentences first, then clean
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    clean = []
    for s in sentences:
        s = s.lower()
        s = re.sub(r'[^\w\s]', '', s)  # remove punctuation
        clean.append(s)
    return clean

# ---------- Edit Distance (Levenshtein) ----------
def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1,
                           dp[i][j-1] + 1,
                           dp[i-1][j-1] + cost)
    return dp[m][n]

# ---------- Heuristic ----------
def heuristic(i, j, lenA, lenB):
    return abs((lenA - i) - (lenB - j))

# ---------- A* Search for Alignment ----------
def astar_align(docA, docB):
    lenA, lenB = len(docA), len(docB)
    start, goal = (0, 0), (lenA, lenB)

    open_set = [(0, start)]  # (fScore, node)
    gScore = {start: 0}
    cameFrom = {}

    while open_set:
        _, (i, j) = heapq.heappop(open_set)

        if (i, j) == goal:
            # reconstruct alignment
            alignment = []
            while (i, j) in cameFrom:
                prev = cameFrom[(i, j)]
                alignment.append((prev, (i, j)))
                i, j = prev
            return alignment[::-1]

        # neighbors: skip A, skip B, match both
        for ni, nj in [(i+1, j), (i, j+1), (i+1, j+1)]:
            if ni > lenA or nj > lenB:
                continue

            if i < lenA and j < lenB and ni == i+1 and nj == j+1:
                cost = edit_distance(docA[i], docB[j])
            else:
                cost = 1

            tentative_g = gScore[(i, j)] + cost
            if (ni, nj) not in gScore or tentative_g < gScore[(ni, nj)]:
                gScore[(ni, nj)] = tentative_g
                fScore = tentative_g + heuristic(ni, nj, lenA, lenB)
                cameFrom[(ni, nj)] = (i, j)
                heapq.heappush(open_set, (fScore, (ni, nj)))

    return None

# ---------- Plagiarism Detection ----------
def detect_plagiarism(text1, text2, threshold=3):
    docA, docB = preprocess(text1), preprocess(text2)
    alignment = astar_align(docA, docB)
    if not alignment:
        return []

    results = []
    for (i, j), (ni, nj) in alignment:
        if ni == i+1 and nj == j+1:  # matched pair
            dist = edit_distance(docA[i], docB[j])
            if dist <= threshold:
                results.append((docA[i], docB[j], dist))
    return results

# ---------- Test ----------
text1 = "The cat sat on the mat. It was sunny. The dog barked."
text2 = "The cat was on the mat. It was sunny today. The dog barked loudly."

print("Detected possible plagiarism:")
for a, b, dist in detect_plagiarism(text1, text2):
    print(f"DocA: '{a}'  <-->  DocB: '{b}'  (edit distance = {dist})")
