import random
import time

def generate_3_sat(m, n):
    """Generate a uniform random 3-SAT problem with m clauses and n variables."""
    clauses = []
    for _ in range(m):
        variables = random.sample(range(1, n + 1), 3)  # Select 3 distinct variables
        clause = []
        for var in variables:
            clause.append(var if random.choice([True, False]) else -var)
        clauses.append(clause)
    return clauses

def evaluate_solution(solution, clauses):
    """Evaluate a solution against the clauses."""
    score = 0
    for clause in clauses:
        if any((literal > 0 and solution[literal - 1]) or (literal < 0 and not solution[-literal - 1]) for literal in clause):
            score += 1
    return score

def hill_climbing(clauses, n, max_steps=1000):
    """Perform Hill Climbing to solve the 3-SAT problem."""
    solution = [random.choice([True, False]) for _ in range(n)]
    best_score = evaluate_solution(solution, clauses)

    for step in range(max_steps):
        for i in range(n):
            # Flip the variable
            solution[i] = not solution[i]
            score = evaluate_solution(solution, clauses)
            if score > best_score:
                best_score = score
                break
            # Flip back if not better
            solution[i] = not solution[i]

    return best_score == len(clauses), best_score

def beam_search(clauses, n, beam_width, max_steps=1000):
    """Perform Beam Search to solve the 3-SAT problem."""
    population = [[random.choice([True, False]) for _ in range(n)] for _ in range(beam_width)]
    for step in range(max_steps):
        scored_population = [(evaluate_solution(sol, clauses), sol) for sol in population]
        scored_population.sort(reverse=True, key=lambda x: x[0])
        population = [sol for _, sol in scored_population[:beam_width]]

        new_population = []
        for sol in population:
            for i in range(n):
                new_sol = sol[:]
                new_sol[i] = not new_sol[i]  # Flip the variable
                new_population.append(new_sol)
        
        # Keep the best new solutions
        scored_new_population = [(evaluate_solution(sol, clauses), sol) for sol in new_population]
        scored_new_population.sort(reverse=True, key=lambda x: x[0])
        population = [sol for _, sol in scored_new_population[:beam_width]]

        if any(evaluate_solution(sol, clauses) == len(clauses) for sol in population):
            return True, len(clauses)

    return False, max(evaluate_solution(sol, clauses) for sol in population)

def variable_neighborhood_descent(clauses, n, max_steps=1000):
    """Perform Variable Neighborhood Descent to solve the 3-SAT problem."""
    solution = [random.choice([True, False]) for _ in range(n)]
    best_score = evaluate_solution(solution, clauses)

    neighborhoods = [
        lambda s: [s[i] for i in range(len(s))],  # Identity neighborhood
        lambda s: [not s[i] for i in range(len(s))],  # Flip all
        lambda s: [not s[i] if i == random.randint(0, n-1) else s[i] for i in range(n)]  # Flip one random
    ]

    for step in range(max_steps):
        for neighborhood in neighborhoods:
            new_solution = neighborhood(solution)
            score = evaluate_solution(new_solution, clauses)
            if score > best_score:
                best_score = score
                solution = new_solution
                break

    return best_score == len(clauses), best_score

def main():
    # Parameters for 3-SAT generation
    m_values = [10, 20, 30]
    n_values = [10, 15, 20]
    beam_widths = [3, 4]
    results = []

    for m in m_values:
        for n in n_values:
            clauses = generate_3_sat(m, n)

            # Hill Climbing
            start_time = time.time()
            hc_success, hc_score = hill_climbing(clauses, n)
            hc_time = time.time() - start_time
            results.append(("Hill Climbing", m, n, hc_success, hc_score, hc_time))

            # Beam Search
            for beam_width in beam_widths:
                start_time = time.time()
                bs_success, bs_score = beam_search(clauses, n, beam_width)
                bs_time = time.time() - start_time
                results.append(("Beam Search", m, n, bs_success, bs_score, bs_time))

            # Variable Neighborhood Descent
            start_time = time.time()
            vnd_success, vnd_score = variable_neighborhood_descent(clauses, n)
            vnd_time = time.time() - start_time
            results.append(("Variable Neighborhood Descent", m, n, vnd_success, vnd_score, vnd_time))

    # Print results
    print("\nResults:")
    for method, m, n, success, score, elapsed_time in results:
        print(f"{method} | m: {m}, n: {n}, Success: {success}, Score: {score}, Time: {elapsed_time:.4f} seconds")

if __name__ == "__main__":
    main()