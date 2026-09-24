import pandas as pd

files = {
    "2024-25": "data/players_data-2024_2025.csv",
    "2025-26": "data/players_data-2025_2026.csv",
    "2026-27": "data/players_data-2026_2027.csv"
}

dfs = {}

for season, file in files.items():
    dfs[season] = pd.read_csv(file)

for season, df in dfs.items():
    print(season, df.shape)

for season, df in dfs.items():
    print("\n" + "=" * 50)
    print(season)
    print("=" * 50)
    df.info()
    print("\n" + "=" * 50)
    print(season)
    print("=" * 50)
    print(df.dtypes)

for season, df in dfs.items():
    print("\n" + "=" * 50)
    print(season)
    print("=" * 50)
    print(df.describe())

for season, df in dfs.items():
    print("\n" + "=" * 50)
    print(season)
    print("=" * 50)
    print(df.head())

for season, df in dfs.items():
    print(season)
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])
    print()

for season, df in dfs.items():
    print("\n" + "=" * 50)
    print(season)
    print("=" * 50)

print("Total columns:", len(dfs["2024-25"].columns))
for column in dfs["2024-25"].columns:
    print(column)




# for season, df in dfs.items():
#     print("\n" + "=" * 50)
#     print(season)
#     print("=" * 50)

#     missing_count = df.isna().sum()
#     missing_percent = (missing_count / len(df)) * 100

#     missing = pd.DataFrame({
#         "Missing Count": missing_count,
#         "Missing %": missing_percent
#     })

#     print(missing[missing["Missing Count"] > 0].to_string())

# columns_24 = set(dfs["2024-25"].columns)
# columns_25 = set(dfs["2025-26"].columns)
# columns_26 = set(dfs["2026-27"].columns)

# common_columns = columns_24 & columns_25 & columns_26

# print("2024-25 columns:", len(columns_24))
# print("2025-26 columns:", len(columns_25))
# print("2026-27 columns:", len(columns_26))

# print("\nCommon columns:", len(common_columns))
# print("Extra in 2024-25:", len(columns_24 - common_columns))

# print("\nExtra 2024-25 columns:")
# print(sorted(columns_24 - common_columns))



common_columns = sorted(
    set(dfs["2024-25"].columns)
    & set(dfs["2025-26"].columns)
    & set(dfs["2026-27"].columns)
)

common_dfs = {}

for season, df in dfs.items():
    common_dfs[season] = df[common_columns].copy()

for season, df in common_dfs.items():
    print(season, "→", df.shape)


for season, df in common_dfs.items():
    print(season)
    print("Number of columns:", len(df.columns))
    print("Columns identical to 2024-25:",
          df.columns.equals(common_dfs["2024-25"].columns))
    print()
    





#print(dfs)