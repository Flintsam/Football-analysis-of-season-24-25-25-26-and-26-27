import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


# ============================================================
# LOAD DATA — DAY 1
# ============================================================

files = {
    "2024-25": "data/players_data-2024_2025.csv",
    "2025-26": "data/players_data-2025_2026.csv",
    "2026-27": "data/players_data-2026_2027.csv"
}

dfs = {}

for season, file in files.items():
    dfs[season] = pd.read_csv(file)


# ============================================================
# COMMON COLUMNS — DAY 1
# ============================================================

common_columns = set(dfs["2024-25"].columns)

for season in ["2025-26", "2026-27"]:
    common_columns &= set(dfs[season].columns)

common_columns = list(common_columns)

common_dfs = {}

for season, df in dfs.items():
    common_dfs[season] = df[common_columns].copy()


# ============================================================
# STANDARDIZATION — DAY 2
# ============================================================

position_order = {
    "DF": 0,
    "MF": 1,
    "FW": 2
}


def standardize_position(pos):
    if pd.isna(pos):
        return pos

    if "," not in pos:
        return pos

    positions = pos.split(",")

    positions.sort(
        key=lambda x: position_order[x]
    )

    return ",".join(positions)


for season, df in common_dfs.items():
    common_dfs[season]["Pos"] = (
        common_dfs[season]["Pos"]
        .apply(standardize_position)
    )


# Standardize Nation to three-letter code

for season, df in common_dfs.items():
    common_dfs[season]["Nation"] = (
        common_dfs[season]["Nation"]
        .str.split()
        .str[1]
    )


# ============================================================
# GK / OUTFIELD SPLIT — DAY 2
# ============================================================

gk_dfs = {}
outfield_dfs = {}

for season, df in common_dfs.items():

    gk_dfs[season] = (
        df[df["Pos"] == "GK"]
        .copy()
    )

    outfield_dfs[season] = (
        df[df["Pos"] != "GK"]
        .copy()
    )


# ============================================================
# MINIMUM-MINUTES FILTER — DAY 3
# ============================================================

MIN_MINUTES_THRESHOLD = 450

filtered_dfs = {}

for season, df in common_dfs.items():

    filtered_dfs[season] = (
        df[df["Min"] >= MIN_MINUTES_THRESHOLD]
        .copy()
    )


# ============================================================
# PER-90 METRICS — DAY 3
# ============================================================

for season, df in filtered_dfs.items():

    df["Gls_per90"] = df["Gls"] / df["90s"]

    df["Ast_per90"] = df["Ast"] / df["90s"]

    df["GA_per90"] = df["G+A"] / df["90s"]


# ============================================================
# OUTFIELD HYPOTHESIS DATA — DAY 3
# ============================================================

hypothesis_dfs = {}

for season, df in filtered_dfs.items():

    hypothesis_dfs[season] = (
        df[df["Pos"].isin(["DF", "MF", "FW"])]
        .copy()
    )




# ============================================================
# CHUNK 1 — SAMPLE SIZE AND SKEWNESS CHECK AND LEVENE'S TEST
# ============================================================

metrics = {
    "H1 — Gls_per90": "Gls_per90",
    "H2 — GA_per90": "GA_per90",
    "H3 — +/-": "+/-"
}

for season, df in hypothesis_dfs.items():

    print(f"\n===== {season} =====")

    for hypothesis, metric in metrics.items():

        #calculating numerical value of skew
        print(f"\n{hypothesis}")

        for position in ["DF", "MF", "FW"]:

            group = df[df["Pos"] == position][metric].dropna()#used for dropping missing value

            print(
                f"{position}: "
                f"n={len(group)}, "
                f"skew={group.skew():.3f}"#skew tells us if its distributed equally if skew=0 its symmetric
            )

        #making skew diagram to check visually
        # groups = [
        #     df[df["Pos"] == position][metric].dropna()
        #     for position in ["DF", "MF", "FW"]
        # ]

        # plt.figure(figsize=(8, 5))

        # plt.boxplot(
        #     groups,
        #     tick_labels=["DF", "MF", "FW"]
        # )

        # plt.title(f"{hypothesis} — {season}")
        # plt.xlabel("Position")
        # plt.ylabel(metric)

        # plt.show()

        #Levene's test
        groups = [
            df[df["Pos"] == position][metric].dropna()
            for position in ["DF", "MF", "FW"]
        ]

        statistic, p_value = stats.levene(
            *groups,
            center="median"
        )

        print(
            f"{hypothesis}: "
            f"statistic={statistic:.4f}, "
            f"p={p_value:.4g}"
            #if p>0.05 variance is less use anova
            #if p<0.05 variance big use kruskal
        )


