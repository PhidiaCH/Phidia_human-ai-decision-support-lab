# Human-AI Decision Support Lab

EMBA 碩士論文研究專案：**情境化AI決策支援對智慧製造管理者資訊理解、信任與決策採用意願之影響**
指導教師：徐立群

## 專案結構

```
web/        受測實驗原型（A/B介面，含製造情境／通用情境分流，多題項構念量表）
analysis/   統計分析腳本（信度、t-test、ANOVA、卡方檢定、中介路徑示意）
docs/       研究計畫PPT、文獻探討、操作型定義、專家內容效度審查表
```

## docs/ 內容

- `thesis_proposal_v1.pptx` — 完整提案簡報（22頁：背景、文獻、架構、方法、先導測試、時程）
- `literature_review.md` — 文獻探討完整版（4理論脈絡＋16篇文獻，含研究定位）
- `operational_definitions.md` — 研究架構、各構念操作型定義、題項、信效度標準
- `content_validity_review.md` — 專家內容效度審查表（正式施測前使用，含CVI計算方式）

## 研究架構

AI決策資訊品質(情境化) → 資訊理解 → AI信任 → 決策採用意願，
感知決策品質作為AI信任與決策採用意願間的中介。

- H1：AI決策資訊品質(情境化)正向影響資訊理解
- H2：資訊理解正向影響AI信任
- H3：AI信任正向影響決策採用意願／行動意願
- H4：資訊理解正向影響決策採用意願／行動意願（穩健性檢定）
- H5：資訊理解與AI信任透過感知決策品質間接影響決策採用意願／行動意願

## 實驗設計

2 (組別：一般資訊 A／情境化AI決策支援 B) × 2 (情境：製造 mfg／通用 generic) 受測者間設計。
受測者為EMBA高階主管，背景題含產業別、職級、AI使用經驗。

## 使用方式

1. 專家內容效度審查：先用 `docs/content_validity_review.md` 邀請3-5位專家評分，依意見修正題項
2. 開啟 `web/vpo-ai-decision-experiment.html`（可直接部署到GitHub Pages或Vercel發連結給受測者）
3. 受測完成後，用頁面下方「研究者面板」下載彙整CSV
4. 將CSV放進 `analysis/`，執行 `python3 analysis/analyze_experiment.py` 進行統計分析（含Cronbach's α）

## 待辦

- [ ] 專家內容效度審查（3-5位）並依CVI結果修正題項
- [ ] 10-15人小樣本前測，檢查填答時間與初步信度
- [ ] 正式SEM模型驗證（建議用 lavaan 或 semopy）
- [ ] 正式資料蒐集啟動（目標160-200份）
- [ ] 文獻探討擴充至30-50篇規模，補充在地實證研究
