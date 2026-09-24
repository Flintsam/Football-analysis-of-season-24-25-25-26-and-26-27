import pandas as pd


# ============================================================
# CHUNK 1 — PLAYER IDENTITY
# Verify Player + Nation and investigate identity collisions.
# ============================================================

files = {
    "2024-25": "data/players_data-2024_2025.csv",
    "2025-26": "data/players_data-2025_2026.csv",
    "2026-27": "data/players_data-2026_2027.csv"
}

# Load the three season CSV files.
dfs = {}

for season, file in files.items():
    dfs[season] = pd.read_csv(file)


# Find columns shared by all three seasons.
common_columns = set(dfs["2024-25"].columns)

for season in ["2025-26", "2026-27"]:
    common_columns &= set(dfs[season].columns)

common_columns = list(common_columns)


# Create analysis DataFrames containing only common columns.
common_dfs = {}

for season, df in dfs.items():
    common_dfs[season] = df[common_columns].copy()


# Verify that Player and Nation are available in every season.
for season, df in common_dfs.items():
    print(
        season,
        "→",
        "Player" in df.columns,
        "Nation" in df.columns
    )


# Check whether Player + Nation is unique within each season.
for season, df in common_dfs.items():
    duplicates = df.duplicated(
        subset=["Player", "Nation"],
        keep=False
    )

    print(f"\n{season}")
    print("Player + Nation duplicates:", duplicates.sum())

    if duplicates.sum() > 0:
        print(
            df.loc[
                duplicates,
                ["Player", "Nation", "Squad"]
            ]
        )


# Investigate how many squads are associated with each Player + Nation collision.
for season, df in common_dfs.items():
    duplicates = df[
        df.duplicated(
            subset=["Player", "Nation"],
            keep=False
        )
    ]

    collision_groups = (
        duplicates
        .groupby(["Player", "Nation"])["Squad"]
        .nunique()
    )

    print(f"\n{season}")
    print(
        "Players involved in collisions:",
        len(collision_groups)
    )
    print(
        "Maximum squads for one Player + Nation:",
        collision_groups.max()
    )


# Check the distribution of the number of squads in each collision.
for season, df in common_dfs.items():
    duplicates = df[
        df.duplicated(
            subset=["Player", "Nation"],
            keep=False
        )
    ]

    collision_groups = (
        duplicates
        .groupby(["Player", "Nation"])["Squad"]
        .nunique()
    )

    print(f"\n{season}")
    print(collision_groups.value_counts())


# Inspect examples of Player + Nation collisions and their squad-level statistics.
for season, df in common_dfs.items():
    duplicates = df[
        df.duplicated(
            subset=["Player", "Nation"],
            keep=False
        )
    ]

    print(f"\n===== {season} =====")

    print(
        duplicates[
            [
                "Player",
                "Nation",
                "Squad",
                "Comp",
                "MP",
                "Starts",
                "Min"
            ]
        ].head(20)
    )


# Verify that Player + Nation + Squad uniquely identifies a season-level record.
for season, df in common_dfs.items():
    duplicates = df.duplicated(
        subset=["Player", "Nation", "Squad"],
        keep=False
    )

    print(f"\n{season}")
    print(
        "Player + Nation + Squad duplicates:",
        duplicates.sum()
    )

    if duplicates.sum() > 0:
        print(
            df.loc[
                duplicates,
                [
                    "Player",
                    "Nation",
                    "Squad",
                    "MP",
                    "Starts",
                    "Min"
                ]
            ]
        )


# ============================================================
# CHUNK 2 — SQUAD CHANGES ACROSS SEASONS
# Compare squad associations for the same Player + Nation between seasons.
# ============================================================

# Create one row per Player + Nation for the 2024-25 season.
season_24 = (
    common_dfs["2024-25"]
    .groupby(["Player", "Nation"])["Squad"]
    .agg(list)
    .reset_index()
)

# Create one row per Player + Nation for the 2025-26 season.
season_25 = (
    common_dfs["2025-26"]
    .groupby(["Player", "Nation"])["Squad"]
    .agg(list)
    .reset_index()
)

print(season_24.head(10))
print(season_25.head(10))


# Match players appearing in both seasons.
comparison = pd.merge(
    season_24,
    season_25,
    on=["Player", "Nation"],
    how="inner",
    suffixes=("_24", "_25")
)

