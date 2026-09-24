import pandas as pd
import scikit_posthocs as sp
from statsmodels.stats.multicomp import pairwise_tukeyhsd


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
# FINAL OUTFIELD ANALYSIS DATA — DAY 3/4
# ============================================================

hypothesis_dfs = {}

for season, df in filtered_dfs.items():

    hypothesis_dfs[season] = (
        df[df["Pos"].isin(["DF", "MF", "FW"])]
        .copy()
    )


# ============================================================
# CHUNK --1 CREATING DUNN AND HOLM FUNCTION FOR H1 and H2
# ============================================================


def run_dunn_test(df, value_column):

    result = sp.posthoc_dunn(
        df,
        val_col=value_column,
        group_col="Pos",
        p_adjust="holm"
    )

    return result

#Running DUNN for H1

#season 24/25
h1_2024_25 = run_dunn_test(
    hypothesis_dfs["2024-25"],
    "Gls_per90"
)

#print("\n===== H1 — 2024-25 =====")
#print(h1_2024_25)

#season 25/26
h1_2025_26 = run_dunn_test(
    hypothesis_dfs["2025-26"],
    "Gls_per90"
)

#print("\n===== H1 — 2025-26 =====")
#print(h1_2025_26)

#season 26/27
h1_2026_27 = run_dunn_test(
    hypothesis_dfs["2026-27"],
    "Gls_per90"
)

#print("\n===== H1 — 2026-27 =====")
#print(h1_2026_27)

#Running DUNN for H2

#season 24/25
h2_2024_25 = run_dunn_test(
    hypothesis_dfs["2024-25"],
    "GA_per90"
)

#print("\n===== H2 — 2024-25 =====")
#print(h2_2024_25)

#season 25/26
h2_2025_26 = run_dunn_test(
    hypothesis_dfs["2025-26"],
    "GA_per90"
)

#print("\n===== H2 — 2025-26 =====")
#print(h2_2025_26)

# ============================================================
# CHUNK --2 CREATING TUKEY HSD FOR H3
# ============================================================

h3_2024_25 = pairwise_tukeyhsd(
    endog=hypothesis_dfs["2024-25"]["+/-"],
    groups=hypothesis_dfs["2024-25"]["Pos"],
    alpha=0.05
)

#print("\n===== H3 — 2024-25 =====")
#print(h3_2024_25)


# ============================================================
# CHUNK --3 CREATING A PROPER TABLE FOR ALL DUNN TEST
# ============================================================

posthoc_results = [

    # H1 — 2024-25
    ["H1", "2024-25", "DF vs FW", h1_2024_25.loc["DF", "FW"]],
    ["H1", "2024-25", "DF vs MF", h1_2024_25.loc["DF", "MF"]],
    ["H1", "2024-25", "FW vs MF", h1_2024_25.loc["FW", "MF"]],

    # H1 — 2025-26
    ["H1", "2025-26", "DF vs FW", h1_2025_26.loc["DF", "FW"]],
    ["H1", "2025-26", "DF vs MF", h1_2025_26.loc["DF", "MF"]],
    ["H1", "2025-26", "FW vs MF", h1_2025_26.loc["FW", "MF"]],

    # H1 — 2026-27
    ["H1", "2026-27", "DF vs FW", h1_2026_27.loc["DF", "FW"]],
    ["H1", "2026-27", "DF vs MF", h1_2026_27.loc["DF", "MF"]],
    ["H1", "2026-27", "FW vs MF", h1_2026_27.loc["FW", "MF"]],

    # H2 — 2024-25
    ["H2", "2024-25", "DF vs FW", h2_2024_25.loc["DF", "FW"]],
    ["H2", "2024-25", "DF vs MF", h2_2024_25.loc["DF", "MF"]],
    ["H2", "2024-25", "FW vs MF", h2_2024_25.loc["FW", "MF"]],

    # H2 — 2025-26
    ["H2", "2025-26", "DF vs FW", h2_2025_26.loc["DF", "FW"]],
    ["H2", "2025-26", "DF vs MF", h2_2025_26.loc["DF", "MF"]],
    ["H2", "2025-26", "FW vs MF", h2_2025_26.loc["FW", "MF"]],
]

posthoc_df = pd.DataFrame(
    posthoc_results,
    columns=["Hypothesis", "Season", "Comparison", "Adjusted_p"]
)

posthoc_df["Significant"] = posthoc_df["Adjusted_p"] < 0.05

print("\n===== POST-HOC RESULTS SUMMARY =====")
print(posthoc_df)

#saving post hoc data
posthoc_df.to_csv(
    "posthoc_results.csv",
    index=False
)


# ============================================================
# CHUNK --4 CREATING A PROPER TABLE FOR ALL TUKEY TEST
# ============================================================


tukey_df = pd.DataFrame(
    data=h3_2024_25._results_table.data[1:],
    columns=h3_2024_25._results_table.data[0]
)

print("\n===== TUKEY RESULTS SUMMARY =====")
print(tukey_df)
