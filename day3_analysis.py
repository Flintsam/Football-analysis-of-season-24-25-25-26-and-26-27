import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# LOAD DAY 2 CLEANED DATA
# ============================================================

files = {
    "2024-25": "data/players_data-2024_2025.csv",
    "2025-26": "data/players_data-2025_2026.csv",
    "2026-27": "data/players_data-2026_2027.csv"
}

dfs = {}

for season, file in files.items():
    dfs[season] = pd.read_csv(file)


# Keep only columns shared by all three seasons
common_columns = set(dfs["2024-25"].columns)

for season in ["2025-26", "2026-27"]:
    common_columns &= set(dfs[season].columns)

common_columns = list(common_columns)

common_dfs = {}

for season, df in dfs.items():
    common_dfs[season] = df[common_columns].copy()


# ============================================================
# DAY 2 STANDARDIZATION
# ============================================================

# Standardize position labels
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
    positions.sort(key=lambda x: position_order[x])

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
# GK / OUTFIELD SPLIT
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
# DAY 3 CONSTANT
# ============================================================

MIN_MINUTES_THRESHOLD = 450


# ============================================================
# VERIFY DAY 3 INPUT DATA
# ============================================================

for season in common_dfs:
    print(
        season,
        "→",
        common_dfs[season].shape
    )


# ============================================================
# CHUNK 1 — CANONICAL SQUAD
# ============================================================

# Shows players who have played for more than one club per season
for season, df in common_dfs.items():

    squad_counts = (
        df.groupby(["Player", "Nation"])["Squad"]
        .nunique()
        .reset_index(name="Squad_Count")
    )

    multiple_squad_players = (
        squad_counts[squad_counts["Squad_Count"] > 1]
    )

    # print(f"\n===== {season} =====")
    # print(multiple_squad_players)


# Create a dictionary to store canonical squad for each player
canonical_squads = {}

# Group by player, nation and squad to show time played
for season, df in common_dfs.items():

    squad_minutes = (
        df.groupby(
            ["Player", "Nation", "Squad"],
            as_index=False
        )["Min"]
        .sum()
    )

    # Compares minutes and assigns the squad where the player played more
    canonical = (
        squad_minutes.loc[
            squad_minutes.groupby(
                ["Player", "Nation"]
            )["Min"].idxmax()
        ]
    )

    # Stores the result
    canonical_squads[season] = canonical


# Create a lookup dictionary for canonical squads
canonical_lookup = {}

for season, df in canonical_squads.items():

    canonical_lookup[season] = (
        df.set_index(
            ["Player", "Nation"]
        )["Squad"]
        .to_dict()
    )


# Compare 2024-25 to 2025-26
comparison_24_25 = pd.DataFrame(
    [
        {
            "Player": player,
            "Nation": nation,
            "Squad_24_25": canonical_lookup["2024-25"][
                (player, nation)
            ],
            "Squad_25_26": canonical_lookup["2025-26"][
                (player, nation)
            ]
        }
        for player, nation in (
            set(canonical_lookup["2024-25"])
            & set(canonical_lookup["2025-26"])
        )
    ]
)

comparison_24_25["squad_changed"] = (
    comparison_24_25["Squad_24_25"]
    != comparison_24_25["Squad_25_26"]
)


# Compare 2025-26 to 2026-27
comparison_25_26 = pd.DataFrame(
    [
        {
            "Player": player,
            "Nation": nation,
            "Squad_25_26": canonical_lookup["2025-26"][
                (player, nation)
            ],
            "Squad_26_27": canonical_lookup["2026-27"][
                (player, nation)
            ]
        }
        for player, nation in (
            set(canonical_lookup["2025-26"])
            & set(canonical_lookup["2026-27"])
        )
    ]
)

comparison_25_26["squad_changed"] = (
    comparison_25_26["Squad_25_26"]
    != comparison_25_26["Squad_26_27"]
)


print("\n===== 2024-25 → 2025-26 =====")
print(
    comparison_24_25["squad_changed"]
    .value_counts()
)

print("\n===== 2025-26 → 2026-27 =====")
print(
    comparison_25_26["squad_changed"]
    .value_counts()
)


# ============================================================
# CHUNK 2 — MISSING VALUES
# ============================================================

# Comparing data while filled with data and NaN using mean median
original_2024 = pd.read_csv(files["2024-25"])
age_original = original_2024["Age"].copy()

print("\n===== Missing Value Experiment =====")

print(
    "Original missing values:",
    age_original.isna().sum()
)

print(
    "Original mean:",
    age_original.mean()
)

print(
    "Original median:",
    age_original.median()
)


age_mean = age_original.fillna(
    age_original.mean()
)

age_median = age_original.fillna(
    age_original.median()
)


print("\nAfter mean imputation")

print(
    "Missing values:",
    age_mean.isna().sum()
)

print(
    "Mean:",
    age_mean.mean()
)

print(
    "Median:",
    age_mean.median()
)


print("\nAfter median imputation")

print(
    "Missing values:",
    age_median.isna().sum()
)

print(
    "Mean:",
    age_median.mean()
)

print(
    "Median:",
    age_median.median()
)


print("\nMean shift")

print(
    "Mean imputation:",
    age_mean.mean() - age_original.mean()
)

print(
    "Median imputation:",
    age_median.mean() - age_original.mean()
)


print("\nMedian shift")

print(
    "Mean imputation:",
    age_mean.median() - age_original.median()
)

print(
    "Median imputation:",
    age_median.median() - age_original.median()
)


