"""一次性：把首頁說明換成只連國文、英文網站的版本。"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2]
src = (DOCS / "english-strategy" / "notes" / "add_guide.py").read_text("utf-8")
ns = {"Path": Path, "__file__": str(DOCS / "english-strategy" / "notes" / "add_guide.py")}
exec(src.split("ANCHOR =")[0], ns)
G = ns["GUIDE"]
for repo in ("guowen-strategy", "english-strategy"):
    p = DOCS / repo / "tools" / "student.py"
    s = p.read_text("utf-8")
    i = s.index('\n<section class="card" style="margin-top:28px">')
    j = s.index("</section>", i) + len("</section>")
    s = s[:i] + G + s[j:]
    assert s.count("兩種網站怎麼用") == 1 and "math-literacy" not in s and "exam-portal" not in s
    p.write_text(s, "utf-8", newline="\n")
    print("ok", repo)
