"""
情境化AI決策支援研究 — 正式結構方程模型(SEM)分析
============================================================
用途：驗證性因素分析(CFA) + 結構路徑模型，取代/補充 analyze_experiment.py 中的
      階層迴歸示意，提供正式論文所需的模型適配度指標(CFI/TLI/RMSEA/SRMR)與
      標準化路徑係數。

資料來源：預設讀取 simulated_sessions.csv（模擬資料，僅供流程驗證）。
          正式資料蒐集完成後，將 --csv 參數指向 web/ 原型匯出的 all_sessions.csv
          （欄位需含 group, understand_1-3, quality_1-3, trust_1-4, adopt_1-3）即可直接套用。

因設計限制（AI信任構念僅於B組蒐集），拆成兩個模型：
  模型一（全樣本 N≈160）：AI決策資訊品質(組別) → 資訊理解 → 感知決策品質 → 決策採用意願
                          （檢定 H1、H5部分路徑，不含信任）
  模型二（僅B組 N≈80）：  資訊理解 → AI信任 → 感知決策品質 → 決策採用意願
                          （檢定 H2、H3、H4、H5完整路徑）
"""
import argparse
import numpy as np
import pandas as pd
from semopy import Model, calc_stats

parser = argparse.ArgumentParser()
parser.add_argument("--csv", default="simulated_sessions.csv",
                     help="受測資料CSV路徑（預設用模擬資料，需與此腳本放在同一資料夾或給完整路徑）")
parser.add_argument("--bootstrap", type=int, default=200,
                     help="間接效果 bootstrap 重抽次數（預設200，正式資料建議1000+）")
args = parser.parse_args()

df = pd.read_csv(args.csv)
df["group_b"] = (df["group"] == "B").astype(int)

UNDERSTAND_ITEMS = [f"understand_{i}" for i in range(1, 4)]
QUALITY_ITEMS = [f"quality_{i}" for i in range(1, 4)]
TRUST_ITEMS = [f"trust_{i}" for i in range(1, 5)]
ADOPT_ITEMS = [f"adopt_{i}" for i in range(1, 4)]

pd.set_option("display.width", 140)
pd.set_option("display.max_columns", 20)


def run_model(name, model_desc, data):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)
    model = Model(model_desc)
    res = model.fit(data)
    print(res)

    stats = calc_stats(model)
    cols = [c for c in ["chi2", "DoF", "chi2 p-value", "CFI", "TLI", "RMSEA", "SRMR", "AIC", "BIC"] if c in stats.index]
    print("\n模型適配度指標：")
    print(stats.loc[cols] if cols else stats)

    print("\n路徑係數（結構模型部分）：")
    ins = model.inspect()
    structural = ins[ins["op"] == "~"]
    print(structural[["lval", "op", "rval", "Estimate", "Std. Err", "p-value"]].to_string(index=False))
    return model, ins


# ------------------------------------------------------------------
# 模型一：全樣本（N≈160）— H1 與 H5 的資訊理解→感知決策品質路徑
# ------------------------------------------------------------------
model1_desc = f"""
# 測量模型
Understand =~ {' + '.join(UNDERSTAND_ITEMS)}
Quality =~ {' + '.join(QUALITY_ITEMS)}
Adopt =~ {' + '.join(ADOPT_ITEMS)}

# 結構模型
Understand ~ group_b
Quality ~ Understand
Adopt ~ Understand + Quality
"""
model1, ins1 = run_model(
    "模型一：全樣本 AI決策資訊品質(組別) → 資訊理解 → 感知決策品質 → 決策採用意願",
    model1_desc, df
)

# ------------------------------------------------------------------
# 模型二：僅B組（N≈80）— H2、H3、H4、H5 完整路徑
# ------------------------------------------------------------------
df_b = df[df["group"] == "B"].copy()
model2_desc = f"""
# 測量模型
Understand =~ {' + '.join(UNDERSTAND_ITEMS)}
Trust =~ {' + '.join(TRUST_ITEMS)}
Quality =~ {' + '.join(QUALITY_ITEMS)}
Adopt =~ {' + '.join(ADOPT_ITEMS)}

# 結構模型
Trust ~ Understand
Quality ~ Understand + Trust
Adopt ~ Trust + Quality + Understand
"""
model2, ins2 = run_model(
    "模型二：B組 資訊理解 → AI信任 → 感知決策品質 → 決策採用意願（H2/H3/H4/H5）",
    model2_desc, df_b
)


