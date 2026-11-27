# Agent-based transport demand for a French department

Course project for *Large-scale models and simulation methods* (Université Gustave Eiffel, Autumn 2026).
We build a transport demand pipeline for one French department outside Île-de-France: territorial analysis →
trip generation/attraction → double-constrained gravity model → disaggregation into individual trips → routing on an
OpenStreetMap network. The deliverable is a **PDF report** (LaTeX, in `report/`); the notebooks in `notebooks/` are the only code.
Deadline: 15/01/2027 (e-mail to the lecturer). Department: **Calvados (14), region Normandie**.

## Who does what

| Person | Name | Exercises | Points | Notebooks |
|---|---|---|---|---|
| A | TODO | 1.1 Study area, 1.2 + 1.3 Territorial analysis, 2.1 Trip production, 2.2 Trip attraction | 12 | `ex11` … `ex21_22` |
| B | TODO | 2.3 Trip distribution, 3.1 Disaggregation, 3.2 Routing | 10 | `ex23` … `ex32` |

## Hand-off contract A → B

`data/processed/zones.parquet` is the **only** interface between Person A and Person B. One row per municipality:

| Column | Type | Content |
|---|---|---|
| `municipality_id` | str | INSEE municipality code (unique) |
| `name` | str | municipality name |
| `geometry` | geometry | municipality polygon, EPSG:2154 |
| `O` | float | scaled originating trips O'_i (Exercise 2.2) |
| `D` | float | arriving trips D_j (Exercise 2.2) |

Constraint: `O.sum() == D.sum() == N` (the total number of trips). The row order of the file defines the zone order of all
vectors and matrices in Person B's part. Write it with `write_zones(zones)` (setup cell of ex21_22, validates the
contract) and read it with `read_zones()` (setup cell of ex23). Both notebooks define the contract in `validate_zones`;
if the contract changes, change it in both.

**Starting early:** until ex21_22 is done, Person B can build placeholder zones in ex23 (see the note there):
O = population 15+ and D = URSSAF employment, scaled to the same total. This is **placeholder data**, not the
result of Exercises 2.1/2.2: it creates the marker `data/processed/zones.PLACEHOLDER`, `read_zones()` warns while the
marker exists, and A's final `write_zones(...)` removes it. Do not put placeholder results in the report.

## Setup

```bash
conda env create -f environment.yml
conda activate lsm
jupyter lab             # open notebooks/ and run them in the order below
```

The notebooks are the **only code** of the project (no Python package, no scripts in Git). Each notebook is
self-contained: its first code cell ("Setup and configuration") holds the imports, the study area
(`DEPARTMENT = "14"`), the paths, the parameters it needs and small helpers such as `save_figure`. A value that is used
by several notebooks (e.g. `DEPARTMENT`, `CRS`, the hand-off contract) is defined in each of them: change it everywhere.

## Data

Download the raw data by hand into `data/raw/` (git-ignored); links, the exact file to pick and the known pitfalls
are in [`data/DATA_SOURCES.md`](data/DATA_SOURCES.md). Then adjust the file names in the setup cell of the
notebooks that read them. Local download helpers can live in `scripts/` (git-ignored).
Intermediate files go to `data/processed/` (git-ignored).

## Notebooks

Run in this order (each notebook states what it reads and writes):

| Notebook | Exercise | Person |
|---|---|---|
| `ex11_study_area` | 1.1 | A |
| `ex12_territorial_analysis_I` | 1.2 | A |
| `ex13_territorial_analysis_II` | 1.3 | A |
| `ex21_22_trip_production_attraction` | 2.1 + 2.2, writes `zones.parquet` | A |
| `ex23_trip_distribution` | 2.3 | B |
| `ex31_disaggregation` | 3.1 | B |
| `ex32_routing` | 3.2 | B |

Individual census data: every notebook that needs it reads `data/processed/census_14.parquet` (written by ex11;
`age` = `AGEREV`, age in completed years; `age_aged` = `AGED`, comparison only) and never the raw census CSV.

## Figures → report

Save every report figure with `save_figure(fig, "name")` (setup cell of each notebook): it writes the vector PDF
`report/figures/name.pdf`. In the chapter, replace `\figplaceholder{name}` by `\includegraphics{name}`
(`\graphicspath` points at `figures/`). The figure names are listed at the top of each notebook and match the
placeholders in the chapters.

## Build the report

```powershell
cd report
.\build.ps1          # Windows; ./build.sh on Linux / macOS / Git Bash; add -Clean / clean to delete build/
```

Uses a local `latexmk` or falls back to the `texlive/texlive` Docker image; the result is `report/build/main.pdf`.
Details and troubleshooting: [`report/README.md`](report/README.md). Before submitting: replace every `\todo{...}`
and `\figplaceholder{...}`, fill in all names and e-mail addresses (required by the assignment) in `report/main.tex`.

## Conventions

- One branch per person (`person-a`, `person-b`), merge into `main` through pull requests; the hand-off file
  and its contract are the only coupling.
- Commit notebooks **with their outputs**: before committing, run the notebook top to bottom from a fresh kernel
  ("Restart Kernel and Run All") so that the saved outputs match the code. Also commit LaTeX, bibliography and the
  final figure PDFs in `report/figures/`. **No data, no compiled report PDF and no helper scripts in Git**
  (`.gitignore` enforces this).
- Every random draw uses `SEED` (setup cell of ex31); every parameter is defined in the setup cell of the notebook
  that uses it.
- Every place that needs a result is a visible `\todo{...}` (LaTeX) or `# TODO` (code); search for `TODO` before submitting.
- Document problems as you go (notebook section "Problems encountered" → report): the assignment gives partial points.
