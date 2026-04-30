"""
Management command to import session data from an Excel (.xlsx) file.

Excel layout (single sheet, first row is header):
    session_name | session_date | session_youtube_url |
    played_tune_group_number | played_tune_group_start_time |
    played_tune_group_end_time | played_tune_group_tunes | offeratory

Each row represents ONE PlayedTuneGroup. The `played_tune_group_tunes` cell
packs the tune type and tunes in the form:

    "<TuneType>: <Name1> (<key>), <Name2> (<key>), ..."

For "set dance (jig)" the prefix itself contains parentheses, e.g.:

    "Set Dance (jig): Some Tune (d)"

For groups containing multiple tune types, separate sub-sections with ';':

    "Barndance: Bill Malley's Barndance (g); An Dro: The Wren (emin)"

Usage:
    python manage.py import_vgsdb_excel path/to/vgsdb_data.xlsx [--dry-run]
"""
import re
from datetime import time, timedelta, datetime
from difflib import get_close_matches

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q

from session.models import (
    Session, PlayedTuneGroup, PlayedTune, Tune, TuneType, Key,
)


# ---------------------------------------------------------------------------
# Tune-type normalization
# ---------------------------------------------------------------------------

CANONICAL_TUNE_TYPES = {
    "5/8",
    "air", "an dro", "barndance", "fling", "hop jig", "hornpipe", "hymn",
    "jig", "jig/slip jig", "lullaby", "march", "mazurka", "o'carolan",
    "polka", "reel", "scottish country dance", "set dance",
    "set dance (jig)", "single reel", "slide", "slip jig", "slow reel", "song",
    "strathspey", "surf tango", "waltz", "welsh",
}

TUNE_TYPE_NORMALIZE = {
    "5/8": "5/8",
    "air": "air", "airs": "air",
    "an dro": "an dro", "an dros": "an dro", "andro": "an dro",
    "barndance": "barndance", "barndances": "barndance",
    "barn dance": "barndance", "barn dances": "barndance",
    "fling": "fling", "flings": "fling",
    "hop jig": "hop jig", "hop jigs": "hop jig",
    "hornpipe": "hornpipe", "hornpipes": "hornpipe",
    "hymn": "hymn", "hymns": "hymn",
    "jig": "jig", "jigs": "jig",
    "jig/slip jig": "jig/slip jig", "jig/slip jigs": "jig/slip jig",
    "lullaby": "lullaby", "lullabies": "lullaby",
    "march": "march", "marches": "march",
    "mazurka": "mazurka", "mazurkas": "mazurka",
    "o'carolan": "o'carolan", "ocarolan": "o'carolan",
    "polka": "polka", "polkas": "polka",
    "reel": "reel", "reels": "reel",
    "scottish country dance": "scottish country dance",
    "scottish country dances": "scottish country dance",
    "set dance": "set dance", "set dances": "set dance",
    "set dance (jig)": "set dance (jig)",
    "set dances (jig)": "set dance (jig)",
    "single reel": "single reel", "single reels": "single reel",
    "slide": "slide", "slides": "slide",
    "slip jig": "slip jig", "slip jigs": "slip jig",
    "slow reel": "slow reel", "slow reels": "slow reel",
    "song": "song", "songs": "song",
    "strathspey": "strathspey", "strathspeys": "strathspey",
    "surf tango": "surf tango", "surf tangos": "surf tango",
    "waltz": "waltz", "waltzes": "waltz",
    "welsh": "welsh",
}


def _normalize_text(s):
    """Lowercase and replace curly apostrophes with straight ones."""
    return s.replace("\u2019", "'").strip().lower()


def normalize_tune_type(prefix):
    key = _normalize_text(prefix)
    if key not in TUNE_TYPE_NORMALIZE:
        raise ValueError(
            f"Unknown tune type prefix: {prefix!r} (normalized: {key!r}). "
            f"Add it to TUNE_TYPE_NORMALIZE."
        )
    return TUNE_TYPE_NORMALIZE[key]


# ---------------------------------------------------------------------------
# Key (musical key) allow-list
# ---------------------------------------------------------------------------

CANONICAL_KEYS = {
    "",  # blank is valid
    "a", "a & d", "a & g", "a & gmix", "a min & g",
    "adorian", "amin", "amin & c", "amin & e", "amin & emin", "amix",
    "b", "bmin", "bmin & d",
    "c",
    "d", "d & a", "d & f#min", "d & g",
    "ddorian", "dmin", "dmix", "dmodal",
    "e", "emin", "emin & bmin", "emin & c", "emin & d", "emin & e", "emin & g",
    "f", "f#min", "f#min & a",
    "g", "g & a", "g & amin", "g & emin", "g and a",
    "gmin", "gmodal",
    "modal",
}


