# Report (LaTeX)

```
report/
├── main.tex              # entry point: metadata + list of chapters
├── preamble.tex          # packages, layout, macros (\todo, \code, \figplaceholder, transport notation)
├── frontmatter/          # title page
├── chapters/             # one .tex per section:
│   ├── 00_introduction
│   ├── 01_study_area                (Ex 1.1)    02_territorial_analysis_I   (Ex 1.2)
│   ├── 03_territorial_analysis_II   (Ex 1.3)    04_trip_production         (Ex 2.1)
│   ├── 05_trip_attraction           (Ex 2.2)    06_trip_distribution       (Ex 2.3)
│   ├── 07_disaggregation            (Ex 3.1)    08_routing                 (Ex 3.2)
│   └── 09_discussion  A_appendix
├── figures/              # plots/images used by the report (PDF preferred)
├── bibliography/         # references.bib
├── .latexmkrc            # build config (output goes to build/)
├── build.ps1 / build.sh  # build scripts
└── build/                # generated, git-ignored (main.pdf is here)
```

The result of a build is always **`report/build/main.pdf`**.

## Building the PDF

You need **either** a local TeX Live (with `latexmk`) **or** Docker. Docker is the easiest option:
nothing has to be installed except Docker itself, and everyone on the team gets the same LaTeX version.

### Option 1: Docker (recommended)

**1. Prerequisites.** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and
**start it**; wait until it reports that the engine is running. Check with:

```
docker info
```

If this prints `failed to connect to the docker API ... daemon is running`, Docker Desktop is not started yet.

**2. Build with the script** (run from the `report/` folder). It uses the `texlive/texlive` image and
downloads it automatically on the first run (several GB, so the first build takes a while; later builds are fast).

```powershell
# Windows PowerShell
cd report
.\build.ps1
```

```bash
# Linux / macOS / Git Bash
cd report
./build.sh
```

If you get "running scripts is disabled" in PowerShell, run once:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

**3. Or run the container by hand** (what the scripts do internally). The current folder is mounted into the
container as `/doc`, and `latexmk` runs pdflatex and bibtex as many times as needed:

```powershell
# Windows PowerShell, from report/
docker run --rm -v "${PWD}:/doc" -w /doc texlive/texlive:latest latexmk main.tex
```

```bash
# Linux / macOS, from report/
docker run --rm -v "$PWD:/doc" -w /doc texlive/texlive:latest latexmk main.tex

# Git Bash on Windows needs MSYS_NO_PATHCONV=1 in front of docker
MSYS_NO_PATHCONV=1 docker run --rm -v "$PWD:/doc" -w /doc texlive/texlive:latest latexmk main.tex
```

**4. Interactive container** (to experiment or debug a build):

```powershell
docker run -it --rm -v "${PWD}:/doc" -w /doc texlive/texlive:latest bash
# inside the container:
latexmk main.tex          # build
latexmk -C                # clean everything
exit
```

`--rm` deletes the container when it exits. Your files are not lost: they live in the mounted `report/` folder.

### Option 2: local TeX Live / MiKTeX

If `latexmk` is on your `PATH`, the scripts use it instead of Docker. You can also call it directly:

```
latexmk main.tex
```

In VS Code, the LaTeX Workshop extension picks up `.latexmkrc` automatically.

### Cleaning

```powershell
.\build.ps1 -Clean     # Windows
./build.sh clean       # Linux / macOS / Git Bash
```

This simply deletes the `build/` folder.

## Troubleshooting

| Problem | Fix |
|---|---|
| `failed to connect to the docker API` | Docker Desktop is not running. Start it and retry. |
| Build fails with a LaTeX error | Open `build/main.log` and search for `!` (error) or the `.tex:LINE:` pattern (`-file-line-error` is on). |
| `??` instead of citation or reference numbers | Normally fixed within the same `latexmk` run. If it persists, run `.\build.ps1 -Clean` and build again. |
| `Citation ... undefined` | The key is missing in `bibliography/references.bib`, or it is misspelled. |
| `File '...pdf' not found` | Put the figure into `figures/` (the notebooks do this via `lsm.plotting.save_figure`) and reference it by file name only, without the folder. |
| `Missing character` / `Undefined control sequence` around an underscore | Escape `_` as `\_` in text, or wrap file names in `\code{\detokenize{my_file}}`. |
| Files in `build/` belong to root (Linux) | Docker wrote them as root: `sudo chown -R "$USER" build`. |
| `Mount denied` / empty folder in the container (Windows) | Docker Desktop, Settings, Resources, File sharing: make sure the drive with the project is shared. |

## Conventions

- **One chapter = one file** in `chapters/`. Add a new chapter to the list in `main.tex`. Chapters are pulled in with
  `\input` (not `\include`), so they do not force page breaks.
- **Structure of an exercise chapter:** `\section` with the line `Responsible: Person A/B`, one `\subsection` per
  question of the assignment with its points in the title, then `\paragraph{Method.}`, a figure/table placeholder, and
  `\paragraph{Result.}`; the chapter ends with `\paragraph{Problems encountered.}` (partial points are given for
  documented problems).
- **Placeholders:** use `\todo{...}` (red, visible in the PDF) and `\figplaceholder{name}` for a figure that does not
  exist yet. Search for `TODO` before submitting; no red text may remain in the final PDF. Do not put `\todo` in
  section titles (it would end up in the table of contents).
- **Figures:** save plots from the notebooks with `lsm.plotting.save_figure(fig, "name")`, which writes
  `report/figures/name.pdf` (vector). Reference them by name only (`\includegraphics{name}`, thanks to
  `\graphicspath`) and replace the `\figplaceholder{name}` call.
- **Notation:** `\Oi`, `\Dj`, `\Fij`, `\dij`, `\rhoij`, `\Oprime`, `\pii`, `\aj` (see `preamble.tex`).
- **Cross-references:** label as `sec:`, `fig:`, `tab:`, `eq:` and use `\cref{...}`.
- **Citations:** add entries to `bibliography/references.bib`, cite with `\cite{key}`.
- **Commit only sources.** `build/` and all LaTeX intermediates are git-ignored; do not commit the compiled PDF.
  The final figure PDFs in `figures/` are committed because the report needs them.
- **Authors:** the assignment requires all names and e-mail addresses on the report; edit them (and the repository
  URL) at the top of `main.tex`. Edit the department in `\reporttitle`.
