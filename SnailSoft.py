import pulp

def main():

    n, m = map(int, input().split()) 
    
    points = [0] * (n + 1) 
    
    games = [[False] * (n + 1) for _ in range(n + 1)]
    
    for _ in range(m):
        i, j, results = map(int, input().split())

        games[i][j] = True
        
        if results == i:  
            points[i] += 3
        elif results == j:  
            points[j] += 3
        else:  
            points[i] += 1
            points[j] += 1
    
    for team in range(1, n + 1):
        min_wins = calculate_min_wins(n, team, points, games)
        print(min_wins)

def calculate_min_wins(n, target_team, points, games):

    target_remaining_matches = []
    for j in range(1, n + 1):
        if j != target_team:

            if not games[target_team][j]:
                target_remaining_matches.append((target_team, j))

            if not games[j][target_team]:
                target_remaining_matches.append((j, target_team))
    
    left, right = 0, len(target_remaining_matches)
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if can_win_with_wins(n, target_team, points, games, mid, target_remaining_matches):
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    
    return result

def can_win_with_wins(n, target_team, initial_points, games, num_wins, target_remaining_matches):

    points = initial_points.copy()
    
    if num_wins > len(target_remaining_matches):
        return False
    
    max_target_points = points[target_team] + num_wins * 3 + (len(target_remaining_matches) - num_wins) * 1
    
    for team in range(1, n + 1):
        if team != target_team and points[team] > max_target_points:
            return False
    
    prob = pulp.LpProblem("SnailSoft", pulp.LpMinimize)
    
    x = {}
    e = {}
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j and i != target_team and j != target_team and not games[i][j]:
                x[(i, j)] = pulp.LpVariable(f"x_{i}_{j}", cat=pulp.LpBinary)
                e[(i, j)] = pulp.LpVariable(f"e_{i}_{j}", cat=pulp.LpBinary)
    
    y = {}  
    d = {} 
    
    for match in target_remaining_matches:
        y[match] = pulp.LpVariable(f"y_{match[0]}_{match[1]}", cat=pulp.LpBinary)
        d[match] = pulp.LpVariable(f"d_{match[0]}_{match[1]}", cat=pulp.LpBinary)
    
    prob += pulp.lpSum([y[match] for match in target_remaining_matches]) == num_wins
    
    for match in target_remaining_matches:
        prob += y[match] + d[match] <= 1
    
    for (i, j) in x.keys():
        prob += x[(i, j)] + e[(i, j)] <= 1
    
    for team in range(1, n + 1):
        if team == target_team:
            continue
        
        team_points = points[team]
        variables_added = False
        
        for match in target_remaining_matches:
            home, away = match
            if home == target_team and away == team:
                
                team_points += 3 * (1 - y[match] - d[match]) + d[match]
                variables_added = True
            elif home == team and away == target_team:
                
                team_points += 3 * (1 - y[match] - d[match]) + d[match]
                variables_added = True
        
        for other in range(1, n + 1):
            if other == team or other == target_team:
                continue
            
            if not games[team][other]:
                team_points += 3 * x[(team, other)] + e[(team, other)]
                variables_added = True
            
            if not games[other][team]:
                team_points += 3 * (1 - x[(other, team)] - e[(other, team)]) + e[(other, team)]
                variables_added = True
        
        if not variables_added:
            if team_points > max_target_points:
                return False
        else:
            prob += team_points <= max_target_points
    
    prob += 0
    
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    return prob.status == pulp.LpStatusOptimal

if __name__ == "__main__":
    main()