# ============================================================
# CHUNK --2 FORMAL STASTICAL TESTS
# ============================================================


#Running H1 and H2 for kruskal-wallis

metrics = {
    "H1 — Gls_per90": "Gls_per90",
    "H2 — GA_per90": "GA_per90"
}

for season, df in hypothesis_dfs.items():

    print(f"\n===== {season} =====")

    for hypothesis, metric in metrics.items():

        groups = [
            df[df["Pos"] == position][metric].dropna()
            for position in ["DF", "MF", "FW"]
        ]

        statistic, p_value = stats.kruskal(*groups)

        print(
            f"{hypothesis}: "
            f"H={statistic:.4f}, "
#if small H group ranks are similar and large H means group ranks are more seperated
            f"p={p_value:.4g}"
        )
print()


#running ANOVA for H3

for season in ["2024-25", "2025-26"]:

    df = hypothesis_dfs[season]

    groups = [
        df[df["Pos"] == position]["+/-"].dropna()
        for position in ["DF", "MF", "FW"]
    ]

    statistic, p_value = stats.f_oneway(*groups)

    print(
        f"{season}: "
        f"F={statistic:.4f}, "
#variation between groups / variation within groups
#small f = relatively similar   big f = realtively seperated
        f"p={p_value:.4g}"
    )


# ============================================================
# CHUNK --3 EFFECT SIZES
# ============================================================

#actually calculating how big the variance is for H1 and H2
metrics = {
    "H1 — Gls_per90": "Gls_per90",
    "H2 — GA_per90": "GA_per90"
}

for season, df in hypothesis_dfs.items():

    print(f"\n===== {season} =====")

    for hypothesis, metric in metrics.items():

        groups = [
            df[df["Pos"] == position][metric].dropna()
            for position in ["DF", "MF", "FW"]
        ]

        H, p_value = stats.kruskal(*groups)#calculating H

        N = sum(len(group) for group in groups)#counting obv
        k = len(groups)#counting number of groups

        epsilon_squared = (H - k + 1) / (N - k)
        #actual measure of effect size measure

        print(
            f"{hypothesis}: "
            f"epsilon²={epsilon_squared:.4f}"
        )


print()
#actually calculating how big the variance is for H3
for season in ["2024-25", "2025-26"]:

    df = hypothesis_dfs[season]

    groups = [
        df[df["Pos"] == position]["+/-"].dropna()
        for position in ["DF", "MF", "FW"]
    ]

    grand_mean = pd.concat(groups).mean()#calculating mean for all groups

    ss_between = sum(#measure the variation caused by group means
        len(group) * (group.mean() - grand_mean) ** 2
        for group in groups
    )

    ss_total = sum(#measures the total variation in all the observations around the grand mean.
        ((group - grand_mean) ** 2).sum()
        for group in groups
    )

    eta_squared = ss_between / ss_total#actual measurement of size diff

    print(
        f"{season}: "
        f"eta²={eta_squared:.4f}"
    )

# ============================================================
# CHUNK --4 MANUAL SANITY CHECK
# ============================================================

#claculating h3 for 24/25
df = hypothesis_dfs["2024-25"]

groups = [
    df[df["Pos"] == position]["+/-"].dropna()
    for position in ["DF", "MF", "FW"]
]

N = sum(len(group) for group in groups)
k = len(groups)

grand_mean = pd.concat(groups).mean()

ss_between = sum(
    len(group) * (group.mean() - grand_mean) ** 2
    for group in groups
)

ss_within = sum(
    ((group - group.mean()) ** 2).sum()
    for group in groups
)

ms_between = ss_between / (k - 1)
ms_within = ss_within / (N - k)

F_manual = ms_between / ms_within

print("N =", N)
print("k =", k)
print("Grand mean =", grand_mean)
print("SS between =", ss_between)
print("SS within =", ss_within)
print("MS between =", ms_between)
print("MS within =", ms_within)
print("Manual F =", F_manual)



# ============================================================
# CHUNK --5 SUMMARY
# ============================================================

metrics = {
    "H1 — Gls_per90": "Gls_per90",
    "H2 — GA_per90": "GA_per90",
    "H3 — +/-": "+/-"
}

for season, df in hypothesis_dfs.items():

    print(f"\n===== {season} =====")

    for hypothesis, metric in metrics.items():

        print(f"\n{hypothesis}")

        for position in ["DF", "MF", "FW"]:

            group = df[df["Pos"] == position][metric].dropna()

            print(
                f"{position}: "
                f"n={len(group)}, "
                f"mean={group.mean():.4f}, "
                f"median={group.median():.4f}, "
                f"std={group.std():.4f}, "
                f"IQR={group.quantile(0.75) - group.quantile(0.25):.4f}"
            )
