#!/usr/bin/env python3
"""由 ../english-reading 的題目與逐題判讀，標上英文閱讀策略（E1–E12），輸出 data/items.csv。

策略由判讀的能力代碼與題型推得（規則見 strategy()），不是官方分類。
會考英語只收閱讀測驗（聽力不收）；學測英文收全部選擇題與混合題。
"""
import csv
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
SRC = R.parent / "english-reading"
sys.path.insert(0, str(SRC / "tools"))
from reading_data import EXAMS, _clean, _exam, build_reading  # noqa: E402

STRUCT = re.compile(r"順序|結構|段|排序|總結|補充|分類|舉例|先.+再")


def strategy(ei, lab, skill, hint):
    kind = lab.split("：")[0]
    if skill == "K2":
        return "E12"
    if skill == "K1":
        if kind == "文意選填":
            return "E9"
        if kind in ("綜合測驗", "克漏字"):
            return "E11"
        return "E10"
    if skill == "C1":
        return "E7" if STRUCT.search(hint) else "E6"
    return {"A1": "E1", "B3": "E2", "A2": "E3", "B1": "E4", "B2": "E5", "C2": "E6", "B5": "E7", "B4": "E8"}[skill]


def main():
    reading = {(it[0], it[1], it[2]): it for it in build_reading(SRC)["items"]}
    rows = []
    for ei in range(len(EXAMS)):
        for y, q, g, lab, a, ns, ex in _exam(SRC, ei):
            it = reading[(ei, y, q["n"])]
            rows.append({"考試": ["會考英語", "學測英文"][ei], "年度": y, "題號": q["n"], "題組": g["a"] if g else "",
                         "考點": lab, "答案": "非選" if ns else a, "能力": it[5], "陷阱": it[6],
                         "策略": strategy(ei, lab, it[5], it[7]), "判讀提示": it[7],
                         "題目文字": _clean(q.get("t")), "題組選文": _clean(g["t"])[:3000] if g else ""})
    out = R / "data" / "items.csv"
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    print(len(rows), "題 →", out)
    for ex in ("會考英語", "學測英文"):
        c = Counter(r["策略"] for r in rows if r["考試"] == ex)
        print(ex, sorted(c.items(), key=lambda kv: int(kv[0][1:])))


if __name__ == "__main__":
    main()
