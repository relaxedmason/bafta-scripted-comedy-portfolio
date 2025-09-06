#!/usr/bin/env python3
# get_raleigh_hr.py
#
# Build a complete Cal Raleigh HR dataset with reliable distances.
# - Pulls Statcast (or reads your CSV)
# - Filters to home runs
# - Backfills missing hit_distance_sc using MLB feed/live totalDistance
# - Writes a clean CSV with a fully-populated distance column
#
# Usage examples:
#   python get_raleigh_hr.py --out cal_raleigh_hr.csv
#   python get_raleigh_hr.py --input my_existing_hr_rows.csv --out cal_raleigh_hr_filled.csv
#   python get_raleigh_hr.py --start 2019-01-01 --end 2025-12-31 --out cal_raleigh_hr.csv
#
# Notes:
# - Requires: pandas, requests (optional: pybaseball if you fetch fresh statcast)
# - We match rows via (game_pk, at_bat_number) to the feed/live "allPlays[].about.atBatIndex".
# - totalDistance is returned in feet (string/number). We cast to float.
# - A small on-disk cache avoids re-hitting the API for the same game_pk multiple times.

import argparse
import json
import time
from pathlib import Path
from typing import Dict, Optional, Any

import pandas as pd
import requests

# --- If you want to fetch fresh Statcast, keep this import. Otherwise, provide --input.
try:
    from pybaseball import statcast_batter
    HAVE_PYBASEBALL = True
except Exception:
    HAVE_PYBASEBALL = False

CAL_RALEIGH_MLBAM_ID = 663728  # Cal Raleigh
FEED_LIVE_URL = "https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
CACHE_PATH = Path(".feed_live_cache.json")
REQUEST_TIMEOUT = 20
REQUEST_SLEEP = 0.25  # polite pacing between new game fetches


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
    key = str(game_pk)
    if key in cache:
        return cache[key]
    url = FEED_LIVE_URL.format(game_pk=game_pk)
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            cache[key] = data
            save_cache(cache)
            time.sleep(REQUEST_SLEEP)
            return data
    except Exception:
        return None
    return None


def extract_total_distance_from_feed(data: Dict[str, Any], at_bat_index: int) -> Optional[float]:
    """
    Look up the matching at-bat in allPlays using about.atBatIndex and return hitData.totalDistance (ft).
    """
    try:
        plays = data["liveData"]["plays"]["allPlays"]
    except (KeyError, TypeError):
        return None

    for play in plays:
        try:
            if int(play.get("about", {}).get("atBatIndex", -1)) != int(at_bat_index):
                continue
            # Ensure it's a HR play; sometimes multiple events exist in an AB
            event_type = play.get("result", {}).get("eventType", "")
            if event_type != "home_run":
                # some feeds mark the AB as HR but eventType might be "home_run" only on final event
                # continue scanning playEvents
                pass

            # Scan playEvents for a batted ball with hitData.totalDistance
            for ev in play.get("playEvents", []):
                hd = ev.get("hitData")
                if not hd:
                    continue
                td = hd.get("totalDistance")
                if td is None:
                    continue
                # totalDistance can be str or number
                try:
                    return float(td)
                except Exception:
                    # last resort: strip non-digits
                    s = "".join(ch for ch in str(td) if (ch.isdigit() or ch == "." or ch == "-"))
                    return float(s) if s else None
        except Exception:
            continue
    return None


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    needed = ["game_pk", "at_bat_number", "events", "hit_distance_sc", "player_name", "game_date"]
    for col in needed:
        if col not in df.columns:
            # create safe defaults
            if col == "player_name":
                df[col] = "Cal Raleigh"
            elif col == "events":
                df[col] = ""
            else:
                df[col] = pd.NA
    return df


def fetch_statcast_cal(start: str, end: str) -> pd.DataFrame:
    if not HAVE_PYBASEBALL:
        raise RuntimeError("pybaseball not installed. Provide --input or install pybaseball.")
    df = statcast_batter(start_dt=start, end_dt=end, player_id=CAL_RALEIGH_MLBAM_ID)
    # normalize types we rely on
    if "game_pk" in df.columns:
        df["game_pk"] = df["game_pk"].astype("Int64")
    if "at_bat_number" in df.columns:
        df["at_bat_number"] = df["at_bat_number"].astype("Int64")
    return df


