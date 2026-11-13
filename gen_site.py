import json
m = json.load(open("model.json"))
features, mean, std = m["features"], m["mean"], m["std"]
coef, icpt = m["coef"], m["intercept"]
mt = m["metrics"]
acc, auc, base = mt["cv_accuracy"], mt["auc"], mt["baseline_accuracy"]
DOMAIN = "cricwin.vercel.app"
JS_MODEL = f"""const MEAN = {json.dumps(mean)};
const STD = {json.dumps(std)};
const COEF = {json.dumps(coef)};
const INTERCEPT = {icpt};
function winProb(vals){{
  let z = INTERCEPT;
  for (let i = 0; i < 6; i++) z += COEF[i] * (vals[i] - MEAN[i]) / STD[i];
  return 1 / (1 + Math.exp(-z)) * 100;
}}
function fullRow(target, runs, wkts, ballsLeft){{
  const ballsBowled = 120 - ballsLeft;
  const rrr = (target - runs) / Math.max(ballsLeft / 6, 0.5);
  const crr = runs / Math.max(ballsBowled / 6, 0.5);
  return [target, runs, wkts, ballsLeft, rrr, crr];
}}"""
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CricWin — Cricket Match Win Probability Predictor | AI/ML Project</title>
<meta name="description" content="CricWin predicts the batting side's win probability in a T20 run chase from the match state — target, runs scored, wickets lost and balls left — using a logistic regression model trained on 1,000 synthetic chase states. Try it live in your browser.">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="CricWin — Cricket Match Win Probability Predictor">
<meta property="og:description" content="Enter the match state of a T20 chase and instantly see the batting side's win probability, with a real trained ML model running in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="CricWin — Cricket Match Win Probability Predictor">
<meta name="twitter:description" content="Logistic regression win-probability predictor for T20 run chases. Try the live demo in your browser.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"CricWin","applicationCategory":"EducationalApplication","description":"T20 run-chase win probability predictor using logistic regression.","url":"https://{DOMAIN}/"}}</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:720px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em}} label{{display:block;margin:12px 0 4px;font-weight:bold}}
input,select{{width:100%;padding:10px;font-size:16px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
button{{margin-top:16px;margin-right:8px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:none;border-radius:4px;cursor:pointer}}
#result{{margin-top:24px;padding:20px;border:2px solid #000;border-radius:8px;display:none}}
#result b{{font-size:1.6em}}
.note{{color:#333;font-size:.95em}} code{{background:#f2f2f2;padding:2px 5px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}}
</style>
</head>
<body>
<h1>&#127951; CricWin — Cricket Win Probability Predictor</h1>
<p class="note">A 2nd-year B.Tech AI/ML project by Vikranth Reddy. A logistic regression model trained on 1,000 synthetic T20 chase states predicts the batting side&apos;s chance of winning from the match state: target, runs scored, wickets lost and balls remaining. The required run rate and current run rate are worked out from those four numbers. 5-fold CV: <b>accuracy = {acc:.1%}</b>, <b>AUC = {auc:.2f}</b> vs a majority-class baseline of {base:.1%}.</p>
<div class="grid">
<label>Target (runs)<input type="number" step="1" id="f0" value="180"></label>
<label>Runs scored so far<input type="number" step="1" id="f1" value="120"></label>
<label>Wickets lost<input type="number" step="1" min="0" max="9" id="f2" value="4"></label>
<label>Balls remaining<input type="number" step="1" min="1" max="120" id="f3" value="48"></label>
</div>
<button onclick="predict()">Predict Win Chance</button>
<button onclick="tryComfortable()">Try comfortable chase</button>
<button onclick="tryTough()">Try tough chase</button>
<div id="result"></div>
<p class="note">How it works: the required run rate (runs needed &divide; overs left) and current run rate (runs scored &divide; overs bowled) are computed from your inputs; all six numbers are standardised (subtract the training mean, divide by the standard deviation), multiplied by the model&apos;s learned weights, and summed with a bias; a sigmoid turns the total into a win probability. The exact same weights run in this page and in the Python training script (<code>train.py</code>), so the browser result matches the trained model.</p>
<p class="note">Try it: chasing 180, at 150/3 with 30 balls left &rarr; about 91.3% win chance. Chasing 180, at 90/7 with 60 balls left &rarr; about 13.1%. Chasing 160, at 110/4 with 36 balls left &rarr; about 48.0% — a genuine coin-flip.</p>
<p class="note">Honest note: this model was trained on synthetic chase states generated from simple cricket logic, so it is a classroom demo — real matches have pitch, weather, players and pressure that no six numbers capture.</p>
<p><a href="https://github.com/HVRGAMING2705/cricwin">View source on GitHub</a></p>
<script>
{JS_MODEL}
function show(){{
  const target = parseFloat(document.getElementById("f0").value) || 0;
  const runs = parseFloat(document.getElementById("f1").value) || 0;
  const wkts = parseFloat(document.getElementById("f2").value) || 0;
  const ballsLeft = parseFloat(document.getElementById("f3").value) || 1;
  const row = fullRow(target, runs, wkts, ballsLeft);
  const p = winProb(row);
  const el = document.getElementById("result");
  el.style.display = "block";
  const verdict = p >= 70 ? "&#128994; FAVOURITES — the chase is well under control" : p >= 40 ? "&#128993; EVEN STEVENS — genuinely anyone&apos;s game" : "&#128308; UP AGAINST IT — needs something special now";
  el.innerHTML = "<b>" + p.toFixed(1) + "% win chance</b><br>" + verdict +
    "<br><span class=note>Required run rate " + row[4].toFixed(2) + " &middot; current run rate " + row[5].toFixed(2) + " &middot; " + Math.max(target - runs, 0) + " needed off " + ballsLeft + " balls with " + (10 - wkts) + " wickets in hand.</span>";
}}
function predict(){{ show(); }}
function tryComfortable(){{ const v = [180, 150, 3, 30]; for (let i = 0; i < 4; i++) document.getElementById("f" + i).value = v[i]; show(); }}
function tryTough(){{ const v = [180, 90, 7, 60]; for (let i = 0; i < 4; i++) document.getElementById("f" + i).value = v[i]; show(); }}
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
vercel = {
 "headers": [{"headers": [
   {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
   {"key": "X-Content-Type-Options", "value": "nosniff"},
   {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
   {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
   {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
   {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
   {"key": "Access-Control-Allow-Origin", "value": f"https://{DOMAIN}"},
   {"key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}],
  "source": "/(.*)"}]}
open("vercel.json", "w").write(json.dumps(vercel, indent=1))
open("404.html", "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page Not Found — CricWin</title><style>body{{font-family:Arial,sans-serif;color:#000;max-width:640px;margin:60px auto;padding:24px}}</style></head><body><h1>404 — Page not found</h1><p>This page does not exist on CricWin.</p><p><a href="https://{DOMAIN}/">Back to CricWin</a></p></body></html>""")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open("sitemap.xml", "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{DOMAIN}/</loc></url></urlset>
""")
open("README.md", "w").write(f"""# CricWin — Cricket Match Win Probability Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

Logistic regression (C=1.0) on standardized features — target, runs scored, wickets lost, balls remaining, required run rate, current run rate — trained on 1,000 synthetic T20 chase states (seed 42).

- 5-fold CV accuracy: {acc:.1%}, AUC: {auc:.2f} (majority-class baseline: {base:.1%})
- Live demo: https://{DOMAIN} (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.

Note: classroom demo on synthetic chase states — real matches have pitch, weather, players and pressure that six numbers can't capture.
""")
samples = json.load(open("parity_samples.json"))
parity = JS_MODEL + "\n" + "\n".join(
    f"console.log(JSON.stringify({{row: {json.dumps(s['row'])}, js: winProb({json.dumps(s['row'])}), py: {s['prob']}}}));"
    for s in samples)
open("parity.js", "w").write(parity)
print("site files written, acc", acc)