def normalize_key(raw):
    """
    Normalize a key string and validate against CANONICAL_KEYS.

    Lowercases, replaces curly apostrophes, and collapses internal whitespace.
    Raises ValueError on unknown keys.
    """
    if raw is None:
        normalized = ""
    else:
        normalized = _normalize_text(str(raw))
        # Collapse runs of whitespace (e.g. "a min  & g" -> "a min & g").
        normalized = re.sub(r"\s+", " ", normalized)

    if normalized not in CANONICAL_KEYS:
        raise ValueError(
            f"Unknown key: {raw!r} (normalized: {normalized!r}). "
            f"Add it to CANONICAL_KEYS if it is valid."
        )
    return normalized


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

# Matches "<name> (<key>)" at the end of a tune item.
# Uses the LAST parenthesized group as the key. The key may be empty
# (e.g. "Tune Name ()") to indicate a blank key. If no trailing "(...)"
# is present at all, the whole string is the name and the key is blank.
TUNE_RE = re.compile(r"^(?P<name>.+?)\s*\((?P<key>[^()]*)\)\s*$")


def time_to_timedelta(t):
    if t is None:
        raise ValueError("Missing time value.")
    if isinstance(t, timedelta):
        return t
    if isinstance(t, time):
        return timedelta(
            hours=t.hour, minutes=t.minute,
            seconds=t.second, microseconds=t.microsecond,
        )
    if isinstance(t, datetime):
        return timedelta(
            hours=t.hour, minutes=t.minute,
            seconds=t.second, microseconds=t.microsecond,
        )
    raise ValueError(f"Unexpected time value: {t!r} ({type(t).__name__})")


def split_prefix_and_rest(cell_text):
    """
    Split "<prefix>: <rest>" while allowing parentheses in the prefix
    (e.g. "Set Dance (jig): ...").

    We split on the FIRST colon that is not inside parentheses.
    """
    depth = 0
    for i, ch in enumerate(cell_text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch == ":" and depth == 0:
            return cell_text[:i].strip(), cell_text[i + 1:].strip()
    raise ValueError(f"Could not find ':' separator in tunes cell: {cell_text!r}")


def parse_tunes_cell(cell_text):
    """
    Parse a tunes cell into a flat ordered list of (tune_type, name, key).

    Single-type cell:
        'Reels: Foo (d), Bar (emin)'
        -> [('reel', 'Foo', 'd'), ('reel', 'Bar', 'emin')]

    Multi-type cell (sub-sections separated by ';'), each sub-section follows
    the same '<TuneType>: <tunes...>' grammar:
        'Barndance: Bill (g); An Dro: Wren (emin)'
        -> [('barndance', 'Bill', 'g'), ('an dro', 'Wren', 'emin')]
    """
    if not cell_text or not str(cell_text).strip():
        raise ValueError("Empty tunes cell.")

    text = str(cell_text)

    # Split top-level sub-sections on ';' (parens aware, just in case).
    sections = _split_top_level(text, ";")

    out = []
    for section in sections:
        section = section.strip()
        if not section:
            continue
        prefix, rest = split_prefix_and_rest(section)
        tune_type = normalize_tune_type(prefix)

        # Split items on commas that are NOT inside parentheses.
        parts = re.split(r",\s*(?![^()]*\))", rest)
        for part in parts:
            item = part.strip()
            if not item:
                continue
            m = TUNE_RE.match(item)
            if m:
                name = m.group("name").strip().rstrip(",").strip()
                key = normalize_key(m.group("key"))
            else:
                # No trailing "(...)" — treat the whole item as the name with a blank key.
                name = item.rstrip(",").strip()
                key = normalize_key("")
            if not name:
                raise ValueError(
                    f"Empty tune name in segment {item!r} of cell {cell_text!r}"
                )
            out.append((tune_type, name, key))

    if not out:
        raise ValueError(f"No tunes parsed from cell: {cell_text!r}")

    return out


def _split_top_level(text, sep):
    """Split `text` on `sep` characters that are NOT inside parentheses."""
    parts = []
    buf = []
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
            buf.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1)
            buf.append(ch)
        elif ch == sep and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return parts


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

EXPECTED_HEADER = (
    "session_name", "session_date", "session_youtube_url",
    "played_tune_group_number", "played_tune_group_start_time",
    "played_tune_group_end_time", "played_tune_group_tunes", "offeratory",
)


