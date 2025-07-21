#! /usr/bin/env python3

import numpy as np
import pandas as pd
import scipy.stats as st
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns
from matplotlib.colors import ListedColormap

from scipy.stats import norm
from math import sqrt

####################################################
df3 = pd.read_csv("../C1-4/c2.csv")
df4 = pd.read_csv("../C1-4/c1.csv")

print(df3['execs_done'].describe())
q1 = df3['execs_done'].quantile(0.25)
q3 = df3['execs_done'].quantile(0.75)
qcd = (q3 - q1) / (q3 + q1)

cv = df3['execs_done'].std()/df3['execs_done'].mean()
print(f"CV: {cv*100}, QCD (Quartile Coefficient of Dispersion): {qcd * 100} %\n\n")

alpha = 0.05

print("Normality of Class 2 experiments...")
stat, p = st.shapiro(df3['execs_done'])
print(f"Statistic: {stat}, p-value: {p}")
if p < alpha:
    print("NOT follow a normal distribution (reject H0).\n\n")
else:
    print("may follow a normal distribution (fail to reject H0).\n\n")

print(df4['execs_done'].describe())
q1 = df4['execs_done'].quantile(0.25)
q3 = df4['execs_done'].quantile(0.75)
qcd = (q3 - q1) / (q3 + q1)

cv = df4['execs_done'].std()/df4['execs_done'].mean()
print(f"CV: {cv*100},QCD (Quartile Coefficient of Dispersion): {qcd * 100} %\n\n")

print("\nNormality of Class 1 experiments...")
stat, p = st.shapiro(df4['execs_done'])
print(f"Statistic: {stat}, p-value: {p}")
if p < alpha:
    print("NOT follow a normal distribution (reject H0).")
else:
    print("may follow a normal distribution (fail to reject H0).")
    # Calculate skewness for both datasets
    skew_df3 = st.skew(df3['execs_done'])
    skew_df4 = st.skew(df4['execs_done'])

#####################################################
print("\n\n")

df2 = pd.read_csv("../C1-4/c3.csv")
df3 = pd.read_csv("../C1-4/c4.csv")

alpha = 0.05
for target in sorted(df2["target"].unique()):
    df22 = df2[df2["target"] == target]
    df32 = df3[df3["target"] == target]

    stat, p = mannwhitneyu(df22["execs_done"], df32["execs_done"], alternative='two-sided')
    if p < alpha:
        print(f"===> {target} distributions in class 3 and class 4 experiments ARE statistically different (reject H0).")
    else:
         print(f"{target} distributions in class 3 and class 4 experiments MAY are statistically equal (fail to reject H0).")

print("\n\n")
######################################################
# Cross comparison of Class 3 and Class 4 experiments (stable unstable targets)
s3 = [27.14, 25.80, 36.82, 23.37, 6.66, 4.18, 4.59, 26.15, 32.01, 15.46] # CV Class 3 stable targets
s4 = [12.64, 42.03, 44.92, 9.44, 10.81, 7.86, 2.91, 41.79, 30.87, 37.24] # CV Class 4 stable targets
i3 = [ 5.00, 6.44, 17.29, 12.18, 23.79, 9.19, 3.57, 10.56, 28.61, 130.25] # CV Class 3 unstable targets
i4 = [5.78, 10.09, 4.99, 22.27, 6.45, 20.72, 9.89, 10.21, 34.67, 106.77 ] # CV Class 4 unstable targets

l = [s3, s4, i3, i4]
for idx, i in enumerate(l):
    for idx2, j in enumerate(l[idx+1:], 1):
        stat, p = mannwhitneyu(i, j, alternative='two-sided')
        if p < alpha:
            print(f"{idx} - {idx2} are statistically different")
        else:
            print(f"{idx} - {idx2} may be statistically equal")
print("\n\n")

#########################################################

# Permit to calculate the ratio r/cv argument of PHI from N
def r_over_cv(n, alpha=0.05, beta=0.05):
    z_alpha = norm.ppf(1 - alpha)
    z_beta = norm.ppf(1- beta)
    z = z_alpha + z_beta
    A = 0.5 + z / np.sqrt(6 * n)
    return np.sqrt(2) * norm.ppf(A)

####################################################
# Plot curves figure 

lines = []
labels = []

cv_values = [0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.3, 0.5] # Noise

p = np.linspace(0.01, 0.11, 500) # Mean ratio

colors = ['#e41a1c',  # red
          '#377eb8',  # blue
          '#4daf4a',  # green
          '#ff7f00',  # orange
          '#984ea3',  # purple
          "#afaf31",  # yellow
          '#a65628',  # brown
          "#f70485"]  # pink
cmap = lambda idx: colors[idx]

plt.figure(figsize=(10, 6))

alpha = beta = 0.05
c = (norm.ppf(1 - alpha) + norm.ppf(1-beta))**2
for idx, cv in enumerate(cv_values):
    color = cmap(idx)
    
    r = (p/(cv * sqrt(2)))
    n = c/(6 * ((norm.cdf(r))-0.5)**2)

    line, = plt.plot(p * 100, n, label=f'{cv*100} %', color=color)
    lines.append(line)
    labels.append(f'{cv * 100} %')