print(comparison.head(10))


# Detect whether the player's recorded squad set changed between seasons.
comparison["squad_changed"] = (
    comparison["Squad_24"].apply(set)
    != comparison["Squad_25"].apply(set)
)

print(
    comparison["squad_changed"].value_counts()
)


# Inspect players whose recorded squad set changed.
changed_players = comparison[
    comparison["squad_changed"]
]

print(
    changed_players[
        [
            "Player",
            "Nation",
            "Squad_24",
            "Squad_25"
        ]
    ].head(30)
)


# Check whether a changed player still shares at least one squad between seasons.
comparison["shared_squad"] = comparison.apply(
    lambda row: bool(
        set(row["Squad_24"]) &
        set(row["Squad_25"])
    ),
    axis=1
)

print(
    comparison[
        comparison["squad_changed"]
    ]["shared_squad"].value_counts()
)


# Inspect changed players with no squad shared between the two seasons.
print(
    comparison[
        (comparison["squad_changed"]) &
        (~comparison["shared_squad"])
    ][
        [
            "Player",
            "Nation",
            "Squad_24",
            "Squad_25"
        ]
    ].head(20)
)


# ============================================================
# CHUNK 3 — MISSING-VALUE STRATEGY
# Inspect missing values and decide which should remain as NaN.
# ============================================================

# Use the 2024-25 dataset to inspect the missing-value patterns in detail.
df = common_dfs["2024-25"]

missing = df.isna().sum()

print(
    missing[
        missing > 0
    ].sort_values(
        ascending=False
    ).head(30)
)


# Inspect rows where On-Off is unavailable instead of treating it as zero.
print(
    df[
        df["On-Off"].isna()
    ][
        [
            "Player",
            "Nation",
            "Pos",
            "Squad",
            "MP",
            "Min",
            "On-Off"
        ]
    ]
)


# Calculate both missing counts and missing percentages.
missing_summary = pd.DataFrame({
    "missing_count": df.isna().sum(),
    "missing_percent": df.isna().mean() * 100
})

print(
    missing_summary[
        missing_summary["missing_count"] > 0
    ].sort_values(
        "missing_count",
        ascending=False
    )
)


# Inspect players with missing age or birth information.
print(
    df[
        df["Age"].isna()
    ][
        [
            "Player",
            "Nation",
            "Age",
            "Born"
        ]
    ]
)


# Inspect players with missing nation information.
print(
    df[
        df["Nation"].isna()
    ][
        [
            "Player",
            "Nation",
            "Pos",
            "Squad"
        ]
    ]
)


# Check missing-value patterns for every season.
for season, df in common_dfs.items():
    print(f"\n===== {season} =====")

    missing = df.isna().sum()

    print(
        missing[
            missing > 0
        ].sort_values(
            ascending=False
        )
    )


# Count how many columns contain at least one missing value in each season.
for season, df in common_dfs.items():
    missing = df.isna().sum()

    print(
        season,
        "→",
        (missing > 0).sum(),
        "columns with missing values"
    )


# No missing values were filled because the identified NaNs represent
# unavailable or not-applicable information rather than values we can safely infer.


# ============================================================
# CHUNK 4 — GK / OUTFIELD SPLIT
# Separate goalkeepers from outfield players for later analysis.
# ============================================================

# Inspect the position distribution before splitting goalkeepers.
for season, df in common_dfs.items():
    print(f"\n===== {season} =====")
    print(
        df["Pos"].value_counts(
            dropna=False
        )
    )


# Create separate goalkeeper and outfield DataFrames.
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


# Verify that the goalkeeper and outfield split preserves every row.
for season in common_dfs:
    print(f"\n===== {season} =====")

    print(
        "Original:",
        len(common_dfs[season])
    )

    print(
        "GK:",
        len(gk_dfs[season])
    )

    print(
        "Outfield:",
        len(outfield_dfs[season])
    )

    print(
        "Split total:",
        len(gk_dfs[season]) +
        len(outfield_dfs[season])
    )


# ============================================================
# CHUNK 5 — POSITION + NATION STANDARDIZATION
# Standardize position ordering and represent Nation using its three-letter code.
# ============================================================

# Define a consistent DF → MF → FW order for combined positions.
position_order = {
    "DF": 0,
    "MF": 1,
    "FW": 2
}