# Manually adding where age is missing using external dataset
age_updates = {
    "Olabade Aluko": 17,
    "Hannes Behrens": 17,
    "Pape Daouda Diongue": 18,
    "Jake Evans": 17,
    "Fer López": 20,
    "Mateus Mane": 16,
    "Max Moerstedt": 18,
    "Jeremy Monga": 15
}

for player, age in age_updates.items():

    common_dfs["2024-25"].loc[
        common_dfs["2024-25"]["Player"] == player,
        "Age"
    ] = age


# Printing players where Age is missing
missing_age = common_dfs["2024-25"][
    common_dfs["2024-25"]["Age"].isna()
]

# print(missing_age[["Player", "Nation", "Squad", "Age"]])


# Updating Nation values manually
nation_updates = {
    "Olabade Aluko": "ENG",
    "Jake Evans": "ENG",
    "Atakan Karazor": "GER",
    "Fer López": "ESP",
    "Mateus Mane": "POR",
    "Jeremy Monga": "ENG",
    "Plamedi Nsingi": "FRA"
}

for player, nation in nation_updates.items():

    common_dfs["2024-25"].loc[
        common_dfs["2024-25"]["Player"] == player,
        "Nation"
    ] = nation


# Missing values in Nation
missing_nation = common_dfs["2024-25"][
    common_dfs["2024-25"]["Nation"].isna()
]

# print(missing_nation[["Player", "Squad", "Nation"]])


# ============================================================
# CHUNK 3 — 450 MINUTE THRESHOLD & PER 90
# ============================================================

# Creating a dictionary where player >450 min
filtered_dfs = {}

for season, df in common_dfs.items():

    filtered_dfs[season] = (
        df[df["Min"] >= MIN_MINUTES_THRESHOLD]
        .copy()
    )

    print(
        season,
        "Before:",
        len(df),
        "After:",
        len(filtered_dfs[season])
    )


# Checking if filter actually worked
for season, df in filtered_dfs.items():

    print(
        season,
        "Minimum minutes:",
        df["Min"].min()
    )


# Creating columns based on per 90 min
for season, df in filtered_dfs.items():

    df["Gls_per90"] = (
        df["Gls"] / df["90s"]
    )

    df["Ast_per90"] = (
        df["Ast"] / df["90s"]
    )

    df["GA_per90"] = (
        df["G+A"] / df["90s"]
    )


# Printing per 90 min values
# for season, df in filtered_dfs.items():
#     print(f"\n===== {season} =====")
#     print(
#         df[
#             ["Player", "Min", "Gls", "Ast", "G+A",
#              "Gls_per90", "Ast_per90", "GA_per90"]
#         ]
#         .sort_values("GA_per90", ascending=False)
#         .head(10)
#     )


# ============================================================
# CHUNK 4 — HYPOTHESES & DESCRIPTIVE STATISTICS
# ============================================================

# Creating a dict of only MF, DF, FW
hypothesis_dfs = {}

for season, df in filtered_dfs.items():

    hypothesis_dfs[season] = (
        df[df["Pos"].isin(["DF", "MF", "FW"])]
        .copy()
    )


# Calculating mean, median, standard deviation and IQR
for season, df in hypothesis_dfs.items():

    print(f"\n===== {season} =====")

    for position in ["DF", "MF", "FW"]:

        position_data = df[
            df["Pos"] == position
        ]

        print(
            f"\n{position} (n={len(position_data)})"
        )

        for metric in [
            "Gls_per90",
            "Ast_per90",
            "GA_per90"
        ]:

            q1 = position_data[metric].quantile(0.25)
            q3 = position_data[metric].quantile(0.75)
            iqr = q3 - q1

            print(
                f"{metric}: "
                f"Mean={position_data[metric].mean():.3f}, "
                f"Median={position_data[metric].median():.3f}, "
                f"SD={position_data[metric].std():.3f}, "
                f"IQR={iqr:.3f}"
            )


# ============================================================
# CHUNK 5 — DISTRIBUTION VISUALIZATIONS
# ============================================================

# metrics = {
#     "Gls_per90": "Goals per 90",
#     "Ast_per90": "Assists per 90",
#     "GA_per90": "Goals + Assists per 90"
# }

# position_order = ["DF", "MF", "FW"]


# for season, df in hypothesis_dfs.items():

#     for metric, title in metrics.items():

#         plt.figure(figsize=(10, 6))

#         sns.boxplot(
#             data=df,
#             x="Pos",
#             y=metric,
#             order=position_order
#         )

#         group_counts = (
#             df["Pos"]
#             .value_counts()
#             .reindex(position_order)
#         )

#         labels = [
#             f"{position}\n(n={group_counts[position]})"
#             for position in position_order
#         ]

#         plt.xticks(
#             range(len(position_order)),
#             labels
#         )

#         plt.title(
#             f"{title} Distribution — {season}"
#         )

#         plt.xlabel("Position")
#         plt.ylabel(title)

#         plt.grid(
#             axis="y",
#             alpha=0.3
#         )

#         plt.tight_layout()
#         plt.show()

# H3 — Compare average plus/minus by position

for season, df in filtered_dfs.items():
    hypothesis_df = df[
        df["Pos"].isin(["DF", "MF", "FW"])
    ].copy()

    print(f"\n===== {season} =====")

    print(
        hypothesis_df
        .groupby("Pos")["+/-"]
        .agg(["count", "mean", "median", "std"])
        .round(3)
    )