# ------------------------------------------------------------------
# H5 間接效果 bootstrap（模型二：Understand → Trust → Adopt，
#                                 Understand → Trust → Quality → Adopt）
# ------------------------------------------------------------------
def get_path(ins, lval, rval):
    row = ins[(ins["lval"] == lval) & (ins["rval"] == rval) & (ins["op"] == "~")]
    return float(row["Estimate"].iloc[0]) if len(row) else np.nan


def indirect_effects(ins):
    a = get_path(ins, "Trust", "Understand")       # Understand -> Trust
    b = get_path(ins, "Adopt", "Trust")             # Trust -> Adopt
    c = get_path(ins, "Quality", "Trust")           # Trust -> Quality
    d = get_path(ins, "Adopt", "Quality")           # Quality -> Adopt
    ind1 = a * b            # Understand -> Trust -> Adopt
    ind2 = a * c * d        # Understand -> Trust -> Quality -> Adopt
    return ind1, ind2


print("\n" + "=" * 70)
print(f"H5 間接效果 Bootstrap（{args.bootstrap} 次重抽，僅B組資料）")
print("=" * 70)

boot_ind1, boot_ind2 = [], []
n = len(df_b)
rng = np.random.default_rng(42)
for i in range(args.bootstrap):
    sample = df_b.iloc[rng.integers(0, n, n)].reset_index(drop=True)
    try:
        m = Model(model2_desc)
        m.fit(sample)
        ins_b = m.inspect()
        i1, i2 = indirect_effects(ins_b)
        if np.isfinite(i1) and np.isfinite(i2):
            boot_ind1.append(i1)
            boot_ind2.append(i2)
    except Exception:
        continue  # 個別重抽樣本可能不收斂，略過

if boot_ind1:
    ci1 = np.percentile(boot_ind1, [2.5, 97.5])
    ci2 = np.percentile(boot_ind2, [2.5, 97.5])
    print(f"成功收斂重抽次數：{len(boot_ind1)} / {args.bootstrap}")
    print(f"間接效果 Understand→Trust→Adopt：           點估計={np.mean(boot_ind1):.3f}  95% CI=[{ci1[0]:.3f}, {ci1[1]:.3f}]"
          f"  {'顯著（不含0）' if ci1[0]*ci1[1] > 0 else '不顯著（CI含0）'}")
    print(f"間接效果 Understand→Trust→Quality→Adopt：    點估計={np.mean(boot_ind2):.3f}  95% CI=[{ci2[0]:.3f}, {ci2[1]:.3f}]"
          f"  {'顯著（不含0）' if ci2[0]*ci2[1] > 0 else '不顯著（CI含0）'}")
else:
    print("Bootstrap未能收斂，建議正式資料量足夠後（B組建議至少n=80）重新執行。")

print("\n" + "=" * 70)
print("使用說明")
print("=" * 70)
print("""
1. 換上真實資料：python3 sem_model.py --csv path/to/all_sessions.csv --bootstrap 1000
2. 適配度判斷標準（一般建議）：CFI/TLI ≥ .90（佳 ≥ .95）、RMSEA ≤ .08（佳 ≤ .05）、SRMR ≤ .08
3. 若模型一/模型二適配不佳，優先檢查：
   - 題項是否需要刪除（觀察每題的因素負荷量 factor loading，見上方測量模型部分的路徑係數）
   - 樣本數是否足夠（模型二僅B組，若B組人數<50，SEM估計可能不穩定，改用階層迴歸示意即可）
4. 間接效果的bootstrap CI是H5「感知決策品質具中介效果」的正式統計證據，正式論文口試常被要求提供
""")
