"""一次性：由 guowen-strategy/tools/student.py 改寫成英文版 tools/student.py。"""
from pathlib import Path

R = Path(__file__).resolve().parents[1]
s = (R.parent / "guowen-strategy" / "tools" / "student.py").read_text("utf-8")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)


rep('"""產生學生版互動網站', '"""產生英文閱讀理解策略的學生版互動網站')
rep('import shutil\n', 'import shutil\n')
rep('from pathlib import Path\n', 'from pathlib import Path\n\nfrom PIL import Image\n')
rep('''    x["id"] = ("K" if x["考試"] == "會考國文" else "X") + x["年度"] + "-" + x["題號"]''',
    '''    x["id"] = ("K" if x["考試"] == "會考英語" else "X") + x["年度"] + "-" + x["題號"]''')
rep('''def group(x):
    if x["考試"] == "會考國文":
        return "會考"
    return "學測舊" if int(x["年度"]) <= 110 else "學測新"''', '''def group(x):
    return "會考" if x["考試"] == "會考英語" else "學測"''')
rep('''N = Counter(group(x) for x in ITEMS)''', '''N = Counter(group(x) for x in ITEMS)
META = json.loads((R / "data" / "picks_meta.json").read_text("utf-8"))''')
rep('''        strats.append({"code": code, "name": st["name"],''', '''        strats.append({"code": code, "name": st["name"], "en": st["en"],''')
rep('''            opts = "ABCDE" if multi or "(E)" in x["題目文字"] else "ABCD"
            qs[i] = {"src": f"{x['考試']} {x['年度']} 年第 {x['題號']} 題", "ans": ans, "opts": opts, "multi": multi,
                     "why": EXPLAIN[i]["why"], "demo": EXPLAIN[i].get("demo", []), "img": f"img/{i}-q.png"}''',
    '''            m = META[i]
            kind = x["考點"].split("：")[0]
            qs[i] = {"src": f"{x['考試']} {x['年度']} 年第 {x['題號']} 題", "kind": kind, "no": x["題號"], "ans": ans,
                     "opts": "ABCDEFGHIJ"[:m["nopt"]], "multi": multi, "why": EXPLAIN[i]["why"], "demo": EXPLAIN[i].get("demo", []),
                     "img": f"img/{webp(m['q'])}" if m.get("q") else "", "g": f"img/{webp(m['g'])}" if m.get("g") else ""}''')
rep('''CSS = """''', '''def webp(name):
    return name.rsplit(".", 1)[0] + ".webp"


CSS = """''')
# 題組選文：可收合
rep('''.q img{display:block;''', '''details.passage{border:1px solid var(--rule);border-radius:8px;padding:8px 10px;background:var(--paper)}
details.passage summary{cursor:pointer;font-weight:700;font-size:15px}
details.passage img{margin-top:8px}
.blank{font-weight:700;color:var(--accent)}
.en{font-family:Georgia,"Times New Roman",serif;font-style:italic;color:var(--ink-3);font-weight:400}
.q img{display:block;''')
rep('''  return `<div class="q" data-q="${id}"><img src="${q.img}" alt="${esc(q.src)}" loading="lazy">${opt.mid||""}''',
    '''  const passage=q.g?`<details class="passage" open><summary>閱讀文章（題組共用，可收合）</summary><img src="${q.g}" alt="${esc(q.src)} 題組文章" loading="lazy"></details>`:"";
  const stem=q.img?`<img src="${q.img}" alt="${esc(q.src)}" loading="lazy">`:`<p>請作答文章中的第 <span class="blank">${q.no}</span> 題空格（${esc(q.kind)}）。</p>`;
  return `<div class="q" data-q="${id}">${passage}${stem}${opt.mid||""}''')
rep('''<p class="sub">${q.multi?"多選題：選出所有正確的選項，再按「確認答案」。":"單選題：選一個答案，再按「確認答案」。"}</p>''',
    '''<p class="sub">${q.multi?"多選題：選出所有正確的選項，再按「確認答案」。":q.opts.length>5?"從文章下方的 (A)–(J) 選一個字，再按「確認答案」。":"單選題：選一個答案，再按「確認答案」。"}</p>''')
rep('''.opt{font:inherit;font-size:18px;font-weight:700;width:52px;height:46px;''', '''.opt{font:inherit;font-size:18px;font-weight:700;width:48px;height:46px;''')
# 學測百分比
s = s.replace('s.pct["學測新"]', 's.pct["學測"]')
rep('（會考 ${s.pct["會考"]}%、學測 108 課綱 ${s.pct["學測"]}%）', '（會考 ${s.pct["會考"]}%、學測 ${s.pct["學測"]}%）')
# 策略名稱加英文
rep('''<h2>${esc(s.name)}</h2><p><b>${esc(s.one)}</b></p>''', '''<h2>${esc(s.name)} <span class="en">${esc(s.en)}</span></h2><p><b>${esc(s.one)}</b></p>''')
rep('''<h2>${s.code} ${esc(s.name)}</h2>''', '''<h2>${s.code} ${esc(s.name)} <span class="en">${esc(s.en)}</span></h2>''')
rep('''<p class="kicker">${s.code}</p><h3>${esc(s.name)}</h3>''', '''<p class="kicker">${s.code}・${esc(s.en)}</p><h3>${esc(s.name)}</h3>''')
rep('const KEY="guowen-strategy-v1";', 'const KEY="english-strategy-v1";')
rep('''FOOTER = ('<footer><p><b>著作權與來源說明</b>　本站收錄的國中教育會考與大學學測試題''', '''FOOTER = ('<footer><p><b>著作權與來源說明</b>　本站收錄的國中教育會考英語與大學學測英文試題''')
# 圖片：轉成 webp
rep('''    for ids in PICKS.values():
        for i in ids:
            shutil.copy(R / "output" / "img" / f"{i}-q.png", OUT / "img")''', '''    for f in sorted((R / "output" / "img").glob("*.png")):
        Image.open(f).save(OUT / "img" / webp(f.name), "WEBP", quality=80, method=6)''')
rep('''    page("index.html", "國文閱讀理解策略", \'\'\'<header class="hero"><p class="kicker">會考國文・學測國文</p><h1>國文閱讀理解策略</h1>
<p>把會考和學測國文的閱讀題整理成 12 種閱讀策略。''', '''    page("index.html", "英文閱讀理解策略", \'\'\'<header class="hero"><p class="kicker">會考英語・學測英文</p><h1>英文閱讀理解策略</h1>
<p>把會考英語閱讀和學測英文的題目整理成 12 種閱讀策略。''')
rep('''<p class="sub">題目取自會考國文 111–115 年與學測國文 107–115 年。''', '''<p class="sub">題目取自會考英語閱讀 111–115 年與學測英文 107–115 年（共 688 題）。''')
rep('''    page("handbook.html", "閱讀策略手冊",''', '''    page("handbook.html", "英文閱讀策略手冊",''')
rep('''<h1>閱讀策略手冊</h1>''', '''<h1>英文閱讀策略手冊</h1>''')
rep('''    page("worksheets.html", "學習單",''', '''    page("worksheets.html", "英文策略學習單",''')
rep('''    page("report.html", "我的分析報告",''', '''    page("report.html", "我的英文閱讀分析報告",''')
assert "國文" not in s, [l for l in s.splitlines() if "國文" in l]
(R / "tools" / "student.py").write_text(s, "utf-8", newline="\n")
print("ok")
