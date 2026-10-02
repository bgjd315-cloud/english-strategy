"""列出每種策略可選的題目（選擇題、有試卷圖片），供挑選例題。"""
import csv, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
SRC = R.parent / "english-reading"
sys.path.insert(0, str(SRC / "tools"))
from reading_data import build_practice
P = build_practice(SRC)
ok = {(["會考英語", "學測英文"][it[0]], it[1], it[2]) for it in P["items"]}
rows = [r for r in csv.DictReader(open(R / "data/items.csv", encoding="utf-8-sig")) if (r["考試"], int(r["年度"]), int(r["題號"])) in ok]
out = open(R / "notes/candidates.txt", "w", encoding="utf-8")
for s in [f"E{i}" for i in range(1, 13)]:
    xs = [r for r in rows if r["策略"] == s]
    out.write(f"\n===== {s} ({len(xs)})\n")
    for r in xs:
        qid = ("K" if r["考試"] == "會考英語" else "X") + r["年度"] + "-" + r["題號"]
        out.write(f"{qid} [{r['答案']}] {r['考點']} | {r['陷阱']} {r['判讀提示']} | passage {len(r['題組選文'])} | {r['題目文字'][:160]}\n")
print(len(rows))
