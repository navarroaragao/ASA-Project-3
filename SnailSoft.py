import sys
from pulp import *

sys.setrecursionlimit(5000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n_teams = int(next(iterator))
        n_played = int(next(iterator))
    except StopIteration:
        return

    current_points = [0] * n_teams
    remaining_counts = [[2 if i != j else 0 for j in range(n_teams)] for i in range(n_teams)]

    for _ in range(n_played):
        u = int(next(iterator)) - 1
        v = int(next(iterator)) - 1
        winner = int(next(iterator))
        
        if remaining_counts[u][v] > 0:
            remaining_counts[u][v] -= 1
            remaining_counts[v][u] -= 1
        
        if winner == 0:
            current_points[u] += 1
            current_points[v] += 1
        elif winner == (u + 1):
            current_points[u] += 3
        else:
            current_points[v] += 3

    all_binary_matches = []

    for i in range(n_teams):
        for j in range(i + 1, n_teams):
            num_games = remaining_counts[i][j]
            if num_games > 0:
                for k in range(num_games):
                    w_i = LpVariable(f"bin_win_{i}_{j}_{k}", 0, 1, LpBinary)
                    w_j = LpVariable(f"bin_win_{j}_{i}_{k}", 0, 1, LpBinary)
                    
                    all_binary_matches.append((i, j, w_i, w_j))

    max_potential = list(current_points)
    for i in range(n_teams):
        for j in range(n_teams):
            if i != j:
                max_potential[i] += 3 * remaining_counts[i][j]

    solver = PULP_CBC_CMD(msg=0)

    for k in range(n_teams):
        impossible = False
        k_max_points = max_potential[k]
        for other in range(n_teams):
            if k != other and current_points[other] > k_max_points:
                print("-1")
                impossible = True
                break
        if impossible:
            continue

        prob = LpProblem(f"BinaryTeam_{k}", LpMinimize)
        
        team_exprs = [current_points[i] for i in range(n_teams)]
        
        k_wins_list = []

        for (i, j, w_i, w_j) in all_binary_matches:
            prob += (w_i + w_j <= 1)
            
            team_exprs[i] += 2 * w_i
            team_exprs[i] += -1 * w_j
            team_exprs[i] += 1
            
            team_exprs[j] += 2 * w_j
            team_exprs[j] += -1 * w_i
            team_exprs[j] += 1 

            if i == k:
                k_wins_list.append(w_i)
            elif j == k:
                k_wins_list.append(w_j)

        prob += lpSum(k_wins_list)

        expr_k = team_exprs[k]
        for other in range(n_teams):
            if k == other: continue
            prob += (expr_k >= team_exprs[other])

        status = prob.solve(solver)

        if status == LpStatusOptimal:
            obj_value = value(prob.objective)
            print(int(obj_value) if obj_value is not None else 0)
        else:
            print("-1")

if __name__ == "__main__":
    solve()