plt.xlabel('Improvement ratio % (P)', fontsize=22)
plt.ylabel('N', fontsize=22)
plt.yscale('log')
plt.xlim(1, 11)
plt.ylim(10, max(n) + 100)
plt.axhline(y=20, color='black', linestyle='--', linewidth=1)
plt.legend(handles=lines[::-1], labels=labels[::-1], title='Noise ratios % (CV)', fontsize=16, title_fontsize=20, loc='upper right', ncol=4)
plt.grid(True)
plt.tight_layout()
plt.xticks(range(1,11,1), fontsize=18)
plt.yticks(fontsize=18)
plt.savefig("curves.pdf", format="pdf", bbox_inches="tight", dpi=300, facecolor=plt.gcf().get_facecolor())

#########################################################

# Minimum difference statistically detectable with 20 runs 
used_n = 20
st = [
    "bloaty_fuzz_target",
    "jsoncpp_jsoncpp_fuzzer",
    "lcms_cms_transform_fuzzer",
    "libjpeg-turbo_libjpeg_turbo_fuzzer",
    "libpng_libpng_read_fuzzer",
    "mbedtls_fuzz_dtlsclient",
    "openssl_x509",
    "vorbis_decode_fuzzer",
    "woff2_convert_woff2ttf_fuzzer",
    "zlib_zlib_uncompress_fuzzer"
]

ist = [
    "curl_curl_fuzzer_http",
    "freetype2_ftfuzzer",
    "harfbuzz_hb-shape-fuzzer",
    "libpcap_fuzz_both",
    "libxml2_xml",
    "libxslt_xpath",
    "openthread_ot-ip6-send-fuzzer",
    "proj4_proj_crs_to_crs_fuzzer",
    "re2_fuzzer",
    "sqlite3_ossfuzz",
]

cvs = np.array([12.64, 42.03, 44.92, 9.44, 10.81, 7.86, 2.91, 41.79, 30.87, 37.24]) # Stable targets CV
cvi = np.array([5.78, 10.09, 4.99, 22.27, 6.45, 20.72, 9.89, 10.21, 34.67, 106.77]) # Unstable targets CV

ps = r_over_cv(used_n) * cvs # P ratios for stable targets
pi = r_over_cv(used_n) * cvi # For unstable

print(f"Stable target with minimum difference statistical detectable: {st[ps.argmin()]}, percentage: {ps.min()}%")
print(f"Unstable target with minimum difference statistical detectable: {ist[pi.argmin()]}, percentage: {pi.min()}%")

print(f"Percentage for LCMS: {ps[st.index("lcms_cms_transform_fuzzer")]} %")

print(f"Percentage for NULL target remote: {r_over_cv(used_n) * 3.57} %")
print(f"Percentage for NULL target local: {r_over_cv(used_n) * 1.79} %")

################################

# Graph for coverage analysis

df = pd.read_csv("./df.csv")

def n_multi_sigma(n1, n2, alpha, beta, m1, m2, s1, s2):
    z_alpha = norm.ppf(1 - alpha)
    z_beta = norm.ppf(1- beta)
    z = z_alpha + z_beta

    c = n1/(n1 + n2)

    N = z**2 / (12 * c * (1 -c) * (norm.cdf(((m1 - m2)/sqrt(s1**2 + s2**2))) - 0.5)**2)

    return N

total = 0
green = 0
yellow = 0
red = 0
red_afl_group = 0
between_familiies = 0