# Reorder combined position labels into the same standard order.
def standardize_position(pos):
    if "," not in pos:
        return pos

    positions = pos.split(",")

    positions.sort(
        key=lambda x: position_order[x]
    )

    return ",".join(positions)


# Apply the standardized position format to every season.
for season, df in common_dfs.items():
    common_dfs[season]["Pos"] = (
        common_dfs[season]["Pos"]
        .apply(standardize_position)
    )


# Verify the standardized position labels.
for season, df in common_dfs.items():
    print(f"\n===== {season} =====")

    print(
        df["Pos"]
        .value_counts()
        .sort_index()
    )


# Inspect the original Nation distribution, including missing values.
for season, df in common_dfs.items():
    print(f"\n===== {season} =====")

    print(
        df["Nation"]
        .value_counts(
            dropna=False
        )
        .head(30)
    )


# Verify that each Nation prefix maps consistently to one three-letter code.
for season, df in common_dfs.items():
    nation_mapping = (
        df.dropna(
            subset=["Nation"]
        )
        .assign(
            nation_prefix=df["Nation"]
            .str.split()
            .str[0],

            nation_code=df["Nation"]
            .str.split()
            .str[1]
        )
        .groupby("nation_prefix")["nation_code"]
        .nunique()
    )

    print(f"\n===== {season} =====")

    print(
        nation_mapping[
            nation_mapping > 1
        ]
    )


# Keep only the three-letter Nation code while preserving missing values.
for season, df in common_dfs.items():
    common_dfs[season]["Nation"] = (
        common_dfs[season]["Nation"]
        .str.split()
        .str[1]
    )


# Verify the standardized Nation values and remaining NaNs.
for season, df in common_dfs.items():
    print(f"\n===== {season} =====")

    print(
        df["Nation"]
        .value_counts(
            dropna=False
        )
    )


# ============================================================
# CHUNK 6 — DUPLICATE ROWS
# Check for exact duplicate records and confirm that none exist.
# ============================================================

# Check whether any entire rows are exact duplicates.
for season, df in common_dfs.items():
    duplicates = df.duplicated(
        keep=False
    )

    print(f"\n===== {season} =====")

    print(
        "Duplicate rows:",
        duplicates.sum()
    )


# ============================================================
# CHUNK 7 — SEASON-TO-SEASON SQUAD-CHANGE FLAGS
# Create flags for recorded squad changes across both season transitions.
# ============================================================

# Mark recorded squad changes from 2024-25 to 2025-26.
comparison[
    "transferred_this_season 24/25-25/26"
] = comparison[
    "squad_changed"
]

print(
    comparison[
        "transferred_this_season 24/25-25/26"
    ].value_counts()
)


# Create one row per Player + Nation for the 2025-26 season.
season_25 = (
    common_dfs["2025-26"]
    .groupby(["Player", "Nation"])["Squad"]
    .agg(list)
    .reset_index()
)


# Create one row per Player + Nation for the 2026-27 season.
season_26 = (
    common_dfs["2026-27"]
    .groupby(["Player", "Nation"])["Squad"]
    .agg(list)
    .reset_index()
)


# Match players appearing in both 2025-26 and 2026-27.
comparison_25_26 = pd.merge(
    season_25,
    season_26,
    on=["Player", "Nation"],
    how="inner",
    suffixes=("_25", "_26")
)


# Mark recorded squad changes from 2025-26 to 2026-27.
comparison_25_26[
    "transferred_this_season 25/26-26/27"
] = (
    comparison_25_26["Squad_25"].apply(set)
    != comparison_25_26["Squad_26"].apply(set)
)


print(
    comparison_25_26[
        "transferred_this_season 25/26-26/27"
    ].value_counts()
)


# ============================================================
# CHUNK 8 — MINIMUM-MINUTES THRESHOLD
# Draft a minimum playing-time rule for future per-90 comparisons.
# ============================================================

# Inspect the playing-time distribution for each season.
for season, df in common_dfs.items():
    print(f"\n===== {season} =====")

    print(
        df["Min"].describe()
    )


# Set the drafted minimum threshold for future per-90 comparisons.
# This is only a rule definition and does not filter the dataset.
MIN_MINUTES_THRESHOLD = 450

print(
    "\nDraft minimum-minutes threshold:",
    MIN_MINUTES_THRESHOLD,
    "minutes"
)