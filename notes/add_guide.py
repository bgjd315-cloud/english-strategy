"""一次性：在國文、英文策略網站首頁加上「兩種網站怎麼用」的說明與連結。"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2]
U = "https://bgjd315-cloud.github.io/"
GUIDE = f'''
<section class="card" style="margin-top:28px"><p class="kicker">搭配使用</p><h2>兩種網站怎麼用？</h2>
<p>老師準備了兩種網站，用的都是會考和學測的歷屆題目，但用途不一樣。</p>
<h3>閱讀策略網站：學方法</h3>
<ul><li>國文：<a href="{U}guowen-strategy/">{U}guowen-strategy/</a></li><li>英文：<a href="{U}english-strategy/">{U}english-strategy/</a></li></ul>
<p>把「回原文找證據、從上下文猜字義、找出言外之意」等讀法整理成 12 種閱讀策略：先讀手冊學方法，再做學習單練習（答案與解析按鍵才出現），最後看分析報告，了解自己的強項和需要加強的地方。</p>
<h3>判讀網站：大量練習</h3>
<ul><li>國文：<a href="{U}guowen-reading/">{U}guowen-reading/</a></li><li>英文：<a href="{U}english-reading/">{U}english-reading/</a></li></ul>
<p>收錄全部歷屆題目，每一題都標出在考什麼能力、陷阱在哪裡。學會方法以後，到這裡多做題目，看看自己能不能把策略用出來。</p>
<p><b>建議的順序：</b>先到策略網站學方法、打好基本功，再到判讀網站多練習。</p></section>'''
ANCHOR = '<button type="button" class="btn ghost" id="reset">清除我的作答紀錄</button></div>'

for repo in ("guowen-strategy", "english-strategy"):
    p = DOCS / repo / "tools" / "student.py"
    s = p.read_text("utf-8")
    assert s.count(ANCHOR) == 1 and "兩種網站怎麼用" not in s, repo
    s = s.replace(ANCHOR, ANCHOR + GUIDE.replace("\\", "\\\\"))
    s = s.replace(".tile h3{font-size:18px}", ".tile h3{font-size:18px}\nsection.card a{overflow-wrap:anywhere}")
    p.write_text(s, "utf-8", newline="\n")
    print("ok", repo)
