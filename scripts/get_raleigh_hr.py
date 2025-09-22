#!/usr/bin/env python3
# scripts/get_raleigh_hr.py

import sys, shlex, re
from pathlib import Path

def _norm_key(k: str) -> str:
    k = k.strip().lower()
    if k in ("output","outfile","path"): k = "out"
    if k in ("start_date","from","date_from"): k = "start"
    if k in ("end_date","to","date_to"): k = "end"
    if k in ("in","input_file","source"): k = "input"
    if k in ("csv","out_csv_path","csv_path"): k = "out_csv"
    if k in ("json","out_json_path","json_path"): k = "out_json"
    return k

def _kv_to_cli(d: dict) -> list[str]:
    args = []
    for k, v in d.items():
        if v is None or str(v).strip() == "": continue
        args.extend([f"--{_norm_key(k)}", str(v).strip()])
    return args

def _parse_params_file(p: Path) -> list[str]:
    raw = p.read_text(encoding="utf-8", errors="ignore")
    lines = [re.sub(r"#.*$", "", ln).strip() for ln in raw.splitlines()]
    lines = [ln for ln in lines if ln]

    joined = " ".join(lines)
    if "--" in joined:
        return shlex.split(joined)

    kv = {}
    for ln in lines:
        if "=" in ln:
            k, v = ln.split("=", 1); kv[_norm_key(k)] = v.strip()
        elif ":" in ln:
            k, v = ln.split(":", 1); kv[_norm_key(k)] = v.strip()

    args = _kv_to_cli(kv)
    return args or shlex.split(joined)

# Only apply parameters.txt when user didn’t pass args
if len(sys.argv) == 1:
    _pf = Path(__file__).with_name("parameters.txt")
    if _pf.exists():
        try:
            _extra = _parse_params_file(_pf)
            if _extra: sys.argv.extend(_extra)
        except Exception:
            pass

import argparse, json, time, datetime as dt
from typing import Dict, Any, Optional, Tuple, List

import pandas as pd
import requests

# Optional Statcast fetch (only needed if you do NOT pass --input)
try:
    from pybaseball import statcast_batter
    HAVE_PYBASEBALL = True
except Exception:
    HAVE_PYBASEBALL = False

CAL_RALEIGH_MLBAM_ID = 663728
MARINERS_TEAM_ID = 136  # NEW: for schedule lookup
FEED_LIVE_URL = "https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
SCHEDULE_URL = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId={team_id}&startDate={start}&endDate={end}"  # NEW
CACHE_PATH = Path(".feed_live_cache.json")
REQUEST_TIMEOUT = 20
REQUEST_SLEEP = 0.25  # polite pacing

# --------------------------------- default dates (2025 season only) ---------------------------------
_today = dt.date.today()
_season_start = dt.date(2025, 3, 27)      # Opening Day 2025
_default_start = _season_start.isoformat()
_default_end = _today.isoformat()

# --------------------------------- argparse ---------------------------------
ap = argparse.ArgumentParser(description="Cal Raleigh HRs (2025): complete distances + venue enrichment (+ JSON export)")
ap.add_argument("--input", help="Existing CSV with Statcast rows (optional). If omitted, fetches Statcast.")
ap.add_argument("--out_csv", default="assets/data/raleigh_hr.csv",
                help="CSV output path (default: assets/data/raleigh_hr.csv)")
ap.add_argument("--out_json", default="assets/data/raleigh_hr.json",
                help="JSON output path (default: assets/data/raleigh_hr.json)")
ap.add_argument("--start", default=_default_start, help=f"Start date YYYY-MM-DD (default: {_default_start})")
ap.add_argument("--end",   default=_default_end,   help=f"End date   YYYY-MM-DD (default: {_default_end})")
args = ap.parse_args()

# Ensure output folders exist
Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)

# --------------------------------- caching ----------------------------------
def load_cache() -> Dict[str, Any]:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_cache(cache: Dict[str, Any]) -> None:
    try:
        CACHE_PATH.write_text(json.dumps(cache), encoding="utf-8")
    except Exception:
        pass

