# Football Player & Team Performance Data Analysis

Statistical analysis of player and team performance across the Big 5 European football leagues, built as the Week 2 (Data Analytics) project in a structured 6-week hands-on CS career exploration. This week was scoped deliberately to exclude machine learning entirely — the goal was to genuinely experience data investigation (cleaning, querying, hypothesis testing, interpretation) as its own discipline.

## Dataset

**Source:** "Football Players Stats" by hubertsidorowicz on Kaggle, originally sourced from [FBref](https://fbref.com). Kaggle is the file host here, not the data's origin — the underlying numbers are real match statistics from FBref, not Kaggle-generated data.

**Seasons covered:**
- 2024-25 (complete)
- 2025-26 (complete)
- 2026-27 (in-progress/incomplete as of analysis date — handled via a minimum-minutes threshold in hypothesis testing rather than exclusion, and excluded entirely from the longitudinal minutes-change analysis to avoid comparing a completed season against a partial one)

## Tools

Python, pandas, SQLite (`sqlite3`), matplotlib, seaborn, `scipy.stats`, Jupyter Notebook, Git.

## Data Cleaning & Identity Resolution

Football transfer data has a structural problem: there's no stable `player_id` in the raw data, and players can appear multiple times per season due to mid-season transfers or loans. This project resolved that with a two-level identity system:

- **Cross-season identity:** `Player + Nation` — used to track the same player across different seasons
- **Season-level record:** `Player + Nation + Squad` — since a player can have multiple squad rows within one season
- **Canonical squad:** for any player who played for multiple squads in a season, the squad where they accumulated the most minutes was chosen as their representative squad for that season (this does not mean they only played there — it's a representative label, not a full transfer history)

Other cleaning steps: goalkeepers were split into a separate `gk_dfs` frame from outfield players (`outfield_dfs`), since GK stats aren't meaningfully comparable to outfield stats; position labels and nationality codes were standardized across seasons; raw source CSVs were kept untouched throughout, with all cleaning applied to derived copies.

## Methodology

**Minimum-minutes threshold:** A `450-minute` threshold was applied for the hypothesis-testing analysis (H1–H3) to exclude players with too little playing time to produce meaningful rate stats. This threshold was **deliberately not applied** to the longitudinal minutes-change analysis, since filtering that population would change the question being studied.

**Rate metrics:** `Gls_per90`, `Ast_per90`, `GA_per90` (goals+assists per 90 minutes) were derived to normalize for playing time.

**Hypotheses tested:**
- **H1:** Forwards have a higher `Gls_per90` than other positions
- **H2:** Forwards have a higher `GA_per90` than other positions
- **H3:** Team `+/-` differs by position (DF/MF/FW)

**Statistical approach:** Skewness and Levene's test for variance homogeneity were checked per hypothesis first, which determined the correct test to use:
- H1/H2 → **Kruskal-Wallis** (non-parametric, due to skew/variance violations), with **effect size (epsilon-squared)**
- H3 → **one-way ANOVA** (2024-25 and 2025-26 only — 2026-27 excluded due to too small a sample size), with **eta-squared** effect size

Where Kruskal-Wallis or ANOVA results were significant, post-hoc tests were run to identify *which* groups differed:
- **Dunn's test with Holm correction** (following significant Kruskal-Wallis results)
- **Tukey HSD** (following the significant H3 ANOVA)

One ANOVA result (2024-25, H3) was manually reconstructed by hand as a verification step against the `scipy` output.

## Key Findings

- **H3 result:** Forwards had the highest team `+/-` across all three seasons — this **contradicted the original hypothesis**, which expected midfielders to lead. This is one of the more notable non-obvious findings of the analysis: the initial intuition about which position drives team plus/minus was wrong.
- H1 and H2 were evaluated with the Kruskal-Wallis + Dunn's test (Holm-corrected) pipeline described above; full statistical output (test statistics, p-values, effect sizes, and pairwise comparisons) is documented in the analysis notebook.
- A labeling bug was caught and corrected during the project: values initially presented as "descriptive means" for one comparison had actually been IQR values pulled from the wrong column — corrected before finalizing results.

### Longitudinal Minutes-Change Analysis (2024-25 → 2025-26)

Built on the same `Player + Nation` identity and canonical-squad logic, restricted to the one fully-completed season transition (2026-27 excluded as incomplete/in-progress). Population: 1,752 players present in both seasons (inner merge).

**Metric:** `Minutes_Delta = Min_25_26 - Min_24_25`

| Statistic | Value |
|---|---|
| Mean | -37.68 |
| Median | -17.5 |
| Std. Dev. | 934.59 |
| Q1 / Q3 | -589.75 / 493.0 |
| IQR | 1082.75 |
| Min / Max | -2924 / 3137 |

The distribution is centered near zero but widely spread, roughly bell-shaped but not perfectly symmetric, with a slight negative shift.

**Age-based exploration** (descriptive only — no significance testing or causal claims), using each player's 2024-25 age as their starting age:

| Age Group | Players | Mean Δ | Median Δ |
|---|---|---|---|
| <19 | 86 | +409.6 | +213.0 |
| 19-20 | 171 | +115.6 | +53.0 |
| 21-22 | 271 | -4.3 | +38.0 |
| 23-24 | 315 | -39.3 | 0.0 |
| 25-26 | 287 | -90.4 | -67.0 |
| 27-28 | 238 | -75.4 | -60.0 |
| 29-30 | 170 | -115.6 | -119.5 |
| 31-32 | 126 | -142.5 | -131.5 |
| 33-34 | 58 | -356.6 | -199.5 |
| 35+ | 30 | -175.1 | -272.0 |

The general pattern: younger players tend to gain minutes season-over-season, older players tend to lose them — consistent with typical career-arc expectations, though this was kept strictly descriptive and no formal test was run to confirm statistical significance of the trend.

## Project Structure

Local path: `Football-analysis/` (SQLite-backed, Jupyter-notebook-driven analysis)
Repository: `Flintsam/Football-analysis-of-season-24-25-25-26-and-26-27` (GitHub, SSH)
`.gitignore` excludes the raw `data/` folder — raw CSVs are not committed, only analysis code and derived outputs.

## Limitations & Data Integrity Notes

- The 2026-27 season is incomplete as of this analysis and is handled carefully throughout: included with a minutes threshold in cross-sectional hypothesis testing, but fully excluded from the longitudinal analysis and from the H3 ANOVA.
- No virtual environment was set up for this project (noted as a deliberate scope simplification, not an oversight).
- The age-based exploration is explicitly descriptive-only; no significance testing or causal interpretation was applied to it.
- An earlier era (2009–2015) was considered and excluded from the core dataset, since publicly available player-level data for that period is FIFA video-game attribute ratings rather than real match performance data — mixing the two would corrupt the statistical analysis. A separate, clearly-labeled side-analysis using FIFA attribute ratings (for a specific historical Barcelona-era question) may be added later, framed explicitly as "how this era was rated," not "how it performed."

## What This Project Was For

This is Week 2 of a 6-week hands-on exploration to decide a CS specialization through real project work. The goal wasn't mastering data science — it was experiencing the actual process of data investigation: resolving messy real-world identity problems, choosing the statistically correct test for the data's actual distribution (not just defaulting to ANOVA), running proper post-hoc corrections, and catching a real labeling bug before it became a wrong conclusion.

## Status

**Week 2 (Data Analytics) — complete**, compressed to 5 working days.
Next: Week 3 (AI/ML) → Week 4 (Cloud & Infrastructure) → Week 5 (Integrated Project) → Week 6 (Deep Dive & Decision).