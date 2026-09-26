import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# LOAD DATA
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
# COMMON COLUMNS
# ============================================================

common_columns = set(dfs["2024-25"].columns)

for season in ["2025-26", "2026-27"]:
    common_columns &= set(dfs[season].columns)

common_columns = list(common_columns)

common_dfs = {}

for season, df in dfs.items():
    common_dfs[season] = df[common_columns].copy()


# ============================================================
# STANDARDIZE POSITION
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


# ============================================================
# STANDARDIZE NATION
# ============================================================

for season, df in common_dfs.items():
    common_dfs[season]["Nation"] = (
        common_dfs[season]["Nation"]
        .str.split()
        .str[1]
    )


# ============================================================
# CANONICAL SQUAD — HIGHEST MINUTES
# ============================================================

canonical_squads = {}

for season, df in common_dfs.items():

    squad_minutes = (
        df.groupby(
            ["Player", "Nation", "Squad"],
            as_index=False
        )["Min"]
        .sum()
    )

    canonical = (
        squad_minutes.loc[
            squad_minutes.groupby(
                ["Player", "Nation"]
            )["Min"].idxmax()
        ]
    )

    canonical_squads[season] = canonical


# ============================================================
# CANONICAL SQUAD LOOKUP
# ============================================================

canonical_lookup = {}

for season, df in canonical_squads.items():

    canonical_lookup[season] = (
        df.set_index(
            ["Player", "Nation"]
        )["Squad"]
        .to_dict()
    )


# ============================================================
# CHUNK 1 -- CREATING  DATA BASED ON DELTA OF MIN FROM 2 SEASON
# ============================================================

#copying data in diff list
season_24_25 = canonical_squads["2024-25"].copy()
season_25_26 = canonical_squads["2025-26"].copy()

print(season_24_25.shape)
print(season_25_26.shape)

#copying data only(player,nation and min)
previous = season_24_25[["Player", "Nation", "Min"]].copy()
next_season = season_25_26[["Player", "Nation", "Min"]].copy()

#renaming min in both season
previous = previous.rename(columns={"Min": "Min_24_25"})
next_season = next_season.rename(columns={"Min": "Min_25_26"})

#printing both data
print(previous.head())
print(next_season.head())

#using (player,nation as pk)
on=["Player", "Nation"]

#using only common value
how="inner"

#actual merge
longitudinal = previous.merge(
    next_season,
    on=["Player", "Nation"],
    how="inner"
)

#creating col for min25/26-min26/27
longitudinal["Minutes_Delta"] = (
    longitudinal["Min_25_26"]
    - longitudinal["Min_24_25"]
)

#printing merged data
print(longitudinal.shape)
print(longitudinal.head())

#checking for missing values
print("Missing deltas:", longitudinal["Minutes_Delta"].isna().sum())

#seperating players based on delta
increase = (longitudinal["Minutes_Delta"] > 0).sum()
decrease = (longitudinal["Minutes_Delta"] < 0).sum()
no_change = (longitudinal["Minutes_Delta"] == 0).sum()

print("Minutes increased:", increase)
print("Minutes decreased:", decrease)
print("No change:", no_change)
print("Total:", increase + decrease + no_change)

#calculation mean,median and sd
mean_delta = longitudinal["Minutes_Delta"].mean()
median_delta = longitudinal["Minutes_Delta"].median()
std_delta = longitudinal["Minutes_Delta"].std()

print("Mean:", mean_delta)
print("Median:", median_delta)
print("Standard deviation:", std_delta)

#calc IQR
q1 = longitudinal["Minutes_Delta"].quantile(0.25)
q3 = longitudinal["Minutes_Delta"].quantile(0.75)

iqr = q3 - q1

print("Q1:", q1)
print("Q3:", q3)
print("IQR:", iqr)

#calc min max
min_delta = longitudinal["Minutes_Delta"].min()
max_delta = longitudinal["Minutes_Delta"].max()

print("Minimum:", min_delta)
print("Maximum:", max_delta)


# ============================================================
# CHUNK 2 --VISUALIZATION
# ============================================================

#visualising using histogram

# plt.figure(figsize=(6, 6))

# sns.histplot(
#     longitudinal["Minutes_Delta"],
#     bins=40,
#     kde=True
# )

# plt.axvline(0, linestyle="--")

# plt.xlabel("Change in Minutes (2025-26 minus 2024-25)")
# plt.ylabel("Number of Players")
# plt.title("Distribution of Player Minutes Change")
# plt.show()


# ============================================================
# CHUNK 3 --AGE BASED EXPLORATION
# ============================================================

#adding age manually in common dfs
age_fixes = {
    "Olabade Aluko": 17,
    "Hannes Behrens": 17,
    "Pape Daouda Diongue": 18,
    "Jake Evans": 17,
    "Fer López": 20,
    "Mateus Mane": 16,
    "Max Moerstedt": 18,
    "Jeremy Monga": 15
}

for player, age in age_fixes.items():
    mask = common_dfs["2024-25"]["Player"] == player
    common_dfs["2024-25"].loc[mask, "Age"] = age

age_data = common_dfs["2024-25"][["Player", "Nation", "Age"]].copy()

print(age_data.shape)
print(age_data.head())
print("Missing Age:", age_data["Age"].isna().sum())

#creating a df for age using (player,nation) as pk
age_lookup = (
    common_dfs["2024-25"][["Player", "Nation", "Age"]]
    .drop_duplicates(subset=["Player", "Nation"])
)

print("Shape:", age_lookup.shape)
print("Duplicate Player + Nation:", age_lookup[["Player", "Nation"]].duplicated().sum())

#merging age into longitudnal
longitudinal = longitudinal.merge(
    age_lookup,
    on=["Player", "Nation"],
    how="left"#using left join
)

longitudinal = longitudinal.rename(columns={"Age": "Age_24_25"})

print("Shape:", longitudinal.shape)
print(longitudinal.head())

#creating agr group
def age_group(age):
    if age < 19:
        return "<19"
    elif age <= 20:
        return "19-20"
    elif age <= 22:
        return "21-22"
    elif age <= 24:
        return "23-24"
    elif age <= 26:
        return "25-26"
    elif age <= 28:
        return "27-28"
    elif age <= 30:
        return "29-30"
    elif age <= 32:
        return "31-32"
    elif age <= 34:
        return "33-34"
    else:
        return "35+"

longitudinal["Age_Group"] = longitudinal["Age_24_25"].apply(age_group)
print(longitudinal["Age_Group"].value_counts().sort_index())

#calc mean, median and count(delta) per age range

age_summary = (
    longitudinal
    .groupby("Age_Group")["Minutes_Delta"]
    .agg(
        Players="count",
        Mean="mean",
        Median="median"
    )
)

age_summary = age_summary.reindex([
    "<19",
    "19-20",
    "21-22",
    "23-24",
    "25-26",
    "27-28",
    "29-30",
    "31-32",
    "33-34",
    "35+"
])

print(age_summary)

# ============================================================
# CHUNK 4 -- VISUALIZATION
# ============================================================

plt.figure(figsize=(12, 6))

sns.boxplot(
    data=longitudinal,
    x="Age_Group",
    y="Minutes_Delta",
    order=[
        "<19",
        "19-20",
        "21-22",
        "23-24",
        "25-26",
        "27-28",
        "29-30",
        "31-32",
        "33-34",
        "35+"
    ]
)

plt.axhline(0, linestyle="--")

plt.xlabel("Age Group (2024-25)")
plt.ylabel("Change in Minutes")
plt.title("Minutes Change by Age Group")

plt.show()



