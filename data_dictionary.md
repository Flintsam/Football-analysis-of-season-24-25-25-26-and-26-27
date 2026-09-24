# Football Player & Team Performance — Data Dictionary

## Dataset

**Source:** Football Players Stats — Kaggle
**Kaggle author:** hubertsidorowicz
**Original statistical source:** FBref

**Seasons used:**

* 2024–25
* 2025–26
* 2026–27

The dataset contains player-level football statistics from multiple FBref statistical sections.

---

# 1. Basic Player Information

| Column   | Meaning                    |
| -------- | -------------------------- |
| `Rk`     | Player rank in the dataset |
| `Player` | Player name                |
| `Nation` | Player nationality         |
| `Pos`    | Player position            |
| `Squad`  | Player's team              |
| `Comp`   | Competition/league         |
| `Age`    | Player's age               |
| `Born`   | Player's birth year        |

---

# 2. Standard Statistics

| Column     | Meaning                                  |
| ---------- | ---------------------------------------- |
| `MP`       | Matches played                           |
| `Starts`   | Matches started                          |
| `Min`      | Minutes played                           |
| `90s`      | 90-minute equivalents played             |
| `Gls`      | Goals scored                             |
| `Ast`      | Assists                                  |
| `G+A`      | Goals + assists                          |
| `G-PK`     | Goals excluding penalties                |
| `PK`       | Penalty kicks scored                     |
| `PKatt`    | Penalty kicks attempted                  |
| `CrdY`     | Yellow cards                             |
| `CrdR`     | Red cards                                |
| `xG`       | Expected goals                           |
| `npxG`     | Non-penalty expected goals               |
| `xAG`      | Expected assisted goals                  |
| `npxG+xAG` | Non-penalty xG + xAG                     |
| `PrgC`     | Progressive carries                      |
| `PrgP`     | Progressive passes                       |
| `PrgR`     | Progressive passes received              |
| `G+A-PK`   | Goals excluding penalties + assists      |
| `xG+xAG`   | Expected goals + expected assisted goals |

---

# 3. Shooting Statistics

| Column                 | Meaning                                     |
| ---------------------- | ------------------------------------------- |
| `Sh`                   | Total shots                                 |
| `SoT`                  | Shots on target                             |
| `SoT%`                 | Percentage of shots on target               |
| `Sh/90`                | Shots per 90 minutes                        |
| `SoT/90`               | Shots on target per 90 minutes              |
| `G/Sh`                 | Goals per shot                              |
| `G/SoT`                | Goals per shot on target                    |
| `Dist`                 | Average distance of shots                   |
| `FK`                   | Shots from free kicks                       |
| `PK_stats_shooting`    | Penalty kicks scored in shooting section    |
| `PKatt_stats_shooting` | Penalty kicks attempted in shooting section |
| `xG_stats_shooting`    | Expected goals in shooting section          |
| `npxG_stats_shooting`  | Non-penalty expected goals                  |
| `npxG/Sh`              | Non-penalty xG per shot                     |
| `G-xG`                 | Goals minus expected goals                  |
| `np:G-xG`              | Non-penalty goals minus non-penalty xG      |

---

# 4. Passing Statistics

| Column               | Meaning                                  |
| -------------------- | ---------------------------------------- |
| `Cmp`                | Completed passes                         |
| `Att`                | Passes attempted                         |
| `Cmp%`               | Pass completion percentage               |
| `TotDist`            | Total distance of completed passes       |
| `PrgDist`            | Progressive distance of completed passes |
| `Ast_stats_passing`  | Assists recorded in passing section      |
| `xAG_stats_passing`  | Expected assisted goals                  |
| `xA`                 | Expected assists                         |
| `A-xAG`              | Assists minus expected assisted goals    |
| `KP`                 | Key passes                               |
| `1/3`                | Passes completed into the final third    |
| `PPA`                | Passes into the penalty area             |
| `CrsPA`              | Crosses into the penalty area            |
| `PrgP_stats_passing` | Progressive passes                       |

