# Data sources

All raw data goes into `data/raw/` (git-ignored). Only the aggregated census (row 2) is downloaded by a notebook (ex12, if missing); everything else by hand.
Record the download date and the exact file name you used (they belong in the report appendix).
The department (`DEPARTMENT = "14"`, Calvados) and the raw file names are set in the setup cell of each notebook;
replace the `TODO_...` file names there.

| # | Data set | Link | File to pick |
|---|---|---|---|
| 1 | INSEE detailed census 2019, "Individus localisés au canton-ou-ville" | <https://www.insee.fr/fr/statistiques/6544333> | The CSV zip of the **zone that contains our department** (the page lists which departments belong to which zone). By analogy with `RP2019_INDCVIZA_csv.zip` / `FD_INDCVIZA_2019.csv` (zone A = Île-de-France) the pattern is `RP2019_INDCVIZ<letter>_csv.zip` containing `FD_INDCVIZ<letter>_2019.csv` (verify). Also useful: the variable dictionary `Varmod_INDCVI_2019.csv`. Semicolon-separated. |
| 2 | INSEE aggregated census, "Population en 2019 – IRIS" | <https://www.insee.fr/fr/statistiques/6543200> | "Population en 2019 – IRIS – France hors Mayotte", CSV (semicolon-separated). Needed: population 15+ by SPC per IRIS (columns like `C19_POP15P_CS1` … `C19_POP15P_CS8`, verify). |
| 3 | IGN CONTOURS-IRIS **2021 edition** | <https://geoservices.ign.fr/contoursiris> | Shapefile, LAMB93 / RGF93 (EPSG:2154). The assignment (Autumn 2026) says: go to <https://cartes.gouv.fr/rechercher-une-donnee/dataset/IGNF_CONTOURS-IRIS>, scroll to "API" → "Data Download", download icon; Zone = France Métropolitaine, Format = SHP, CRS = RGF93; one file remains, a `.7z` archive (needs 7-Zip or similar to unpack). |
| 4 | URSSAF employees per municipality × APE | <https://open.urssaf.fr/explore/dataset/etablissements-et-effectifs-salaries-au-niveau-commune-x-ape-last/information/> | Tab "Export" → CSV. Private-sector salaried employment only. Check the separator and column names. |
| 5 | Geofabrik OpenStreetMap extract | <http://download.geofabrik.de/europe/france.html> | `<region>-latest.osm.pbf` of the **region that contains our department** (sub-region page under `europe/france/`). |

## Downloaded for Exercise 1.1 (2026-11-27)

| File in `data/raw/` | Source |
|---|---|
| `FD_INDCVIZB_2019.csv` (~930 MB), `Varmod_INDCVI_2019.csv` | <https://www.insee.fr/fr/statistiques/fichier/6544333/RP2019_INDCVIZB_csv.zip> (zone B = Centre-Val de Loire, Bourgogne-Franche-Comté, **Normandie**, Hauts-de-France) |
| `dictionnaire_indcvi_rp2019.pdf` | <https://www.insee.fr/fr/statistiques/fichier/6544333/dictionnaire_indcvi_rp2019.pdf> |
| `CONTOURS-IRIS.{shp,shx,dbf,prj,cpg}` | <https://data.geopf.fr/telechargement/download/CONTOURS-IRIS/CONTOURS-IRIS_2-1__SHP__FRA_2021-01-01/CONTOURS-IRIS_2-1__SHP__FRA_2021-01-01.7z>, folder `CONTOURS-IRIS/1_DONNEES_LIVRAISON_2021-06-00217/CONTOURS-IRIS_2-1_SHP_LAMB93_FXX-2021/` |

Unpacking the `.7z` on Windows: without 7-Zip, `pip install py7zr` works. Extract into a **short** folder (e.g. a temp
folder), not inside the project: the archive's nested folder names exceed the Windows 260-character path limit when
the project lives in a long OneDrive path. Then copy only the `CONTOURS-IRIS.*` files into `data/raw/`. The shapefile
is UTF-8 encoded and its `.prj` (IGNF:LAMB93) is the same CRS as EPSG:2154.

## Downloaded for Exercise 1.2 (2026-11-27)

| File in `data/raw/` | Source |
|---|---|
| `base-ic-evol-struct-pop-2019.CSV`, `meta_base-ic-evol-struct-pop-2019.CSV` (variable dictionary) | <https://www.insee.fr/fr/statistiques/fichier/6543200/base-ic-evol-struct-pop-2019_csv.zip> ("Population en 2019 – IRIS – France hors Mayotte"); the data cell of `ex12` downloads it if missing |

## Known pitfalls

- **Age variable.** The detailed census has `AGED` (census year minus birth year) and `AGEREV` (completed years).
  The age bands of the aggregated census are in completed years; use `AGEREV` (Ex. 1.2).

- **Weights.** Use the weight `IPONDI` for anything about persons in the detailed census: the number of
  persons is `sum(IPONDI)`, not the number of rows; means, histograms and shares must be weighted too.
- **Canton-ou-ville localisation.** The detailed census is localised at canton-ou-ville level: persons in small
  municipalities have no IRIS code (`IRIS` is a placeholder such as `ZZZZZZZZZ`), so not every municipality can be
  identified there. Decide how to handle this (e.g. restrict municipality statistics to identifiable
  municipalities, or use the aggregated census where municipality-level numbers are needed), apply it
  consistently, and **describe it in the report** (Exercises 1.1 and 1.2).
- **Municipality codes.** Municipality codes can differ between sources (merged communes, code vintages;
  arrondissements of Paris/Lyon/Marseille; Corsica `2A`/`2B` are strings). Check every join: count unmatched keys on
  both sides before and after merging.
- **Trip generation.** `O_i = max(β0 + Σ_s β_s n_s, 0)`: the intercept β0 is added **once**, not once per SPC
  (the course notebook 02 adds it 8 times). Because of β0 and the `max`, the total depends on the zone level the
  model is applied to (IRIS vs. municipality); decide and document.
- **Friction.** `ρ_ij = exp(β d_ij)` with β = −1.1e-4 (d in metres). Table 2 of the assignment lists a second
  parameter, −0.4, which is a constant intercept in the exponent (`ρ_ij = exp(β d_ij + α)`, α = −0.4; the symbols were
  lost in the text export, confirm in the PDF). It cancels in the double-constrained balancing (absorbed by `p_i`,
  `a_j`) and does not change `F_ij`; the setup cell of ex23 keeps both.
- **Toy example.** In the toy example of the assignment, `D_1` must be **420** (the PDF prints 9462 by mistake; 9462 is
  `d_14`). Note that 420 + 2294 + 48377 + 6621 = 57712 while ΣO = 57715 (Table 5 is rounded down): with
  `D_1 = 423` the totals balance and the floored flows match Table 5 exactly. The toy-example cell of ex23
  checks both.
- **Departure time.** `T ~ N(μ, σ = 3600 s)`: the assignment text reads μ = "83600", which looks like a lost
  multiplication sign (8·3600 = 28 800 s, 08:00). The setup cell of ex31 uses `8 * 3600`; confirm in the PDF.
