# Word Puzzle Performance Analyzer — P75

**DOSHI NIRDESH JIGESHKUMAR | IU2441230468 | Roll/serial 75**

Tkinter desktop application for player/puzzle CRUD, dated puzzle attempts, score and completion-time analysis, category/player comparisons, search/filter, and two Matplotlib charts.

## Start

1. Extract ZIP, open terminal in `P75_Word_Puzzle_Analyzer`.
2. Install Python 3.10+ with Tkinter available and a graphical desktop.
3. Run:

```bash
python -m pip install -r requirements.txt
python main.py
```

On Linux use `python3` if needed and install your distribution's `python3-tk` package. Online text-only compilers usually cannot display Tkinter windows.

## Contents

- `main.py` — GUI with Players, Puzzles, Results, Analysis & Charts tabs
- `storage.py` — CSV persistence with header validation and atomic replacement
- `records.py` — validated add/update/delete/search, foreign-key checks
- `analysis.py` — Pandas/NumPy summaries, category/player comparisons, filtering
- `charts.py` — average time by category bar chart and average score by player bar chart
- `sample_data.py` — safe synthetic demo generator, used for included records
- `tests/test_project.py` — automated tests
- `data/` — persistent data in CSV files
- `sample_reports/` — chart images and summary CSVs from demo records

## Use

Players tab: add/edit/delete player names and ages. Puzzles tab: add/edit/delete puzzle titles, categories, and difficulty. Results tab: choose player and puzzle, enter date, score 0–100, time in seconds (positive), and whether completed. Add/update/delete attempts; search in each tab. Parent records with related results are protected against deletion; remove related results first.

Analysis tab: text/category/player/date filters apply to the displayed summary and exported charts. Use **Analyze** for attempts count, average score, mean time, completion percentage, category and player tables, and a descriptive pattern note. Open charts or export two PNG files.

**Interpretation:** The category with highest mean time may be more challenging, but this comparison is descriptive, not a calibrated difficulty measure. All attempts (including incomplete ones) count toward average time and score; completion rate uses Yes/No. A player can have multiple attempts. Recorded scores must be on a 0–100 scale, and times in seconds. Compare categories and players only with attention to sample sizes and difficulty levels.

### Demonstration

Four fictional players, four puzzles (Crossword, Word Search, Anagram, Cryptogram), and 16 fictional attempts are included. No actual player data is claimed. Re-run `python sample_data.py` only on an empty database; it does not overwrite existing rows.

## Testing

```bash
python -m unittest discover -s tests -v
```

Tests cover empty data, CSV persistence, CRUD, validation, parent deletion protection, filtering, summaries, charts and malformed values. GUI interaction requires manual verification on your computer. Sample charts were exported using the non-interactive plotting backend, not desktop screenshots.

## Known boundaries

Single-user CSV app; no login, concurrent editing, network service, or statistical causation claims. Back up `data/` before extensive changes. Unknown IDs, invalid dates and negative/non-finite numbers are rejected in record operations. Two plots are available, and the table allows horizontal scrolling.