---

# 5. Passing Types

| Column                    | Meaning                         |
| ------------------------- | ------------------------------- |
| `Att_stats_passing_types` | Total passes attempted          |
| `Live`                    | Live-ball passes                |
| `Dead`                    | Dead-ball passes                |
| `FK_stats_passing_types`  | Free-kick passes                |
| `TB`                      | Through balls                   |
| `Sw`                      | Switches of play                |
| `Crs`                     | Crosses                         |
| `TI`                      | Throw-ins                       |
| `CK`                      | Corner kicks                    |
| `In`                      | Inswinging corners              |
| `Out`                     | Outswinging corners             |
| `Str`                     | Straight/flat corner kicks      |
| `Cmp_stats_passing_types` | Completed passes                |
| `Off`                     | Passes that resulted in offside |
| `Blocks`                  | Passes blocked by opponents     |

---

# 6. Shot-Creating Actions and Goal-Creating Actions

| Column         | Meaning                                      |
| -------------- | -------------------------------------------- |
| `SCA`          | Shot-creating actions                        |
| `SCA90`        | Shot-creating actions per 90 minutes         |
| `PassLive`     | Shot-creating actions from live-ball passes  |
| `PassDead`     | Shot-creating actions from dead-ball passes  |
| `TO`           | Shot-creating actions from take-ons          |
| `Sh_stats_gca` | Shot-creating actions from shots             |
| `Fld`          | Shot-creating actions from fouls drawn       |
| `Def`          | Shot-creating actions from defensive actions |
| `GCA`          | Goal-creating actions                        |
| `GCA90`        | Goal-creating actions per 90 minutes         |

---

# 7. Defensive Statistics

| Column                 | Meaning                                         |
| ---------------------- | ----------------------------------------------- |
| `Tkl`                  | Tackles                                         |
| `TklW`                 | Tackles won                                     |
| `Def 3rd`              | Tackles in defensive third                      |
| `Mid 3rd`              | Tackles in middle third                         |
| `Att 3rd`              | Tackles in attacking third                      |
| `Att_stats_defense`    | Attacking actions/attempts in defensive section |
| `Tkl%`                 | Percentage of tackles won                       |
| `Lost`                 | Tackles lost                                    |
| `Blocks_stats_defense` | Blocks                                          |
| `Sh_stats_defense`     | Shots blocked                                   |
| `Pass`                 | Passes blocked                                  |
| `Int`                  | Interceptions                                   |
| `Tkl+Int`              | Tackles + interceptions                         |
| `Clr`                  | Clearances                                      |
| `Err`                  | Errors leading to opponent shots                |

---

# 8. Possession Statistics

| Column                     | Meaning                                           |
| -------------------------- | ------------------------------------------------- |
| `Touches`                  | Number of touches                                 |
| `Def Pen`                  | Touches in defensive penalty area                 |
| `Def 3rd_stats_possession` | Touches in defensive third                        |
| `Mid 3rd_stats_possession` | Touches in middle third                           |
| `Att 3rd_stats_possession` | Touches in attacking third                        |
| `Att Pen`                  | Touches in attacking penalty area                 |
| `Live_stats_possession`    | Live-ball touches                                 |
| `Att_stats_possession`     | Take-on attempts                                  |
| `Succ`                     | Successful take-ons                               |
| `Succ%`                    | Successful take-on percentage                     |
| `Tkld`                     | Times tackled during take-ons                     |
| `Tkld%`                    | Percentage of take-ons resulting in being tackled |
| `Carries`                  | Times player carried the ball                     |
| `TotDist_stats_possession` | Total distance carried                            |
| `PrgDist_stats_possession` | Progressive distance carried                      |
| `PrgC_stats_possession`    | Progressive carries                               |
| `1/3_stats_possession`     | Carries into the final third                      |
| `CPA`                      | Carries into the penalty area                     |
| `Mis`                      | Miscontrols                                       |
| `Dis`                      | Times dispossessed                                |
| `Rec`                      | Times receiving the ball                          |
| `PrgR_stats_possession`    | Progressive passes received                       |

