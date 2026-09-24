import pandas as pd


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