def filter_home_runs(df: pd.DataFrame) -> pd.DataFrame:
    # Statcast uses events == 'home_run' for HR balls in play
    mask = (df.get("events", "") == "home_run")
    hr = df.loc[mask].copy()
    return hr


def backfill_distances(hr_df: pd.DataFrame) -> pd.DataFrame:
    """
    For rows where hit_distance_sc is NA, fetch from feed/live using (game_pk, at_bat_number).
    Writes a new column: distance_ft (float), which prefers hit_distance_sc then falls back to totalDistance.
    """
    hr_df = ensure_columns(hr_df)
    # base distance
    hr_df["distance_ft"] = pd.to_numeric(hr_df.get("hit_distance_sc"), errors="coerce")

    cache = load_cache()

    needs_backfill = hr_df[hr_df["distance_ft"].isna()].copy()
    if needs_backfill.empty:
        return hr_df

    # We’ll iterate unique (game_pk), fetch once, then map at_bat_number inside
    for game_pk in sorted(needs_backfill["game_pk"].dropna().unique().tolist()):
        try:
            data = get_feed_live(int(game_pk), cache)
            if not data:
                continue
        except Exception:
            continue

        # apply to all rows for this game
        rows = hr_df.index[hr_df["game_pk"] == game_pk].tolist()
        for idx in rows:
            if pd.notna(hr_df.at[idx, "distance_ft"]):
                continue
            ab = hr_df.at[idx, "at_bat_number"]
            if pd.isna(ab):
                continue
            td = extract_total_distance_from_feed(data, int(ab))
            if td is not None:
                hr_df.at[idx, "distance_ft"] = float(td)

    return hr_df


def tidy_output_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Keep a concise, analysis-friendly set. Add more as needed.
    keep = [
        "game_date",
        "game_pk",
        "at_bat_number",
        "player_name",
        "events",
        "description",
        "home_team",
        "away_team",
        "pitch_number",
        "pitch_type",
        "release_speed",
        "launch_speed",
        "launch_angle",
        "hc_x",
        "hc_y",
        "bb_type",
        "estimated_ba_using_speedangle",
        "estimated_woba_using_speedangle",
        "home_team_runs",
        "away_team_runs",
        "inning",
        "inning_topbot",
        "home_score",
        "away_score",
        "outs_when_up",
        "stand",
        "p_throws",
        "pitcher",
        "batter",
        "hit_distance_sc",   # original statcast (may be NaN)
        "distance_ft",       # filled value
        "events"
    ]
    cols = [c for c in keep if c in df.columns]
    out = df[cols].copy()
    # Sort by date just in case
    if "game_date" in out.columns:
        out["game_date"] = pd.to_datetime(out["game_date"], errors="coerce")
        out = out.sort_values(["game_date", "game_pk", "at_bat_number"]).reset_index(drop=True)
    return out


def main():
    ap = argparse.ArgumentParser(description="Cal Raleigh HRs with complete distances (Statcast + feed/live backfill).")
    ap.add_argument("--input", help="Path to an existing CSV with Statcast rows (optional). If omitted, pulls Statcast.")
    ap.add_argument("--out", required=True, help="Output CSV path")
    ap.add_argument("--start", default="2019-01-01", help="Start date (if fetching): YYYY-MM-DD")
    ap.add_argument("--end", default="2025-12-31", help="End date (if fetching): YYYY-MM-DD")
    args = ap.parse_args()

    if args.input:
        df = pd.read_csv(args.input)
    else:
        if not HAVE_PYBASEBALL:
            raise SystemExit("pybaseball not installed and no --input provided. Install pybaseball or pass --input.")
        df = fetch_statcast_cal(args.start, args.end)

    # Filter to HRs, then backfill
    hr_df = filter_home_runs(df)
    if hr_df.empty:
        print("No home runs found in the provided data range/input.")
        hr_df.to_csv(args.out, index=False)
        return

    hr_df = backfill_distances(hr_df)
    out = tidy_output_columns(hr_df)
    out.to_csv(args.out, index=False)

    # Quick summary
    total = len(out)
    filled = out["distance_ft"].notna().sum()
    print(f"Wrote {args.out} — HR rows: {total} | with distance_ft: {filled} | missing: {total - filled}")


if __name__ == "__main__":
    main()
