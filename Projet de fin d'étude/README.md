# SentixPredict — Veille IA × Finance × NLP

Prédiction mensuelle de la rentabilité du S&P 500 via NLP et sentiment financier.

## Dernier rapport de veille

📄 **[Rapport du 2026-05-01](reports/rapport-2026-05-01.md)**

## 🔥 3 dernières trouvailles importantes

1. **TradingAgents v0.2.4** (25 avril 2026) — Framework multi-agent LangGraph simulant une firme de trading entière (5 couches, ~12 agents LLM). Support Claude 4, GPT-5, Gemini 3. → [GitHub](https://github.com/TauricResearch/TradingAgents)

2. **Ensemble DeBERTa+RoBERTa+FinBERT ≈ 80 % de précision** sur la prédiction de mouvement boursier à partir du sentiment de news financières. (arXiv:2602.00086, mars 2026) → [arXiv](https://arxiv.org/abs/2602.00086)

3. **NOSIBLE/financial-sentiment** — 100 000 samples news LLM-annotés via active-learning, disponibles sur HuggingFace. Outperform Financial PhraseBank. Dataset candidat immédiat pour SentixPredict. → [HuggingFace](https://huggingface.co/datasets/NOSIBLE/financial-sentiment)

## Structure du dépôt

```
├── data/
│   └── veille-YYYY-MM-DD.csv      # Données structurées (datasets, modèles, repos, papiers, marchés, MLOps)
├── reports/
│   └── rapport-YYYY-MM-DD.md      # Rapport quotidien de veille
├── Présentation de projet/
│   └── ...                         # Slides et documents du projet
└── README.md
```

## Contexte du projet

SentixPredict vise à prédire mensuellement la rentabilité du S&P 500 en combinant :
- **NLP et analyse de sentiment** sur les actualités financières
- **Modèles pré-entraînés** (FinBERT, FinGPT, DeBERTa, RoBERTa)
- **Données macro** (décisions Fed, CPI, earnings tech)
- **Pipeline MLOps** respectant les exigences DORA / AI Act 2026

## Historique des rapports

| Date | Rapport | CSV |
|---|---|---|
| 2026-05-01 | [rapport-2026-05-01.md](reports/rapport-2026-05-01.md) | [veille-2026-05-01.csv](data/veille-2026-05-01.csv) |
