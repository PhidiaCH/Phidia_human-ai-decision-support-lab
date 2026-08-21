"""
情境化AI決策支援研究 — 統計分析範例
輸入：與 vpo-ai-decision-experiment.html 匯出的 all_sessions.csv 同格式
這裡先用模擬資料展示分析流程，未來換成真實 CSV 即可直接套用。
"""
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

np.random.seed(42)
N = 160  # 對齊海報第7節的目標樣本數 160-200

# ---------- 1. 模擬資料 ----------
industries = np.random.choice(
    ['半導體／電子製造','傳統製造／機械／化工','金融／保險','零售／消費／服務業','科技／軟體','其他'],
    N, p=[.30,.15,.15,.15,.15,.10])
rank = np.random.choice(['協理／處長以上','經理／副理','其他'], N, p=[.35,.45,.20])
mfg_involved = np.isin(industries, ['半導體／電子製造','傳統製造／機械／化工']) | (np.random.rand(N) < 0.25)
scenario_type = np.where(mfg_involved, 'mfg', 'generic')
group = np.random.choice(['A','B'], N)
ai_experience = np.clip(np.random.normal(3.0, 1.0, N).round(), 1, 5)

# 效果設定：B組(有AI建議)在理解、信心、採用意願上平均較高，且B組更容易選擇「升級」
base_understand = np.random.normal(3.4, 0.9, N)
base_confidence  = np.random.normal(3.2, 0.9, N)
base_adopt       = np.random.normal(3.1, 1.0, N)

is_B = (group == 'B')
understand = np.clip((base_understand + is_B*0.55).round(), 1, 5).astype(int)
confidence = np.clip((base_confidence + is_B*0.65).round(), 1, 5).astype(int)
adopt      = np.clip((base_adopt + is_B*0.75).round(), 1, 5).astype(int)
trust      = np.where(is_B, np.clip(np.random.normal(3.6,0.8,N).round(),1,5).astype(int), np.nan)

# AI信任與使用經驗一起把「升級」機率往上拉
logit = -1.0 + is_B*0.9 + (ai_experience-3)*0.15 + (understand-3)*0.25
p_escalate = 1/(1+np.exp(-logit))
decision = np.where(np.random.rand(N) < p_escalate, 'yes', 'no')

read_sec = np.clip(np.random.normal(45,15,N) + is_B*12, 10, None).round(1)
decide_sec = np.clip(np.random.normal(30,10,N), 5, None).round(1)

df = pd.DataFrame({
    'session_id': [f'S{i:04d}' for i in range(N)],
    'industry': industries, 'rank': rank, 'mfg_involved': mfg_involved,
    'scenario_type': scenario_type, 'ai_experience': ai_experience,
    'group': group, 'decision': decision,
    'understand': understand, 'confidence': confidence, 'trust': trust, 'adopt': adopt,
    'read_sec': read_sec, 'decide_sec': decide_sec,
})
df.to_csv('/mnt/user-data/outputs/simulated_sessions.csv', index=False)
print(f"模擬樣本數: {N}　A組: {(group=='A').sum()}　B組: {(group=='B').sum()}\n")

# ---------- 2. 獨立樣本 t-test：A組 vs B組 ----------
print("="*60)
print("獨立樣本 t-test（A組 vs B組）")
print("="*60)
for col in ['understand','confidence','adopt']:
    a = df.loc[df.group=='A', col]
    b = df.loc[df.group=='B', col]
    t, p = stats.ttest_ind(b, a, equal_var=False)
    d = (b.mean()-a.mean()) / np.sqrt((b.var()+a.var())/2)  # Cohen's d
    sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'n.s.'
    print(f"{col:12s}  A平均={a.mean():.2f}  B平均={b.mean():.2f}  "
          f"t={t:6.2f}  p={p:.4f} {sig}   Cohen's d={d:.2f}")

# ---------- 3. 卡方檢定：決策(升級/不升級) × 組別 ----------
print("\n" + "="*60)
print("卡方檢定：是否升級 × 組別")
print("="*60)
ct = pd.crosstab(df.group, df.decision)
chi2, p, dof, _ = stats.chi2_contingency(ct)
print(ct)
print(f"chi2={chi2:.2f}  p={p:.4f}")

# ---------- 4. 二因子 ANOVA：組別 × 情境類型 對 採用意願的影響 ----------
print("\n" + "="*60)
print("二因子 ANOVA：group × scenario_type → adopt")
print("="*60)
model = ols('adopt ~ C(group) * C(scenario_type)', data=df).fit()
aov = sm.stats.anova_lm(model, typ=2)
print(aov.round(4))

# ---------- 5. 迴歸：AI信任 是否中介 資訊理解→採用意願（B組子樣本） ----------
print("\n" + "="*60)
print("路徑檢定示意（僅B組，因trust只在B組蒐集）")
print("="*60)
dfb = df[df.group=='B'].copy()
step1 = ols('trust ~ understand', data=dfb).fit()
step2 = ols('adopt ~ understand + trust', data=dfb).fit()
print("Step1  understand → trust      係數=%.3f  p=%.4f" % (step1.params['understand'], step1.pvalues['understand']))
print("Step2  understand → adopt(控制trust)  係數=%.3f  p=%.4f" % (step2.params['understand'], step2.pvalues['understand']))
print("Step2  trust → adopt           係數=%.3f  p=%.4f" % (step2.params['trust'], step2.pvalues['trust']))
print("\n(正式SEM需用 lavaan/semopy 跑完整路徑模型與適配度指標，這裡先用階層迴歸示意中介效果方向)")

print("\n模擬資料已輸出：/mnt/user-data/outputs/simulated_sessions.csv")
