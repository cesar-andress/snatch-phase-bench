# Workspace Policy

## Two synchronized projects

The workspace contains **two independent but synchronized projects**. Do not merge them.

| Project | Location | Purpose | Version control |
|---------|----------|---------|-----------------|
| **Manuscript** | `~/papers/snatch-phase-bench/` | Journal paper: LaTeX, figures, tables, bibliography, writing notes | Independent (not in Git) |
| **Software** | `~/papers/snatch-phase-bench/snatch-phase-bench/` | Canonical repo: code, benchmark, docs, reproducibility, release, Zenodo package | Git (`main` → GitHub / Zenodo) |

### Where content belongs

| Content type | Location |
|--------------|----------|
| Manuscript prose, tables, figures for publication | `~/papers/snatch-phase-bench/paper/` |
| Benchmark / software documentation | `snatch-phase-bench/docs/` |
| Reproducibility documentation | `snatch-phase-bench/docs/reproduction/` |
| Benchmark specifications | `snatch-phase-bench/docs/benchmark/` |
| Release / publication strategy | `snatch-phase-bench/docs/release/` |

### Synchronization rules

- **Do not duplicate** documentation unnecessarily. The software repo holds **operational** docs; the manuscript holds **publication-quality scientific content** only.
- When both must be updated (e.g. dataset taxonomy), change the operational source in `docs/` and reflect the scientific summary in `paper/sections/` — do not copy full operational docs into the manuscript.
- **Never** move the manuscript into the software repository.
- **Never** move software documentation into the manuscript (brief `\repo{...}` pointers in appendices are acceptable).
- **Git commits and pushes apply only** to `~/papers/snatch-phase-bench/snatch-phase-bench/`.

---

## Read-only original repository

The directory `~/papers/Paper_TFM-main` is a **strictly read-only archived snapshot** of the student's submission.

### Never do this inside `Paper_TFM-main`

- Modify, create, delete, or rename files
- Create virtual environments or install packages
- Initialize git, commit, checkout, reset, or clean
- Edit configuration files
- Run `git pull`, `git lfs pull`, or any command that changes the tree

### Allowed inside `Paper_TFM-main`

- Inspect and read files
- Read code and compare against the thesis
- Copy files **out** into this canonical repository when needed

The original repository must remain **byte-for-byte identical** for the entire project lifetime.

## Canonical workspace

**All software development** happens only in:

```text
~/papers/snatch-phase-bench/snatch-phase-bench/
```

The **manuscript** lives alongside it at `~/papers/snatch-phase-bench/paper/` and is versioned independently. See [Two synchronized projects](#two-synchronized-projects) above.

| Activity | Location |
|----------|----------|
| Virtual environments | This repository (e.g. `.venv/`) |
| Package installation | This repository |
| Experiments and training | This repository |
| Outputs and logs | `outputs/` (gitignored) |
| Documentation | `docs/` |
| Git commits and pushes | This repository, branch `main` |

## Using data from the original repository

When baseline files are needed:

1. **Copy** (or obtain from the student) into `data/interim/` or `data/processed/` here.
2. Do **not** require changes to `Paper_TFM-main` for reproduction.
3. Do **not** commit large binaries unless explicitly approved for release.

Example (read-only source, write destination):

```bash
# Read-only: do not cd into Paper_TFM-main for writes
cp -a ~/papers/Paper_TFM-main/data/keypoints/ ./data/interim/keypoints/
cp ~/papers/Paper_TFM-main/data/annotations/master_frame_labels.csv ./data/interim/
```

For Git LFS pointer stubs in the snapshot (`X.npy`, `best_model.pt`, etc.), obtain real binaries from the student and place them under `data/processed/` **here** — never run `git lfs pull` inside the archived snapshot.

## Git workflow

- Single branch: **`main`**
- Remote: `origin` → `git@github-cesar-andress:cesar-andress/snatch-phase-bench.git`
- Commit all substantive changes before pushing
