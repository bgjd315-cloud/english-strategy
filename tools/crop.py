#!/usr/bin/env python3
"""依 ../english-reading 的試卷圖片與裁切範圍，產生 picks.py 選用題目的圖片。

output/img/<id>-q.png：題目（文意選填等沒有獨立題目範圍的題目不產生）
output/img/<題組代號>-g.png：題組選文（同一題組只產生一次）
會考英語的裁切有裁切框與白色遮罩（隱藏同頁的其他題目），學測只有上下範圍。
"""
import json
import sys
from pathlib import Path

from PIL import Image

R = Path(__file__).resolve().parents[1]
SRC = R.parent / "english-reading"
sys.path.insert(0, str(SRC / "tools"))
sys.path.insert(0, str(R / "tools"))
from picks import PICKS  # noqa: E402
from reading_data import build_practice  # noqa: E402

OUT = R / "output" / "img"
_cache = {}


def page(ei, y, p):
    f = SRC / "assets" / (f"english/eng-pages/{y}-R-{p}.webp" if ei == 0 else f"xuece-en/pages/{y}-{p}.webp")
    if f not in _cache:
        _cache[f] = Image.open(f).convert("RGB")
    return _cache[f]


def render(ei, y, slices, pg):
    W, H, x0, xw = pg
    parts = []
    for p, a, b, clips, masks in slices:
        im = page(ei, y, p)
        s = im.width / W
        box = [round(v * s) for v in (x0, a, x0 + xw, b)]
        if clips:
            out = Image.new("RGB", (box[2] - box[0], box[3] - box[1]), "white")
            for x, yy, w, h in clips:
                c = [round(v * s) for v in (x, yy, x + w, yy + h)]
                c = [max(c[0], box[0]), max(c[1], box[1]), min(c[2], box[2]), min(c[3], box[3])]
                if c[2] > c[0] and c[3] > c[1]:
                    out.paste(im.crop(c), (c[0] - box[0], c[1] - box[1]))
            for x, yy, w, h in masks:
                m = [round(v * s) for v in (x - x0, yy - a, x - x0 + w, yy - a + h)]
                out.paste("white", m)
        else:
            out = im.crop(box)
        parts.append(out)
    total = Image.new("RGB", (max(p.width for p in parts), sum(p.height for p in parts)), "white")
    yy = 0
    for p in parts:
        total.paste(p, (0, yy))
        yy += p.height
    return total


def main():
    P = build_practice(SRC)
    items = {(("K" if it[0] == 0 else "X") + f"{it[1]}-{it[2]}"): it for it in P["items"]}
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {}
    for ids in PICKS.values():
        for i in ids:
            it = items[i]
            ei, y, gid = it[0], it[1], it[9]
            pg = P["pages"][f"{ei}-{y}"]
            m = {"nopt": it[10], "group": gid}
            if it[8]:
                render(ei, y, it[8], pg).save(OUT / f"{i}-q.png", optimize=True)
                m["q"] = f"{i}-q.png"
            if gid:
                gname = f"{'K' if ei == 0 else 'X'}{y}-g{gid.split('-')[2]}-g.png"
                if not (OUT / gname).exists():
                    render(ei, y, P["groups"][gid], pg).save(OUT / gname, optimize=True)
                m["g"] = gname
            meta[i] = m
    (R / "data" / "picks_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), "utf-8")
    print(len(meta), "題，圖片在", OUT)


if __name__ == "__main__":
    main()
