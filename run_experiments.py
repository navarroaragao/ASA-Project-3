#!/usr/bin/env python3
"""
Script para executar experimentos e medir tempos de execução do SnailSoft.py
"""
import subprocess
import time
import json
import os

def compile_generator():
    """Compila o gerador de instâncias"""
    print("Compilando gerador...")
    result = subprocess.run(['g++', '-std=c++11', '-o', 'gerador_p3', 'gerador_p3.cpp'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro ao compilar: {result.stderr}")
        return False
    print("Gerador compilado com sucesso!")
    return True

def generate_instance(n_teams, prob, seed):
    """Gera uma instância usando o gerador"""
    result = subprocess.run(['./gerador_p3', str(n_teams), str(prob), str(seed)],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro ao gerar instância: {result.stderr}")
        return None
    return result.stdout

def count_constraints_and_variables(instance_data):
    """Conta o número de restrições e variáveis na instância"""
    lines = instance_data.strip().split('\n')
    n_teams, n_played = map(int, lines[0].split())
    
    # Calcular jogos restantes
    remaining_games = 0
    remaining_counts = [[2 if i != j else 0 for j in range(n_teams)] for i in range(n_teams)]
    
    for i in range(1, n_played + 1):
        u, v, winner = map(int, lines[i].split())
        u -= 1
        v -= 1
        if remaining_counts[u][v] > 0:
            remaining_counts[u][v] -= 1
            remaining_counts[v][u] -= 1
    
    for i in range(n_teams):
        for j in range(i + 1, n_teams):
            remaining_games += remaining_counts[i][j]
    
    # Variáveis: 2 variáveis binárias por jogo restante
    n_variables = 2 * remaining_games
    
    # Restrições:
    # - 1 restrição por jogo restante (w_i + w_j <= 1)
    # - Para cada equipe k: (n_teams - 1) restrições de ordenação
    n_constraints = remaining_games + n_teams * (n_teams - 1)
    
    return n_variables, n_constraints, n_teams, n_played, remaining_games

def run_snailsoft(instance_data):
    """Executa o SnailSoft.py e mede o tempo"""
    start_time = time.time()
    
    result = subprocess.run(['python3', 'SnailSoft.py'],
                          input=instance_data,
                          capture_output=True,
                          text=True)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if result.returncode != 0:
        print(f"Erro ao executar SnailSoft: {result.stderr}")
        return None, elapsed_time
    
    return result.stdout, elapsed_time

def main():
    # Compilar o gerador
    if not compile_generator():
        return
    
    # Configurações dos experimentos
    # Vamos gerar instâncias com número crescente de equipas
    team_sizes = [3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 20, 25]
    probability = 70  # Probabilidade de um jogo ter sido jogado
    seed = 42  # Semente fixa para reprodutibilidade
    
    results = []
    
    print("\nExecutando experimentos...")
    print("=" * 80)
    
    for i, n_teams in enumerate(team_sizes, 1):
        print(f"\nExperimento {i}/{len(team_sizes)}: N = {n_teams} equipas")
        print("-" * 80)
        
        # Gerar instância
        instance_data = generate_instance(n_teams, probability, seed + i)
        if instance_data is None:
            continue
        
        # Contar variáveis e restrições
        n_vars, n_constr, n_teams_check, n_played, n_remaining = count_constraints_and_variables(instance_data)
        
        print(f"  Equipas: {n_teams_check}")
        print(f"  Jogos já realizados: {n_played}")
        print(f"  Jogos restantes: {n_remaining}")
        print(f"  Variáveis: {n_vars}")
        print(f"  Restrições: {n_constr}")
        print(f"  Total (Vars + Constr): {n_vars + n_constr}")
        
        # Executar SnailSoft
        output, elapsed_time = run_snailsoft(instance_data)
        
        print(f"  Tempo de execução: {elapsed_time:.4f} segundos")
        
        results.append({
            'n_teams': n_teams,
            'n_played': n_played,
            'n_remaining': n_remaining,
            'n_variables': n_vars,
            'n_constraints': n_constr,
            'total_size': n_vars + n_constr,
            'time': elapsed_time
        })
    
    # Salvar resultados em JSON
    with open('experimental_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 80)
    print("Experimentos concluídos!")
    print(f"Resultados salvos em: experimental_results.json")
    print("=" * 80)
    
    # Mostrar resumo
    print("\nResumo dos resultados:")
    print("-" * 80)
    for r in results:
        print(f"N={r['n_teams']:3d} | Vars={r['n_variables']:5d} | "
              f"Constr={r['n_constraints']:5d} | Total={r['total_size']:6d} | "
              f"Tempo={r['time']:7.4f}s")

if __name__ == "__main__":
    main()
