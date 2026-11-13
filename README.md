# CricWin — Cricket Match Win Probability Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Logistic regression (C=1.0) on standardized features — target, runs scored, wickets lost, balls remaining, required run rate, current run rate — trained on 1,000 synthetic T20 chase states (seed 42).

- 5-fold CV accuracy: 83.0%, AUC: 0.91 (majority-class baseline: 56.3%)
- Live demo: https://cricwin-one.vercel.app (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.

Note: classroom demo on synthetic chase states — real matches have pitch, weather, players and pressure that six numbers can't capture.
