# 英文閱讀理解策略・學生版

用會考英語閱讀（111–115 年）與學測英文（107–115 年）共 688 題，整理成 12 種英文閱讀策略的互動練習網站。只有學生版，沒有教師資料。

## 資料夾

| 路徑 | 內容 |
|---|---|
| `data/items.csv` | 688 題：考試、年度、題號、題組、考點、答案、能力、陷阱、策略、判讀提示、題目文字、題組選文（UTF-8，可用 Excel 開啟） |
| `data/picks_meta.json` | 選用題目的選項數與圖片檔名（由 crop.py 產生） |
| `tools/export.py` | 由 ../english-reading 的題目與逐題判讀，依規則標上策略 E1–E12，輸出 items.csv |
| `tools/picks.py` | 每種策略選用的三題（第一題是學習單的示範題） |
| `tools/content.py` | 12 種策略的說明與 36 題的解析 |
| `tools/crop.py` | 從 ../english-reading 的試卷圖片裁切題目與題組文章（output/img，不提交） |
| `tools/student.py` | 產生學生版互動網站（output/student） |
| `tools/candidates.py` | 列出每種策略可選的題目（notes/candidates.txt） |

## 12 種策略與分類規則

E1 掃讀找細節、E2 略讀抓主旨、E3 上下文猜字義、E4 指涉與同義改寫、E5 推論言外之意、E6 作者目的與態度、E7 篇章結構與轉折、E8 圖表與實用文本、E9 詞性先篩選字、E10 語境線索選字、E11 克漏字通篇理解、E12 句型與文法。

策略由 english-reading 的逐題判讀推得：閱讀題依 PISA 能力（A1→E1、B3→E2、A2→E3、B1→E4、B2→E5、C2→E6、B5→E7、B4→E8；C1 談結構順序的歸 E7，其餘歸 E6），字彙題依題型（文意選填→E9、詞彙／字彙→E10、綜合測驗／克漏字→E11），語法題（K2）→E12。分類與解析為本站判讀，不是官方分類。

## 重新產生網站

```bash
python tools/export.py    # 需要 ../english-reading
python tools/crop.py      # 需要 ../english-reading/assets
python tools/student.py
```

推送到 GitHub 後，由 GitHub Actions 把 `output/student/` 發布到 GitHub Pages。這個 repo 是公開的，只放學生看得到的內容。網站不連到其他判讀網站或入口頁。
