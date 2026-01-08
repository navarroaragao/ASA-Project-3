#!/usr/bin/env python3
"""
Script para gerar gráficos da avaliação experimental
"""
import json
import sys
import matplotlib.pyplot as plt
import numpy as np

def plot_time_vs_size(results):
    """Gera gráfico de tempo vs f(n) = n²"""
    
    # Extrair dados
    n_teams = [r['n_teams'] for r in results]
    times = [r['time'] for r in results]
    
    # Calcular f(n) = n²
    f_n = [n**2 for n in n_teams]
    
    # Criar figura
    plt.figure(figsize=(12, 7))
    
    # Plotar linha com marcadores
    plt.plot(f_n, times, marker='o', markersize=8, linewidth=2, color='blue')
    
    # Configurações do gráfico
    plt.xlabel('f(n) = n²', fontsize=12)
    plt.ylabel('Tempo (s)', fontsize=12)
    plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # Salvar figura
    plt.tight_layout()
    plt.savefig('plot_time_vs_size.png', dpi=300, bbox_inches='tight')
    print("Gráfico salvo em: plot_time_vs_size.png")
    
    plt.savefig('plot_time_vs_size.pdf', bbox_inches='tight')
    print("Gráfico salvo em: plot_time_vs_size.pdf")

def plot_multiple_views(results):
    """Gera múltiplos gráficos em uma única figura"""
    
    # Extrair dados
    sizes = [r['total_size'] for r in results]
    times = [r['time'] for r in results]
    n_teams = [r['n_teams'] for r in results]
    n_vars = [r['n_variables'] for r in results]
    n_constr = [r['n_constraints'] for r in results]
    
    # Criar figura com subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Gráfico 1: Tempo vs Tamanho Total
    ax1 = axes[0, 0]
    ax1.scatter(sizes, times, s=80, alpha=0.6, color='blue', edgecolors='black')
    z = np.polyfit(sizes, times, 2)
    p = np.poly1d(z)
    x_smooth = np.linspace(min(sizes), max(sizes), 100)
    ax1.plot(x_smooth, p(x_smooth), "r--", alpha=0.8, linewidth=2)
    ax1.set_xlabel('Tamanho Total (Vars + Restr)', fontweight='bold')
    ax1.set_ylabel('Tempo (s)', fontweight='bold')
    ax1.set_title('Tempo vs Tamanho Total', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Gráfico 2: Tempo vs Número de Equipas
    ax2 = axes[0, 1]
    ax2.scatter(n_teams, times, s=80, alpha=0.6, color='green', edgecolors='black')
    z2 = np.polyfit(n_teams, times, 2)
    p2 = np.poly1d(z2)
    x_smooth2 = np.linspace(min(n_teams), max(n_teams), 100)
    ax2.plot(x_smooth2, p2(x_smooth2), "r--", alpha=0.8, linewidth=2)
    ax2.set_xlabel('Número de Equipas (N)', fontweight='bold')
    ax2.set_ylabel('Tempo (s)', fontweight='bold')
    ax2.set_title('Tempo vs Número de Equipas', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Gráfico 3: Variáveis e Restrições vs Equipas
    ax3 = axes[1, 0]
    ax3.plot(n_teams, n_vars, 'o-', label='Variáveis', linewidth=2, markersize=6, alpha=0.7)
    ax3.plot(n_teams, n_constr, 's-', label='Restrições', linewidth=2, markersize=6, alpha=0.7)
    ax3.plot(n_teams, sizes, '^-', label='Total', linewidth=2, markersize=6, alpha=0.7)
    ax3.set_xlabel('Número de Equipas (N)', fontweight='bold')
    ax3.set_ylabel('Quantidade', fontweight='bold')
    ax3.set_title('Crescimento de Variáveis e Restrições', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Gráfico 4: Tempo em escala log-log
    ax4 = axes[1, 1]
    ax4.scatter(sizes, times, s=80, alpha=0.6, color='purple', edgecolors='black')
    ax4.set_xlabel('Tamanho Total (Vars + Restr)', fontweight='bold')
    ax4.set_ylabel('Tempo (s)', fontweight='bold')
    ax4.set_title('Tempo vs Tamanho (Escala Log-Log)', fontweight='bold')
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.grid(True, alpha=0.3, which='both')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar
    plt.savefig('plot_comprehensive.png', dpi=300, bbox_inches='tight')
    print("Gráfico abrangente salvo em: plot_comprehensive.png")
    
    plt.savefig('plot_comprehensive.pdf', bbox_inches='tight')
    print("Gráfico abrangente salvo em: plot_comprehensive.pdf")

def main():
    # Verificar se matplotlib está instalado
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Erro: matplotlib não está instalado.")
        print("Instale com: pip install matplotlib")
        sys.exit(1)
    
    # Ler resultados
    try:
        with open('experimental_results.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo experimental_results.json não encontrado.")
        print("Execute primeiro o script run_experiments.py")
        sys.exit(1)
    
    if not results:
        print("Erro: Nenhum resultado encontrado no arquivo.")
        sys.exit(1)
    
    print("Gerando gráficos...")
    
    # Gerar gráfico principal
    plot_time_vs_size(results)
    
    # Gerar gráficos adicionais
    plot_multiple_views(results)
    
    print("\nGráficos gerados com sucesso!")
    print("\nArquivos criados:")
    print("  - plot_time_vs_size.png (gráfico principal)")
    print("  - plot_time_vs_size.pdf (gráfico principal em PDF)")
    print("  - plot_comprehensive.png (4 gráficos)")
    print("  - plot_comprehensive.pdf (4 gráficos em PDF)")

if __name__ == "__main__":
    main()