def get_feed_live(game_pk: int, cache: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    k = str(game_pk)
    if k in cache:
        return cache[k]
    try:
        r = requests.get(FEED_LIVE_URL.format(game_pk=game_pk), timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            data = r.json()
            cache[k] = data
            save_cache(cache)
            time.sleep(REQUEST_SLEEP)
            return data
    except Exception:
        return None
    return None

# ------------------------------ feed parsing --------------------------------
def extract_total_distance_and_venue(feed: Dict[str, Any], at_bat_index: int) -> Tuple[Optional[float], Optional[str]]:
    """Return (totalDistance_ft, venue_name) for the given at-bat index."""
    venue = None
    try:
        venue = feed["gameData"]["venue"]["name"]
    except Exception:
        pass

    try:
        plays = feed["liveData"]["plays"]["allPlays"]
    except Exception:
        return (None, venue)

    for play in plays:
        try:
            if int(play.get("about", {}).get("atBatIndex", -1)) != int(at_bat_index):
                continue
            for ev in play.get("playEvents", []):
                hd = ev.get("hitData")
                if not hd:
                    continue
                td = hd.get("totalDistance")
                if td is None:
                    continue
                try:
                    return (float(td), venue)
                except Exception:
                    s = "".join(ch for ch in str(td) if ch.isdigit() or ch in ".-")
                    return (float(s), venue) if s else (None, venue)
        except Exception:
            continue
    return (None, venue)

# ------------------------------- schedule → team_game_number (NEW) -------------------------------
def build_team_game_number_map(start_iso: str, end_iso: str, team_id: int = MARINERS_TEAM_ID) -> Dict[int, int]:
    """
    Query MLB StatsAPI schedule for the given team/date range and return {gamePk: team_game_number},
    where team_game_number is 1..N in chronological order (doubleheaders handled by gameDate then gamePk).
    """
    url = SCHEDULE_URL.format(team_id=team_id, start=start_iso, end=end_iso)
    try:
        r = requests.get(url, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        data = r.json()
    except Exception:
        return {}

    games = []
    for date_blk in data.get("dates", []):
        for g in date_blk.get("games", []):
            try:
                game_pk = int(g.get("gamePk"))
                game_date = g.get("gameDate")  # ISO timestamp
                games.append((game_date, game_pk))
            except Exception:
                continue

    # sort by timestamp, then by gamePk for stability (doubleheaders)
    games.sort(key=lambda t: (t[0] or "", t[1]))
    mapping = {}
    n = 0
    for _, gpk in games:
        n += 1
        mapping[gpk] = n
    return mapping

# ------------------------------- data ops -----------------------------------
NEEDED_COLS: List[str] = [
    "game_date", "game_pk", "at_bat_number", "events", "hit_distance_sc",
    "player_name", "venue_name", "home_team", "away_team", "inning_topbot"
]

def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in NEEDED_COLS:
        if col not in df.columns:
            df[col] = pd.NA
    if "game_pk" in df.columns:
        df["game_pk"] = pd.to_numeric(df["game_pk"], errors="coerce").astype("Int64")
    if "at_bat_number" in df.columns:
        df["at_bat_number"] = pd.to_numeric(df["at_bat_number"], errors="coerce").astype("Int64")
    if "player_name" in df.columns:
        df["player_name"] = df["player_name"].fillna("Cal Raleigh")
    return df

def fetch_statcast(start: str, end: str) -> pd.DataFrame:
    if not HAVE_PYBASEBALL:
        raise RuntimeError("pybaseball not installed; pass --input or install pybaseball>=2.2")
    df = statcast_batter(start_dt=start, end_dt=end, player_id=CAL_RALEIGH_MLBAM_ID)
    return df

def filter_home_runs(df: pd.DataFrame) -> pd.DataFrame:
    ev = df.get("events")
    mask = (ev == "home_run") | (ev.astype(str).str.lower() == "home_run")
    return df.loc[mask].copy()

def backfill_distances_and_venue(hr_df: pd.DataFrame) -> pd.DataFrame:
    """Create distance_ft from hit_distance_sc; backfill via feed/live; fill venue_name."""
    hr_df["distance_ft"] = pd.to_numeric(hr_df.get("hit_distance_sc"), errors="coerce")
    cache = load_cache()

    if "venue_name" not in hr_df.columns:
        hr_df["venue_name"] = pd.NA

    unique_games = sorted([int(g) for g in hr_df["game_pk"].dropna().unique().tolist()])
    feeds: Dict[int, Dict[str, Any]] = {}
    for g in unique_games:
        data = get_feed_live(g, cache)
        if data:
            feeds[g] = data

    for idx, row in hr_df.iterrows():
        g = row.get("game_pk")
        ab = row.get("at_bat_number")
        feed = feeds.get(int(g)) if pd.notna(g) and int(g) in feeds else None

        # Enrich venue whenever missing and feed is available
        if pd.isna(row.get("venue_name")) and feed:
            _, venue = extract_total_distance_and_venue(feed, int(ab) if pd.notna(ab) else -1)
            if venue:
                hr_df.at[idx, "venue_name"] = venue

        # Distance backfill
        if pd.isna(row["distance_ft"]) and feed and pd.notna(ab):
            td, _ = extract_total_distance_and_venue(feed, int(ab))
            if td is not None:
                hr_df.at[idx, "distance_ft"] = float(td)

    return hr_df

# include team_game_number + (keep your existing columns)
KEEP_COLS: List[str] = [
    "game_date","game_pk","team_game_number","at_bat_number","player_name","events",
    "hit_distance_sc","distance_ft","venue_name",
    "launch_speed","launch_angle","pitch_type","release_speed",
    "home_team","away_team","inning","inning_topbot"
]

def tidy(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in KEEP_COLS if c in df.columns]
    out = df[cols].copy()
    if "game_date" in out.columns:
        out["game_date"] = pd.to_datetime(out["game_date"], errors="coerce").dt.date
        out = out.sort_values(["game_date","game_pk","at_bat_number"]).reset_index(drop=True)
    return out

def to_json_records(df: pd.DataFrame) -> List[Dict[str, Any]]:
    recs = df.to_dict(orient="records")
    # Ensure date is ISO string
    for r in recs:
        gd = r.get("game_date")
        if hasattr(gd, "isoformat"):
            r["game_date"] = gd.isoformat()
        elif gd is not None:
            r["game_date"] = str(gd)
    return recs

# ----------------------------------- main -----------------------------------
def main():
    # Load input or fetch
    if args.input:
        df = pd.read_csv(args.input)
    else:
        if not HAVE_PYBASEBALL:
            raise SystemExit("pybaseball not installed and no --input provided.")
        df = fetch_statcast(args.start, args.end)

    df = ensure_columns(df)
    hr = filter_home_runs(df)

    if hr.empty:
        pd.DataFrame(columns=KEEP_COLS).to_csv(args.out_csv, index=False)
        Path(args.out_json).write_text("[]", encoding="utf-8")
        print(f"Wrote empty files: {args.out_csv}, {args.out_json} — HR rows: 0")
        return

    # Backfill distance + venue as before
    hr = backfill_distances_and_venue(hr)

    # NEW: add team_game_number via schedule API (gamePk → 1..N for Mariners)
    game_no_map = build_team_game_number_map(args.start, args.end, MARINERS_TEAM_ID)
    if game_no_map:
        # map by game_pk; if not found, leave NA (e.g., preseason or postponed)
        hr["team_game_number"] = hr["game_pk"].map(lambda x: game_no_map.get(int(x)) if pd.notna(x) else pd.NA)
    else:
        hr["team_game_number"] = pd.NA  # graceful fallback

    out = tidy(hr)

    # Write CSV + JSON
    out.to_csv(args.out_csv, index=False)
    recs = to_json_records(out)
    Path(args.out_json).write_text(json.dumps(recs, ensure_ascii=False, indent=2), encoding="utf-8")

    total = len(out)
    have_dist = out["distance_ft"].notna().sum() if "distance_ft" in out.columns else 0
    have_venue = out["venue_name"].notna().sum() if "venue_name" in out.columns else 0
    have_gnum  = out["team_game_number"].notna().sum() if "team_game_number" in out.columns else 0

    print(
        f"Wrote: {args.out_csv}, {args.out_json} — "
        f"HR rows: {total} | with distance_ft: {have_dist} | missing dist: {total - have_dist} | "
        f"venue filled: {have_venue} | team_game_number set: {have_gnum}"
    )

if __name__ == "__main__":
    main()