---

# 9. Playing-Time Statistics

| Column                      | Meaning                                                        |
| --------------------------- | -------------------------------------------------------------- |
| `MP_stats_playing_time`     | Matches played                                                 |
| `Min_stats_playing_time`    | Minutes played                                                 |
| `Mn/MP`                     | Minutes per match                                              |
| `Min%`                      | Percentage of available minutes played                         |
| `90s_stats_playing_time`    | 90-minute equivalents                                          |
| `Starts_stats_playing_time` | Starts                                                         |
| `Mn/Start`                  | Minutes per start                                              |
| `Compl`                     | Complete matches                                               |
| `Subs`                      | Substitute appearances                                         |
| `Mn/Sub`                    | Minutes per substitute appearance                              |
| `unSub`                     | Unused substitute appearances                                  |
| `PPM`                       | Points per match                                               |
| `onG`                       | Team goals while player was on the pitch                       |
| `onGA`                      | Opponent goals while player was on the pitch                   |
| `+/-`                       | Team goal difference while player was on the pitch             |
| `+/-90`                     | Goal difference per 90 minutes while player was on the pitch   |
| `On-Off`                    | Difference in team goal difference with and without the player |
| `onxG`                      | Team expected goals while player was on the pitch              |
| `onxGA`                     | Opponent expected goals while player was on the pitch          |
| `xG+/-`                     | Expected-goal difference while player was on the pitch         |
| `xG+/-90`                   | Expected-goal difference per 90 minutes                        |

---

# 10. Miscellaneous Statistics

| Column            | Meaning                        |
| ----------------- | ------------------------------ |
| `CrdY_stats_misc` | Yellow cards                   |
| `CrdR_stats_misc` | Red cards                      |
| `2CrdY`           | Second-yellow-card dismissals  |
| `Fls`             | Fouls committed                |
| `Fld_stats_misc`  | Fouls drawn                    |
| `Off_stats_misc`  | Offsides                       |
| `Crs_stats_misc`  | Crosses                        |
| `Int_stats_misc`  | Interceptions                  |
| `TklW_stats_misc` | Tackles won                    |
| `PKwon`           | Penalty kicks won              |
| `PKcon`           | Penalty kicks conceded         |
| `OG`              | Own goals                      |
| `Recov`           | Ball recoveries                |
| `Won`             | Aerial duels won               |
| `Lost_stats_misc` | Aerial duels lost              |
| `Won%`            | Percentage of aerial duels won |

---

# 11. Goalkeeping Statistics

| Column  | Meaning                          |
| ------- | -------------------------------- |
| `GA`    | Goals conceded                   |
| `GA90`  | Goals conceded per 90 minutes    |
| `SoTA`  | Shots on target faced            |
| `Saves` | Saves made                       |
| `Save%` | Save percentage                  |
| `W`     | Wins                             |
| `D`     | Draws                            |
| `L`     | Losses                           |
| `CS`    | Clean sheets                     |
| `CS%`   | Clean-sheet percentage           |
| `PKA`   | Penalty kicks faced              |
| `PKsv`  | Penalty kicks saved              |
| `PKm`   | Penalty kicks missed by opponent |

---

# 12. Advanced Goalkeeping Statistics

| Column                 | Meaning            |
| ---------------------- | ------------------ |
| `GA_stats_keeper_adv`  | Goals conceded     |
| `PKA_stats_keeper_adv` | Penalties faced    |
| `FK_stats_keeper_adv`  | Free kicks faced   |
| `CK_stats_keeper_adv`  | Corner kicks faced |
| `OG_stats_keeper_adv`  | Own goals          |
| `PSxG`                 |                    |

