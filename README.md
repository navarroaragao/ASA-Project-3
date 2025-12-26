# Projeto ASA – Análise de Campeonatos com Programação Linear

Este projeto foi desenvolvido no âmbito da unidade curricular **Análise e Síntese de Algoritmos (ASA)** 
                 Instituto Superior Técnico, ano letivo 2025/2026.

O objetivo é determinar, para cada equipa de um campeonato por pontos com duas voltas, o **menor número de jogos que essa equipa ainda precisa de ganhar** para que seja possível conquistar o campeonato, assumindo que os resultados dos jogos das outras equipas e os critérios de desempate lhe são favoráveis.

---

## Abordagem

O problema é modelado como um conjunto de **problemas de Programação Linear (PL)**, resolvidos com a biblioteca **PuLP** em Python.

Para cada equipa `i`:

1. Assume-se que a equipa ganha exatamente `k` jogos dos que ainda faltam.
2. Os restantes jogos da equipa `i` são considerados empates, maximizando os seus pontos.
3. Os jogos restantes entre as outras equipas são modelados através de variáveis de PL.
4. Impõem-se restrições que garantem que nenhuma outra equipa termina o campeonato com mais pontos do que a equipa `i`.
5. O menor valor de `k` para o qual o problema é viável corresponde à resposta.

Caso não exista qualquer valor de `k` que satisfaça as restrições, conclui-se que a equipa já não pode ganhar o campeonato e o resultado é `-1`.

---

## Input

O programa lê do **standard input**:

- Uma linha com dois inteiros `n` e `m`:
  - `n`: número total de equipas
  - `m`: número de jogos já realizados
- `m` linhas seguintes, cada uma com três inteiros:
  - `i`: identificador da equipa da casa (1 ≤ i ≤ n)
  - `j`: identificador da equipa visitante (j ≠ i)
  - `r`: resultado do jogo  
    - `i` ou `j` se houver vencedor  
    - `0` em caso de empate

---

## Output

O programa escreve no **standard output** `n` linhas:

- Na linha `i`, um único inteiro correspondente ao **menor número de vitórias** que a equipa `i` ainda precisa de obter para poder ganhar o campeonato.
- Caso a equipa `i` já não possa ganhar o campeonato, é impresso `-1`.

---

## Execução

### Dependências

- Python 3
- Biblioteca PuLP

Instalação da biblioteca PuLP:
```bash
python3 -m pip install pulp
```
Para correr o programa:
```
python3 SnailSoft.py < ./Inputs_Outputs/input1.txt
```
- No final é possível confirmar o output através do output com o mesmo número do input
