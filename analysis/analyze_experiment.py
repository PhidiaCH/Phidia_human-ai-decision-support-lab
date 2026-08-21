"""
情境化AI決策支援研究 — 統計分析範例（多題項構念版）
輸入：與 web/vpo-ai-decision-experiment.html 匯出的 all_sessions.csv 同格式
（欄位含 understand_1..3, quality_1..3, trust_1..4, adopt_1..3 等題項級資料）
這裡先用模擬資料展示分析流程，未來換成真實 CSV 即可直接套用。
"""
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

np.random.seed(42)
N = 160  # 對齊海報第7節的目標樣本數 160-200

def cronbach_alpha(item_df):
    """item_df: 每欄一個題項，每列一位受測者"""
    item_df = item_df.dropna()
    k = item_df.shape[1]
    item_var = item_df.var(axis=0, ddof=1).sum()
    total_var = item_df.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_var / total_var)

# ---------- 1. 模擬題項級資料 ----------
industries = np.random.choice(
    ['半導體／電子製造','傳統製造／機械／化工','金融／保險','零售／消費／服務業','科技／軟體','其他'],
    N, p=[.30,.15,.15,.15,.15,.10])
rank = np.random.choice(['協理／處長以上','經理／副理','其他'], N, p=[.35,.45,.20])
mfg_involved = np.isin(industries, ['半導體／電子製造','傳統製造／機械／化工']) | (np.random.rand(N) < 0.25)
scenario_type = np.where(mfg_involved, 'mfg', 'generic')
group = np.random.choice(['A','B'], N)
ai_experience = np.clip(np.random.normal(3.0, 1.0, N).round(), 1, 5)
is_B = (group == 'B')

def gen_items(n_items, base_mean, group_boost, noise=0.6):
    latent = np.random.normal(base_mean, 0.8, N) + is_B*group_boost
    items = np.clip((latent[:,None] + np.random.normal(0, noise, (N, n_items))).round(), 1, 5)
    return items.astype(int)

understand_items = gen_items(3, 3.3, 0.5)
quality_items    = gen_items(3, 3.2, 0.6)
trust_items      = gen_items(4, 3.4, 0.0)
adopt_items      = gen_items(3, 3.1, 0.7)

df = pd.DataFrame({
    'session_id': [f'S{i:04d}' for i in range(N)],
    'industry': industries, 'rank': rank, 'mfg_involved': mfg_involved,
    'scenario_type': scenario_type, 'ai_experience': ai_experience,
    'group': group,
})
for i in range(3):
    df[f'understand_{i+1}'] = understand_items[:, i]
    df[f'quality_{i+1}'] = quality_items[:, i]
    df[f'adopt_{i+1}'] = adopt_items[:, i]
for i in range(4):
    df[f'trust_{i+1}'] = np.where(is_B, trust_items[:, i], np.nan)

df['understand_mean'] = df[[f'understand_{i+1}' for i in range(3)]].mean(axis=1)
df['quality_mean'] = df[[f'quality_{i+1}' for i in range(3)]].mean(axis=1)
df['adopt_mean'] = df[[f'adopt_{i+1}' for i in range(3)]].mean(axis=1)
df['trust_mean'] = df[[f'trust_{i+1}' for i in range(4)]].mean(axis=1)

df['confidence'] = np.clip(np.random.normal(3.2, 0.9, N) + is_B*0.5, 1, 5).round().astype(int)
logit = -1.0 + is_B*0.9 + (ai_experience-3)*0.15 + (df['understand_mean']-3)*0.25
p_escalate = 1/(1+np.exp(-logit))
df['decision'] = np.where(np.random.rand(N) < p_escalate, 'yes', 'no')
df['read_sec'] = np.clip(np.random.normal(45,15,N) + is_B*12, 10, None).round(1)
df['decide_sec'] = np.clip(np.random.normal(30,10,N), 5, None).round(1)

df.to_csv('/mnt/user-data/outputs/simulated_sessions.csv', index=False)
print(f"模擬樣本數: {N}　A組: {(group=='A').sum()}　B組: {(group=='B').sum()}\n")

# ---------- 2. 信度分析：Cronbach's alpha ----------
print("="*60)
print("信度分析（Cronbach's alpha，各構念題項內部一致性）")
print("="*60)
print(f"資訊理解（3題）  alpha = {cronbach_alpha(df[[f'understand_{i+1}' for i in range(3)]]):.3f}")
print(f"感知決策品質（3題）  alpha = {cronbach_alpha(df[[f'quality_{i+1}' for i in range(3)]]):.3f}")
print(f"AI信任（4題，僅B組）  alpha = {cronbach_alpha(df.loc[df.group=='B', [f'trust_{i+1}' for i in range(4)]]):.3f}")
print(f"決策採用意願（3題）  alpha = {cronbach_alpha(df[[f'adopt_{i+1}' for i in range(3)]]):.3f}")
print("（一般建議 alpha ≥ 0.70 為可接受，≥ 0.80 為良好）")

# ---------- 3. 獨立樣本 t-test：A組 vs B組（構念平均分數） ----------
print("\n" + "="*60)
print("獨立樣本 t-test（A組 vs B組，構念平均分數）")
print("="*60)
for col in ['understand_mean','quality_mean','adopt_mean']:
    a = df.loc[df.group=='A', col]
    b = df.loc[df.group=='B', col]
    t, p = stats.ttest_ind(b, a, equal_var=False)
    d = (b.mean()-a.mean()) / np.sqrt((b.var()+a.var())/2)
    sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'n.s.'
    print(f"{col:16s}  A平均={a.mean():.2f}  B平均={b.mean():.2f}  "
          f"t={t:6.2f}  p={p:.4f} {sig}   Cohen's d={d:.2f}")

# ---------- 4. 卡方檢定：決策 × 組別 ----------
print("\n" + "="*60)
print("卡方檢定：是否升級 × 組別")
print("="*60)
ct = pd.crosstab(df.group, df.decision)
chi2, p, dof, _ = stats.chi2_contingency(ct)
print(ct)
print(f"chi2={chi2:.2f}  p={p:.4f}")

# ---------- 5. 二因子 ANOVA：組別 × 情境類型 → 採用意願 ----------
print("\n" + "="*60)
print("二因子 ANOVA：group × scenario_type → adopt_mean")
print("="*60)
model = ols('adopt_mean ~ C(group) * C(scenario_type)', data=df).fit()
aov = sm.stats.anova_lm(model, typ=2)
print(aov.round(4))

# ---------- 6. 迴歸：資訊理解 → AI信任 → 決策採用意願（僅B組） ----------
print("\n" + "="*60)
print("路徑檢定示意（僅B組）：understand_mean → trust_mean → adopt_mean")
print("="*60)
dfb = df[df.group=='B'].copy()
step1 = ols('trust_mean ~ understand_mean', data=dfb).fit()
step2 = ols('adopt_mean ~ understand_mean + trust_mean', data=dfb).fit()
print("Step1  understand → trust      係數=%.3f  p=%.4f" % (step1.params['understand_mean'], step1.pvalues['understand_mean']))
print("Step2  understand → adopt(控制trust)  係數=%.3f  p=%.4f" % (step2.params['understand_mean'], step2.pvalues['understand_mean']))
print("Step2  trust → adopt           係數=%.3f  p=%.4f" % (step2.params['trust_mean'], step2.pvalues['trust_mean']))
print("\n(正式SEM需用 lavaan/semopy 跑完整路徑模型與適配度指標，這裡先用階層迴歸示意中介效果方向)")

print("\n模擬資料已輸出：/mnt/user-data/outputs/simulated_sessions.csv")
