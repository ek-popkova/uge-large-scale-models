# Agent-based transport demand for a French department

Course project for *Large-scale models and simulation methods* (Université Gustave Eiffel, Autumn 2026).
We build a transport demand pipeline for one French department outside Île-de-France: territorial analysis →
trip generation/attraction → double-constrained gravity model → disaggregation into individual trips → routing on an
OpenStreetMap network. The deliverable is a **PDF report** (LaTeX, in `report/`); the code supports it.
Deadline: 15/01/2027 (e-mail to the lecturer). Department: **TODO**.

## Who does what

| Person | Name | Exercises | Points | Notebooks |
|---|---|---|---|---|
| A | TODO | 1.1 Study area, 1.2 + 1.3 Territorial analysis, 2.1 Trip production, 2.2 Trip attraction | 12 | `A1` … `A4` |
| B | TODO | 2.3 Trip distribution, 3.1 Disaggregation, 3.2 Routing | 10 | `B1` … `B3` |

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
vectors and matrices in Person B's part. Write it with `lsm.io.write_zones(zones)` (validates the contract) and read
it with `lsm.io.read_zones()`.

**Starting early:** until A4 is done, Person B can call `lsm.io.write_placeholder_zones()`. It writes zones with
O = population 15+ and D = URSSAF employment, scaled to the same total. This is **placeholder data**, not the
result of Exercises 2.1/2.2: it creates the marker `data/processed/zones.PLACEHOLDER`, `read_zones()` warns while the
marker exists, and A's final `write_zones(...)` removes it. Do not put placeholder results in the report.

## Setup

```bash
conda env create -f environment.yml
conda activate lsm
pip install -e .        # makes `lsm` importable; or rely on the sys.path cell at the top of each notebook
pytest                  # toy example of the gravity model (fails until lsm/gravity.py is implemented)
```

Set the department (`DEPARTMENT`) in `src/lsm/config.py`. Notebooks import the shared package with
`from lsm import config, geo, io, plotting`; their first code cell adds `src/` to `sys.path`, so the editable install is
optional.

## Data

Download the raw data by hand into `data/raw/` (git-ignored); links, the exact file to pick and the known pitfalls
are in [`data/DATA_SOURCES.md`](data/DATA_SOURCES.md). Then adjust the file names in `src/lsm/config.py`.
Intermediate files go to `data/processed/` (git-ignored).

## Notebooks

Run in this order (each notebook states what it reads and writes):

| Notebook | Exercise | Person |
|---|---|---|
| `A1_study_area` | 1.1 | A |
| `A2_territorial_analysis_I` | 1.2 | A |
| `A3_territorial_analysis_II` | 1.3 | A |
| `A4_trip_production_attraction` | 2.1 + 2.2, writes `zones.parquet` | A |
| `B1_trip_distribution` | 2.3 | B |
| `B2_disaggregation` | 3.1 | B |
| `B3_routing` | 3.2 | B |

## Figures → report

Save every report figure with `lsm.plotting.save_figure(fig, "name")`: it writes the vector PDF
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
- Commit sources only: code, notebooks (clear outputs before committing), LaTeX, bibliography and the final figure
  PDFs in `report/figures/`. **No data and no compiled report PDF in Git** (`.gitignore` enforces this).
- Every random draw uses `config.SEED`; every parameter lives in `src/lsm/config.py`.
- Every place that needs a result is a visible `\todo{...}` (LaTeX) or `# TODO` (code); search for `TODO` before submitting.
- Document problems as you go (notebook section "Problems encountered" → report): the assignment gives partial points.
