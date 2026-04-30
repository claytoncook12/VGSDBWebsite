# `import_vgsdb_excel` — Excel session importer

Django management command that loads sessions, played tune groups, and tunes from an `.xlsx` file into the `session` app's database.

## Usage

```bash
cd DjangoApp
python manage.py import_vgsdb_excel <path-to-xlsx> [options]
```

### Options

| Flag | Effect |
|---|---|
| `--dry-run` | Parse and validate everything, then roll back. No DB changes. |
| `--sheet <name>` | Use a specific worksheet (defaults to the active sheet). |
| `--strict-tunes` | Error if a tune name fuzzy-matches an existing tune of the same type. |
| `--allow-new-tunes` | Skip near-match warnings; create new tunes silently. Mutually exclusive with `--strict-tunes`. |
| `--fuzzy-cutoff <float>` | difflib similarity threshold (default `0.85`). |

## Required Excel layout

Single sheet, header row first. Columns must appear in this order:

```
session_name | session_date | session_youtube_url |
played_tune_group_number | played_tune_group_start_time |
played_tune_group_end_time | played_tune_group_tunes | offeratory
```

- One row = one `PlayedTuneGroup`. Session columns repeat per group.
- `session_date` may be a date or datetime cell.
- `played_tune_group_start_time` / `_end_time` must be Excel time cells.
- `offeratory` is truthy/blank (e.g. `1` for offertory, blank otherwise).

### `played_tune_group_tunes` cell grammar

```
<TuneType>: <Name1> (<key>), <Name2> (<key>), ...
```

- The prefix before the first top-level `:` is the tune type. Parens inside the prefix are allowed (e.g. `Set Dance (jig): ...`).
- Each tune segment ends with `(<key>)`. Blank key `()` is allowed. A segment with no trailing `(...)` is treated as having a blank key.
- Commas inside parens are ignored when splitting tune segments.

### Allowed values

- **Tune types**: `air`, `an dro`, `barndance`, `fling`, `hop jig`, `hornpipe`, `hymn`, `jig`, `jig/slip jig`, `march`, `mazurka`, `o'carolan`, `polka`, `reel`, `scottish country dance`, `set dance`, `set dance (jig)`, `slide`, `slip jig`, `slow reel`, `song`, `strathspey`, `surf tango`, `waltz`, `welsh`. Common plurals (`reels`, `jigs`, ...) are normalized.
- **Keys**: see `CANONICAL_KEYS` in `commands/import_vgsdb_excel.py`. Blank is valid. Unknown keys raise an error.

## Behavior

- **Idempotent (replace)**: any existing `PlayedTuneGroup` matching `(session, session_order_num)` is deleted (cascade) and re-created from the row. Reruns produce a clean import.
- **Sessions** are matched by `(name, date)` via `get_or_create`; `youtube_url` is backfilled if missing.
- **Tunes** are looked up by an exact lowercased match against any of `name1`–`name4` within the same `TuneType`. If no match, a fuzzy search runs against all tunes of the same type:
  - Default: warn and create a new `Tune`.
  - `--strict-tunes`: raise an error listing the candidates so typos can be fixed before commit.
  - `--allow-new-tunes`: create silently.
- **Whole-import atomicity**: everything runs inside a transaction; any error rolls back all changes.

## Recommended workflow

```bash
# 1. Validate without writing.
python manage.py import_vgsdb_excel ../vgsdb_data.xlsx --dry-run

# 2. Strict pass to surface fuzzy matches (typos).
python manage.py import_vgsdb_excel ../vgsdb_data.xlsx --strict-tunes --dry-run

# 3. Real import.
python manage.py import_vgsdb_excel ../vgsdb_data.xlsx
```

## Common errors

- `Unknown tune type prefix: ...` — fix the prefix in Excel or extend `TUNE_TYPE_NORMALIZE`.
- `Unknown key: ...` — fix the key in Excel or extend `CANONICAL_KEYS`.
- `Tune '<name>' is close to existing tune(s): ...` (only with `--strict-tunes`) — fix the spelling or rerun with `--allow-new-tunes`.
- `Could not find ':' separator` / `Could not parse tune segment` — the tunes cell does not match the grammar above.
