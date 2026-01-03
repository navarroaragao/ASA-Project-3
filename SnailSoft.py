#Copy from another submission 2

import sys
import pulp

sys.setrecursionlimit(5000)

SOLVER = pulp.PULP_CBC_CMD(msg=0, timeLimit=0.4, gapRel=0.01)

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    points = [0] * (n + 1)
    games_played = [[False] * (n + 1) for _ in range(n + 1)]
    
    for _ in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        r = int(next(iterator))
        
        games_played[u][v] = True
        
        if r == u:
            points[u] += 3
        elif r == v:
            points[v] += 3
        else:
            points[u] += 1
            points[v] += 1

    target_games_map = {i: [] for i in range(n + 1)}
    
    all_unplayed = []
    
    matches_remaining_count = [0] * (n + 1)

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j: continue
            if not games_played[i][j]:
                match = (i, j)
                all_unplayed.append(match)
                target_games_map[i].append(match)
                target_games_map[j].append(match)
                matches_remaining_count[i] += 1

    for team in range(1, n + 1):
        solve_team(n, team, points, target_games_map, all_unplayed, matches_remaining_count)

def solve_team(n, target_team, points, target_games_map, all_unplayed, matches_remaining_count):
    my_matches = target_games_map[target_team]
    num_my_matches = len(my_matches)
    
    left, right = 0, num_my_matches
    best_result = -1

    if not can_win(n, target_team, points, right, my_matches, all_unplayed, matches_remaining_count):
        print("-1")
        return

    while left <= right:
        mid = (left + right) // 2
        if can_win(n, target_team, points, mid, my_matches, all_unplayed, matches_remaining_count):
            best_result = mid
            right = mid - 1
        else:
            left = mid + 1
            
    print(best_result)

def can_win(n, target_team, points, num_wins, my_matches, all_unplayed, matches_remaining_count):
    target_final_score = points[target_team] + (num_wins * 3) + (len(my_matches) - num_wins)
    
    dangerous_teams = []
    dangerous_set = set()

    for i in range(1, n + 1):
        if i == target_team: continue
        
        if points[i] > target_final_score:
            return False
            
        max_possible_i = points[i] + (3 * matches_remaining_count[i])
        
        if max_possible_i > target_final_score:
            dangerous_teams.append(i)
            dangerous_set.add(i)
            
    if not dangerous_teams:
        return True

    prob = pulp.LpProblem("Check", pulp.LpMinimize)
    
    target_vars = {}
    for match in my_matches:
        y = pulp.LpVariable(f"y{match[0]}_{match[1]}", cat=pulp.LpBinary)
        d = pulp.LpVariable(f"d{match[0]}_{match[1]}", cat=pulp.LpBinary)
        target_vars[match] = (y, d)
        prob += y + d <= 1
        
    prob += pulp.lpSum([v[0] for v in target_vars.values()]) == num_wins
    
    other_vars = {}
    
    relevant_matches = []
    for u, v in all_unplayed:
        if u == target_team or v == target_team:
            continue
        if u in dangerous_set or v in dangerous_set:
            relevant_matches.append((u, v))
            
    for u, v in relevant_matches:
        x = pulp.LpVariable(f"x{u}_{v}", cat=pulp.LpBinary)
        e = pulp.LpVariable(f"e{u}_{v}", cat=pulp.LpBinary)
        other_vars[(u, v)] = (x, e)
        prob += x + e <= 1

    for team in dangerous_teams:
        terms = [points[team]]
        
        for u, v in my_matches:
            if u == team or v == team:
                y, d = target_vars[(u, v)]
                terms.append(3 - 3*y - 2*d)
        
        for u, v in relevant_matches:
            if (u, v) in other_vars:
                x, e = other_vars[(u, v)]
                if u == team:
                    terms.append(3*x + e)
                elif v == team:
                    terms.append(3 - 3*x - 2*e)
        
        prob += pulp.lpSum(terms) <= target_final_score

    prob += 0
    
    status = prob.solve(SOLVER)
    
    return status == pulp.LpStatusOptimal

if __name__ == "__main__":
    main()