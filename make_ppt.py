from pptx import Presentation
from pptx.util import Inches, Pt
import sys
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "cricwin.vercel.app"
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def add(i, title, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame; tf.word_wrap = True
    for j, ln in enumerate(lines):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = ln; p.font.size = Pt(20); p.space_after = Pt(10)
add(0, "CricWin — Cricket Match Win Probability Predictor", ["An AI/ML project by Vikranth Reddy", "B.Tech CSE (AI & ML), 2nd Year — Woxsen University", "A model that reads the match state of a T20 chase and predicts the batting side's chance of winning"])
add(1, "The Problem", ["Every cricket fan asks the same question mid-chase: 'are we going to win this?'", "TV win predictors exist, but they are black boxes — nobody sees how the number is made", "Can a simple, explainable model turn the match state into a win probability?", "CricWin answers that question with logistic regression anyone can follow"])
add(2, "The Solution — CricWin", ["Enter 4 numbers: target, runs scored, wickets lost, balls remaining", "The model works out the required and current run rates, then returns the win chance as a percentage", "Try a comfortable chase or a tough chase with one click", "Runs fully in the browser — no backend, no waiting"])
add(3, "Tech Stack", ["Python + scikit-learn: dataset generation and model training", "Logistic regression (C = 1.0) on 6 standardised features", "HTML, CSS and vanilla JavaScript for the interactive demo", "GitHub for source control, Vercel for free hosting"])
add(4, "Architecture", ["Dataset: 1,000 synthetic T20 chase states built from simple cricket logic", "Match state -> required & current run rates -> standardisation -> logistic regression -> sigmoid -> win probability", "model.json ships with the site; JavaScript applies the same formula", "Training script: train.py; site generator: gen_site.py"])
add(5, "Live Demo", ["Try it: enter the match state and press Predict Win Chance", "Chasing 180, at 150/3 with 30 balls left -> about 91.3% win chance", "Chasing 180, at 90/7 with 60 balls left -> about 13.1% win chance", f"Demo: https://{DOMAIN}"])
add(6, "Results", ["5-fold cross-validation accuracy: 83.0%, AUC: 0.91", "Baseline (always guessing the most common result): 56.3% — a clear lift", "Win rate in the data: 56.3%, close to a balanced chase", "Browser demo matches Python probabilities exactly on all test samples"])
add(7, "Future Scope", ["Train on real ball-by-ball data (IPL / T20 internationals)", "Add features: pitch type, venue, batting order strength, player form", "Extend to first-innings score prediction and live over-by-over updates", "Add a Duckworth-Lewis style rain-adjustment for interrupted matches"])
add(8, "Thank You", ["CricWin — Cricket Match Win Probability Predictor", "Vikranth Reddy, B.Tech CSE (AI & ML), Woxsen University", "Source: github.com/HVRGAMING2705/cricwin", "Questions welcome!"])
prs.save("/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_CricWin_2026-11-13.pptx")
print("slides:", len(prs.slides._sldIdLst))
