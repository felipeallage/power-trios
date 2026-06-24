# Power Trios — A Ciência por Trás do Som

> "Como três músicos conseguem soar maiores do que bandas inteiras?"

## Sobre o Projeto

Este projeto combina análise de dados, acústica musical e storytelling para responder uma pergunta que todo fã de rock já se fez: por que power trios como Jimi Hendrix Experience, Cream e The Police soam tão grandes com apenas três instrumentos?

A resposta não está apenas no talento — está na **arquitetura do som**.

## Hipótese Central

> "O Jimi Hendrix Experience criava a percepção de uma banda maior porque cada instrumento ocupava uma faixa de frequência distinta e complementar, sem sobreposição — algo raro para 1967."

## Casos Analisados

| Trio | Período | Estilo |
|------|---------|--------|
| Jimi Hendrix Experience | 1966–1970 | Blues/Psychedelic Rock |
| Cream | 1966–1968 | Blues Rock |
| The Police | 1977–1984 | New Wave/Reggae Rock |
| ZZ Top | 1969–presente | Blues Rock |
| SRV & Double Trouble | 1978–1990 | Texas Blues |

## Metodologia

- **Análise espectral** com `librosa` — extração de energia por faixa de frequência
- **Comparação com contemporâneos** — Rolling Stones, Beatles, Cream
- **Visualizações** — espectrogramas, heatmaps, radar charts
- **Narrativa histórica** — contexto musical de cada trio

## Estrutura do Projeto

power-trios/
│
├── data/
│   └── audio/
│       ├── hendrix/        — Purple Haze, Voodoo Child, Little Wing, All Along the Watchtower
│       └── comparacao/     — Jumpin Jack Flash, Come Together, Sunshine of Your Love
│
├── notebooks/
│   ├── 01_hendrix_espectral.ipynb      — análise espectral do Experience
│   ├── 02_comparacao_contemporaneos.ipynb
│   ├── 03_outros_trios.ipynb
│   └── 04_conclusao.ipynb
│
└── README.md

## Stack Tecnológica

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Librosa](https://img.shields.io/badge/Librosa-0.10-green)
![Pandas](https://img.shields.io/badge/Pandas-2.2-blue)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8-orange)

- `librosa` — análise de áudio e extração de features espectrais
- `pandas` — manipulação de dados
- `matplotlib` / `plotly` — visualizações
- `numpy` — processamento numérico
- `streamlit` — dashboard interativo (em desenvolvimento)

## Status

- [x] Análise espectral — Jimi Hendrix Experience (4 faixas)
- [x] Comparação com contemporâneos (Rolling Stones, Beatles, Cream)
- [ ] Análise dos outros 4 trios
- [ ] Dashboard Streamlit
- [ ] Notebook narrativo completo

## Autor

Felipe Allage — [github.com/felipeallage](https://github.com/felipeallage)