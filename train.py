import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

rng = np.random.default_rng(42)
N = 1000  # synthetic second-innings (chase) match states

# Sample realistic chase states from a 20-over (120-ball) innings
target = rng.integers(120, 221, N).astype(float)          # target runs
balls_remaining = rng.integers(6, 121, N).astype(float)   # balls left
balls_bowled = 120 - balls_remaining
wickets_lost = np.clip(rng.poisson(3.2, N), 0, 9).astype(float)
# runs scored so far: roughly par pace with noise, capped below target
progress = balls_bowled / 120.0
runs_scored = np.clip(target * progress * rng.normal(1.0, 0.18, N), 0, target - 1)
runs_scored = np.round(runs_scored).astype(float)

runs_needed = target - runs_scored
rrr = runs_needed / np.maximum(balls_remaining / 6.0, 0.5)          # required run rate
crr = runs_scored / np.maximum(balls_bowled / 6.0, 0.5)             # current run rate

X_raw = np.column_stack([target, runs_scored, wickets_lost, balls_remaining, rrr, crr])
FEATURES = ["target", "runs_scored", "wickets_lost", "balls_remaining",
            "required_run_rate", "current_run_rate"]

# Generative logit: a chase is won when the required rate is below what the
# batting side can score with the wickets it still has in hand, plus a
# small bonus for being ahead of (slightly accelerating) par pace.
# Expected scoring rate rises with wickets in hand (~6.5 + 0.45 per wicket).
exp_rate = 6.5 + 0.45 * (10 - wickets_lost)
par = target * progress ** 1.15   # scoring accelerates towards the death
ahead = runs_scored - par
z = (0.85 * (exp_rate - rrr)
     + 0.04 * ahead
     - 0.12 * wickets_lost
     - 0.4 * (wickets_lost >= 8)
     - 0.45)  # rebalance: keeps the win rate near 50%
p = 1 / (1 + np.exp(-z))
y = (rng.random(N) < p).astype(int)

mean = X_raw.mean(axis=0)
std = X_raw.std(axis=0)
X = (X_raw - mean) / std

model = LogisticRegression(C=1.0, max_iter=2000).fit(X, y)
skf = StratifiedKFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(LogisticRegression(C=1.0, max_iter=2000), X, y, cv=skf)
proba_cv = cross_val_predict(LogisticRegression(C=1.0, max_iter=2000), X, y, cv=skf, method="predict_proba")[:, 1]
acc = float(accuracy_score(y, pred_cv))
auc = float(roc_auc_score(y, proba_cv))
base = float(max(np.bincount(y)) / len(y))
print(f"n={N} win_rate={y.mean():.3f}")
print(f"CV accuracy={acc:.3f} AUC={auc:.3f} baseline={base:.3f}")
print(classification_report(y, pred_cv, target_names=["chase lost", "chase won"], digits=3))

mj = {"features": FEATURES, "mean": mean.tolist(), "std": std.tolist(),
      "coef": model.coef_[0].tolist(), "intercept": float(model.intercept_[0]),
      "metrics": {"cv_accuracy": acc, "auc": auc, "baseline_accuracy": base,
                  "win_rate": float(y.mean()), "n": N}}
with open("model.json", "w") as f:
    json.dump(mj, f, indent=1)

def py_prob(row):
    xs = (np.array(row) - mean) / std
    return float(model.predict_proba([xs])[0][1] * 100)

def full_row(target_, runs_, wkts_, balls_left_):
    balls_bowled_ = 120 - balls_left_
    rrr_ = (target_ - runs_) / max(balls_left_ / 6.0, 0.5)
    crr_ = runs_ / max(balls_bowled_ / 6.0, 0.5)
    return [target_, runs_, wkts_, balls_left_, rrr_, crr_]

samples = [
    full_row(180, 150, 3, 30),   # 30 needed off 30 balls, 7 wickets left: strong position
    full_row(180, 90, 7, 60),    # 90 off 60, only 3 wickets left: tough
    full_row(160, 110, 4, 36),   # 50 off 36, 6 wickets left: comfortable
    full_row(200, 60, 2, 90),    # early days, 140 off 90: even
    full_row(150, 145, 8, 12),   # 5 off 12 but only 2 wickets left: tense
]
for s in samples:
    print([round(v, 2) for v in s], "->", round(py_prob(s), 2), "% win chance")
with open("parity_samples.json", "w") as f:
    json.dump([{"row": s, "prob": py_prob(s)} for s in samples], f, indent=1)
