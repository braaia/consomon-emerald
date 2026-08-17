# Tabela de XP para level up

Baseado na lógica de `poke_status.py`:

- `exp_to_next = int(100 + (level - 1) * 35)`
- O valor mostrado abaixo é o total de XP acumulado necessário para chegar ao nível indicado.

| Nível | XP total para chegar ao nível |
| -----: | -----------------------------: |
|      1 |                              0 |
|      2 |                            100 |
|      3 |                            235 |
|      4 |                            405 |
|      5 |                            610 |
|      6 |                            850 |
|      7 |                          1.125 |
|      8 |                          1.435 |
|      9 |                          1.780 |
|     10 |                          2.160 |
|     11 |                          2.575 |
|     12 |                          3.025 |
|     13 |                          3.510 |
|     14 |                          4.030 |
|     15 |                          4.585 |
|     16 |                          5.175 |
|     17 |                          5.800 |
|     18 |                          6.460 |
|     19 |                          7.155 |
|     20 |                          7.885 |
|     21 |                          8.650 |
|     22 |                          9.450 |
|     23 |                         10.285 |
|     24 |                         11.155 |
|     25 |                         12.060 |
|     26 |                         13.000 |
|     27 |                         13.975 |
|     28 |                         14.985 |
|     29 |                         16.030 |
|     30 |                         17.110 |
|     31 |                         18.225 |
|     32 |                         19.375 |
|     33 |                         20.560 |
|     34 |                         21.780 |
|     35 |                         23.035 |

## Fórmula do código

```python
pokemon["exp_to_next"] = int(100 + (pokemon["level"] - 1) * 35)
```

A cada level up, o XP restante é subtraído e o próximo valor é recalculado com a mesma fórmula.
