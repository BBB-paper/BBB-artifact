import pandas as pd
import sys

if len(sys.argv) != 2:
    print("Usage: python3 cv_qcd.py <choice>")
    exit(0)

choice = int(sys.argv[1])
cols_ignore = ["core_number"]
#void

if choice == 2:
    df1 = pd.read_csv("./c2.csv")
elif choice == 1:
    df1 = pd.read_csv("./c1.csv")
elif choice == 3:
    df1 = pd.read_csv("./c3.csv")
elif choice == 4:
    df1 = pd.read_csv("./c4.csv")
else:
    print("Choice wrong")
    exit(0)

df = pd.concat([df1], ignore_index=True)
df = df.drop(columns=cols_ignore)

chosen_config = ""
if choice == 4:
    # remote normal
    chosen_config = ['aflplusplus_toka1', 'aflplusplus_toka2', 'aflplusplus_toka3', 'aflplusplus_toka4', 'aflplusplus_toka5']
elif choice == 3:
    # remote fixed
    chosen_config = ['aflplusplus_fixseed1', 'aflplusplus_fixseed2', 'aflplusplus_fixseed3', 'aflplusplus_fixseed4', 'aflplusplus_fixseed5']
else:
    chosen_config = ['aflplusplus_nothing1', 'aflplusplus_nothing2', 'aflplusplus_nothing3', 'aflplusplus_nothing4', 'aflplusplus_nothing5']

df = df[df['config'].isin(chosen_config)]

print(df)
# ──────────────────────────────────────────────
# 2. Compute stats
# ──────────────────────────────────────────────
stats = (
    df.groupby("target")["execs_done"]
      .agg(n="size",                      # how many rows
           mean="mean",
           std="std",
           min="min",
           max="max",
           q1=lambda x: x.quantile(0.25),
           q3=lambda x: x.quantile(0.75))
      .reset_index()
)

stats["cv_pct"]  = (stats["std"] / stats["mean"]) * 100
stats["qcd_pct"] = ((stats["q3"] - stats["q1"]) /
                    (stats["q3"] + stats["q1"]) * 100)
# Keep required columns & tidy up
tbl = stats[["target", "n", "mean", "cv_pct", "qcd_pct", "min", "max"]].copy()
tbl["mean"] = (tbl["mean"] / 1e6).round(0).astype(int)      # millions
tbl["min"] = (tbl["min"] / 1e6).round(0).astype(int)      # millions
tbl["max"] = (tbl["max"] / 1e6).round(0).astype(int)      # millions
tbl = tbl.round({"cv_pct": 2, "qcd_pct": 2})
tbl = tbl.sort_values("target")            # optional

# ──────────────────────────────────────────────
# 3. Export to LaTeX
# ──────────────────────────────────────────────
latex_code = tbl.to_latex(index=False,
                          column_format="lrrr",   # left + 3 right-aligned
                          float_format="%.2f",
                          caption="Throughput variability per target.",
                          label="tab:throughput_stats",
                          escape=True)

print("LaTeX table written to throughput_mean_cv_iqr.tex")
print("\nPreview:\n")
print(latex_code)