for target1 in sorted(df['benchmark'].unique()):
    if "systemd" in target1:
        continue

    dft = df[df['benchmark'] == target1]
    count = 0
    count2 = 0

    total_t = 0
    green_t = 0
    yellow_t = 0
    red_t = 0

    red_afl = False
    between_familiies_t = False

    import matplotlib.pyplot as plt

    # Prepare data for heatmap
    fuzzers = ["afl", "aflfast", "aflplusplus", "aflsmart", "eclipser", "fairfuzz", "lafintel", "mopt", "libfuzzer", "entropic", "honggfuzz"] 
    afl = ["afl", "aflfast", "aflplusplus", "aflsmart", "eclipser", "fairfuzz", "lafintel", "mopt"]

    heatmap_data = np.zeros((len(fuzzers), len(fuzzers)))
    color_map = np.empty((len(fuzzers), len(fuzzers)), dtype=object)

    for i, fuzzer1 in enumerate(fuzzers):
        for j, fuzzer2 in enumerate(fuzzers):
            if fuzzer1 == fuzzer2:
                heatmap_data[i, j] = np.nan
                color_map[i, j] = 'white'
                continue

            df1 = dft[dft['fuzzer'] == fuzzer1]
            df2 = dft[dft['fuzzer'] == fuzzer2]
            m1 = df1['edges_covered'].mean()
            s1 = df1['edges_covered'].std()
            n1 = len(df1)
            m2 = df2['edges_covered'].mean()
            s2 = df2['edges_covered'].std()
            n2 = len(df2)

            try:
                N = round(n_multi_sigma(n1, n2, 0.05,0.05,m1,m2,s1,s2)/2)
            except:
                N = np.nan

            total += 1
            total_t += 1
            heatmap_data[i, j] = N
            if N <= 20:
                color_map[i, j] = 'green' 
                green += 1
                green_t += 1
            elif N <= n1 + n2:
                color_map[i, j] = 'yellow' 
                yellow += 1
                yellow_t += 1
                if fuzzer1 in afl and fuzzer2 in afl:
                    red_afl = True
                if (fuzzer1 not in afl and fuzzer2 in afl) or (fuzzer1 in afl and fuzzer2 not in afl):
                    between_familiies_t = True
            else:
                color_map[i, j] = 'red'
                red += 1
                red_t += 1
                if fuzzer1 in afl and fuzzer2 in afl:
                    red_afl = True
                if (fuzzer1 not in afl and fuzzer2 in afl) or (fuzzer1 in afl and fuzzer2 not in afl):
                    between_familiies_t = True

    fig, ax = plt.subplots(figsize=(8, 6))
    mask = np.isnan(heatmap_data)
    # Create a custom color map based on color_map

    # Flatten color_map and get unique colors in order
    flat_colors = color_map.flatten()
    unique_colors = [c for c in ['white', 'green', 'yellow', 'red'] if c in flat_colors]

    # Map color names to RGB
    color_dict = {
        'white': (1, 1, 1),
        'green': (0.56, 0.93, 0.56),
        'yellow': (1, 1, 0.6),
        'red': (1, 0.6, 0.6)
    }
    color_list = [color_dict[c] for c in unique_colors]
    cmap = ListedColormap(color_list)

    # Map color_map to integer indices for plotting
    color_indices = np.vectorize(lambda c: unique_colors.index(c))(color_map)
    color_indices = np.where(mask, np.nan, color_indices)

    
    mask = np.triu(heatmap_data)
    # Plot the heatmap using the respected color_map
    sns.heatmap(
        heatmap_data,
        mask=mask,
        annot=True,
        fmt='.0f',
        cmap=cmap,
        cbar=False,
        linewidths=0,  # Make grid thinner
        linecolor='black',  # Use a lighter color for the grid
        ax=ax,
        annot_kws={"size": 8, "weight": "bold", "color": "black"},
        square=True,
        vmin=np.nanmin(heatmap_data),
        vmax=np.nanmax(heatmap_data)
    )

    # Overlay the respected colors
    for (i, j), val in np.ndenumerate(heatmap_data):
        if not mask[i, j]:
            ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=True, color=color_dict[color_map[i, j]], linewidth=0))
    ax.set_xticks(np.arange(len(fuzzers[:-1])) + 0.5)
    ax.set_yticks(np.arange(1,len(fuzzers)) + 0.5)
    ax.set_xticklabels(fuzzers[:-1], rotation=45, ha='right', fontsize=12)
    ax.set_yticklabels(fuzzers[1:], rotation=0, fontsize=12)
    # ax.set_title(f"{target1}", fontsize=14, pad=-10)
    ax.set_xlim(0, len(fuzzers))
    ax.set_ylim(len(fuzzers), 0)
    ax.set_ylabel(f"{target1}", fontsize=14)

    # Add vertical and horizontal lines between mopt/libfuzzer and entropic/honggfuzz
    idx_mopt = fuzzers.index('mopt')
    idx_entropic = fuzzers.index('entropic')
    ax.axvline(x=idx_mopt + 1, ymin=0, ymax=0.9, color='black', linestyle='--', linewidth=1)
    ax.axvline(x=idx_entropic + 1, ymin=0, ymax=0.9, color='black', linestyle='--', linewidth=1)
    ax.axhline(y=idx_mopt + 1, xmin=0, xmax=0.9, color='black', linestyle='--', linewidth=1)
    ax.axhline(y=idx_entropic + 1, xmin=0, xmax=0.9, color='black', linestyle='--', linewidth=1)
    ax.axhline(y=1, xmin=0, xmax=0.9, color='black', linestyle='--', linewidth=1)


    plt.tight_layout()
    plt.savefig(f"robe/{target1}.pdf", format="pdf", bbox_inches="tight", dpi=300, facecolor=plt.gcf().get_facecolor())

    print(f"{target1}: Green: {green_t/total_t * 100} %, Yellow: {yellow_t/total_t * 100} %, Red: {red_t /total_t * 100} %")

    if red_afl:
        red_afl_group += 1
    if between_familiies_t:
        between_familiies += 1
print(f"Green: {green/total * 100} %, Yellow: {yellow/total * 100} %, Red: {red /total * 100} %, Fuzzers with at least a couple of fuzzer non distinguishable: {red_afl_group}, Fuzzers with at least a couple of interfamilies fuzzer non distinguishable: {between_familiies}")