class Command(BaseCommand):
    help = "Import sessions, played tune groups, and tunes from a vgsdb Excel file."

    def add_arguments(self, parser):
        parser.add_argument("xlsx_path", help="Path to the .xlsx file to import.")
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Parse and validate without committing to the database.",
        )
        parser.add_argument(
            "--sheet", default=None,
            help="Worksheet name (defaults to the active sheet).",
        )
        parser.add_argument(
            "--strict-tunes", action="store_true",
            help=(
                "Refuse to create a new Tune if a fuzzy match against existing "
                "tunes of the same TuneType is found. Use this to catch typos."
            ),
        )
        parser.add_argument(
            "--allow-new-tunes", action="store_true",
            help=(
                "Silence near-match warnings and create new Tune rows freely. "
                "Overrides the warnings printed by default. Cannot be combined "
                "with --strict-tunes."
            ),
        )
        parser.add_argument(
            "--fuzzy-cutoff", type=float, default=0.85,
            help="difflib similarity cutoff for fuzzy matches (default: 0.85).",
        )

    def handle(self, *args, xlsx_path, dry_run, sheet,
               strict_tunes, allow_new_tunes, fuzzy_cutoff, **opts):
        if strict_tunes and allow_new_tunes:
            raise CommandError(
                "--strict-tunes and --allow-new-tunes are mutually exclusive."
            )
        self.strict_tunes = strict_tunes
        self.allow_new_tunes = allow_new_tunes
        self.fuzzy_cutoff = fuzzy_cutoff
        try:
            import openpyxl
        except ImportError as exc:
            raise CommandError(
                "openpyxl is required. Install with `pip install openpyxl`."
            ) from exc

        try:
            wb = openpyxl.load_workbook(xlsx_path, data_only=True)
        except FileNotFoundError as exc:
            raise CommandError(f"File not found: {xlsx_path}") from exc

        ws = wb[sheet] if sheet else wb.active

        rows_iter = ws.iter_rows(values_only=True)
        try:
            header = next(rows_iter)
        except StopIteration:
            raise CommandError("Worksheet is empty.")

        header_norm = tuple(
            (h or "").strip().lower() for h in header[:len(EXPECTED_HEADER)]
        )
        if header_norm != EXPECTED_HEADER:
            raise CommandError(
                f"Unexpected header.\n  expected: {EXPECTED_HEADER}\n  got:      {header_norm}"
            )

        try:
            with transaction.atomic():
                stats = self._import_rows(rows_iter)
                if dry_run:
                    self.stdout.write(self.style.WARNING(
                        "Dry run requested — rolling back transaction. "
                        "No DB changes were committed (any 'NEAR-MATCH' "
                        "messages above describe what WOULD have been created)."
                    ))
                    raise _DryRunRollback(stats)
        except _DryRunRollback as rb:
            stats = rb.stats

        self.stdout.write(self.style.SUCCESS(
            f"Done. sessions={stats['sessions']} "
            f"groups={stats['groups']} tunes_played={stats['played_tunes']}"
        ))

    # ------------------------------------------------------------------
    def _import_rows(self, rows_iter):
        sessions_seen = set()
        groups_created = 0
        played_tunes_created = 0

        for row_num, row in enumerate(rows_iter, start=2):
            # Skip fully-blank rows.
            if row is None or all(v is None for v in row):
                continue

            try:
                (s_name, s_date, s_url,
                 group_num, start_t, end_t, tunes_text, offertory) = row[:8]
            except ValueError as exc:
                raise CommandError(f"Row {row_num}: bad shape: {row!r}") from exc

            if s_name is None or s_date is None or group_num is None:
                raise CommandError(
                    f"Row {row_num}: session_name, session_date, and "
                    f"played_tune_group_number are required."
                )

            # Skip rows scaffolded with session metadata but no group data yet
            # (no start time and no tunes text).
            if start_t is None and (tunes_text is None or not str(tunes_text).strip()):
                self.stdout.write(
                    f"Row {row_num}: skipping (no start_time / tunes filled in yet)."
                )
                continue

            session_date = s_date.date() if isinstance(s_date, datetime) else s_date

            session, _created = Session.objects.get_or_create(
                name=str(s_name).lower(),
                date=session_date,
                defaults={"youtube_url": s_url or ""},
            )
            # Backfill youtube_url if it was missing previously.
            if s_url and not session.youtube_url:
                session.youtube_url = s_url
                session.save(update_fields=["youtube_url"])
            sessions_seen.add(session.pk)

            try:
                start_td = time_to_timedelta(start_t)
                end_td = time_to_timedelta(end_t) if end_t is not None else None
            except ValueError as exc:
                raise CommandError(f"Row {row_num}: {exc}") from exc

            # Idempotency (Replace): drop any existing group with the same
            # (session, session_order_num); cascade removes its PlayedTunes.
            PlayedTuneGroup.objects.filter(
                session=session,
                session_order_num=int(group_num),
            ).delete()

            ptg = PlayedTuneGroup.objects.create(
                session=session,
                session_order_num=int(group_num),
                start_time=start_td,
                end_time=end_td,
                offertory=bool(offertory),
                teaching=False,
            )
            groups_created += 1

            try:
                tunes = parse_tunes_cell(tunes_text)
            except ValueError as exc:
                raise CommandError(f"Row {row_num}: {exc}") from exc

            tune_type_cache = {}

            for order, (tune_type_str, name, key_str) in enumerate(tunes, start=1):
                if tune_type_str not in tune_type_cache:
                    tune_type_cache[tune_type_str], _ = TuneType.objects.get_or_create(
                        tune_type_char=tune_type_str,
                    )
                tune_type = tune_type_cache[tune_type_str]
                key, _ = Key.objects.get_or_create(key_type_char=key_str)
                try:
                    tune = self._resolve_tune(name, tune_type, row_num)
                except ValueError as exc:
                    raise CommandError(f"Row {row_num}: {exc}") from exc
                PlayedTune.objects.create(
                    tune=tune,
                    played_tune_group=ptg,
                    key=key,
                    group_order_num=order,
                )
                played_tunes_created += 1

            types_summary = ",".join(sorted({t for t, _, _ in tunes}))
            self.stdout.write(
                f"Row {row_num}: session={session.pk} group#{group_num} "
                f"types={types_summary} tunes={len(tunes)}"
            )

        return {
            "sessions": len(sessions_seen),
            "groups": groups_created,
            "played_tunes": played_tunes_created,
        }

    # ------------------------------------------------------------------
    def _resolve_tune(self, raw_name, tune_type, row_num):
        """
        Find or create a Tune for (name, tune_type).

        Lookup order:
          1. Exact match on any of name1..name4 (lowercased), same tune_type.
          2. Fuzzy match against name1..name4 of all tunes of the same type.
             - If --strict-tunes: raise.
             - Else: warn (unless --allow-new-tunes) and create a new Tune.
          3. Otherwise: create a new Tune.
        """
        name = _normalize_text(raw_name)

        # 1. Exact cross-name match.
        existing = Tune.objects.filter(tune_type=tune_type).filter(
            Q(name1=name) | Q(name2=name) | Q(name3=name) | Q(name4=name)
        ).first()
        if existing is not None:
            return existing

        # 2. Fuzzy match against existing tunes of the same type.
        same_type = list(Tune.objects.filter(tune_type=tune_type))
        candidates = []  # list[(score_name, tune)] simplified to just tunes
        # Build a flat list of (name_value, tune) pairs for matching.
        index = []
        for t in same_type:
            for field_val in (t.name1, t.name2, t.name3, t.name4):
                if field_val:
                    index.append((field_val, t))

        if index:
            names_only = [n for n, _ in index]
            close = get_close_matches(
                name, names_only, n=3, cutoff=self.fuzzy_cutoff,
            )
            if close:
                # Map matched names back to unique tunes (preserve order).
                seen_pks = set()
                for matched_name in close:
                    for n_val, t in index:
                        if n_val == matched_name and t.pk not in seen_pks:
                            seen_pks.add(t.pk)
                            candidates.append((matched_name, t))

        if candidates:
            details = ", ".join(
                f"{t.name1!r} (pk={t.pk}, matched on {mn!r})"
                for mn, t in candidates
            )
            if self.strict_tunes:
                raise ValueError(
                    f"Tune {raw_name!r} ({tune_type.tune_type_char}) is close to "
                    f"existing tune(s): {details}. Fix the spelling in the "
                    f"Excel file, or rerun with --allow-new-tunes."
                )
            if not self.allow_new_tunes:
                self.stdout.write(self.style.WARNING(
                    f"Row {row_num}: NEAR-MATCH — creating a NEW Tune row "
                    f"{raw_name!r} ({tune_type.tune_type_char}); will NOT "
                    f"be merged with existing: {details}. "
                    f"If they are the same tune, fix the Excel spelling or "
                    f"add it as an alternate name (name2..name4) on the "
                    f"existing Tune, then rerun."
                ))

        # 3. Create new tune.
        tune = Tune.objects.create(name1=name, tune_type=tune_type)
        return tune


class _DryRunRollback(Exception):
    """Internal — used to roll back the transaction in dry-run mode."""
    def __init__(self, stats):
        super().__init__("dry run")
        self.stats = stats
