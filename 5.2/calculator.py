import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def compute(target: str, ax, no_y=False):
    times, cv_values = [], []

    for i in range(1, 96, 4):  # 15-min steps: 1,5,9…
        fname = f"./data/fuzzbench-z-{i}.csv"
        if not os.path.exists(fname):
            continue

        df = pd.read_csv(fname)

        subset = df.loc[
            (df["target"] == target)
            & (df["config"].isin([f"aflplusplus_fixseed{j}" for j in range(1, 6)])),
            "execs_done",
        ]
        if subset.empty:
            continue

        mean, std = subset.mean(), subset.std()
        cv = (std / mean) * 100 if mean else float("inf")

        times.append(i * 15 / 60)  # convert to hours
        cv_values.append(cv)

    ax.plot(times, cv_values, marker="o")
    ax.set_title(f"{target}", fontsize=26)
    ax.set_xlabel("Time (hours)", fontsize=22)
    if not no_y:
        ax.set_ylabel("Coefficient of Variation (%)", fontsize=22)

    ax.set_xticks(np.arange(0, 24, 2))  # ticks from 0 to 23 with step 2
    ax.set_xlim(0, 23)                  # ensure the plot covers full range
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.grid(True)

# -------- driver code: 1 × 2 figure --------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

compute("bloaty_fuzz_target",            axes[0])
compute("lcms_cms_transform_fuzzer",     axes[1], no_y=True)

fig.tight_layout()
fig.savefig("combined.pdf")
