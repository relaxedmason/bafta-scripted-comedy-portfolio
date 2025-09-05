# scripts/get_raleigh_hr.py
from datetime import date, datetime
from pathlib import Path
import os
import pandas as pd
import requests
from pybaseball import playerid_lookup, statcast_batter

OUT_DIR = Path("assets/data")
OUT_JSON = OUT_DIR / "raleigh_hr.json"
OUT_CSV  = OUT_DIR / "raleigh_hr.csv"

def current_season_range(today: date):
    """Regular season window: Mar 27 → Nov 30 (this year)."""
    start = date(today.year, 3, 27)  # Opening Day
    end   = min(today, date(today.year, 11, 30))
    return start, end

def get_range():
    """Use START_DATE/END_DATE (YYYY-MM-DD) if set; otherwise current season. Return ISO strings."""
    today = date.today()
    default_start, default_end = current_season_range(today)
    sd = os.getenv("START_DATE", "")
    ed = os.getenv("END_DATE", "")
    try:
        start = datetime.strptime(sd, "%Y-%m-%d").date() if sd else default_start
    except Exception:
        start = default_start
    try:
        end = datetime.strptime(ed, "%Y-%m-%d").date() if ed else default_end
    except Exception:
        end = default_end
    return start.isoformat(), end.isoformat()

def venue_name(game_pk: int, cache: dict) -> str:
    if game_pk in cache:
        return cache[game_pk]
    url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    name = r.json()["gameData"]["venue"]["name"]
    cache[game_pk] = name
    return name

def tidy_empty_df():
    cols = [
        "game_date","venue_name","home","home_team","away_team",
        "launch_speed","launch_angle","hit_distance_sc",
        "hc_x","hc_y","pitch_type","release_speed","p_throws",
        "player_name","pitcher","game_pk"
    ]
    return pd.DataFrame(columns=cols)

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    start_str, end_str = get_range()
    print(f"[info] Querying Statcast for Cal Raleigh from {start_str} to {end_str}")

    try:
        pid = int(playerid_lookup('Raleigh', 'Cal')["key_mlbam"].iloc[0])
        print(f"[info] MLBAM id = {pid}")
    except Exception as e:
        print("[error] Failed to look up Cal Raleigh ID:", e)
        df = tidy_empty_df()
        df.to_json(OUT_JSON, orient="records", date_format="iso")
        df.to_csv(OUT_CSV, index=False)
        return

    try:
        raw = statcast_batter(start_str, end_str, pid)
    except Exception as e:
        print("[error] Statcast call failed:", e)
        raw = None

    if raw is None or raw.empty:
        print("[warn] No Statcast data returned")
        df = tidy_empty_df()
    else:
        print(f"[info] Statcast rows: {len(raw)}")
        ev_col = "events"
        hr = raw[raw[ev_col].astype(str).str.lower().eq("home_run")] if ev_col in raw.columns else raw.copy()
        print(f"[info] Home run rows after filter: {len(hr)}")

        if hr.empty:
            df = tidy_empty_df()
        else:
            # Regular-season only
            opening_day = datetime.strptime(start_str, "%Y-%m-%d").date()
            if "game_type" in hr.columns:
                before = len(hr)
                hr = hr[hr["game_type"].astype(str).str.upper().eq("R")].copy()
                print(f"[info] Filtered to regular season via game_type: {before} -> {len(hr)} rows")
            else:
                before = len(hr)
                hr["game_date"] = pd.to_datetime(hr.get("game_date"), errors="coerce").dt.date
                hr = hr[hr["game_date"] >= opening_day].copy()
                print(f"[info] Filtered to dates >= {opening_day}: {before} -> {len(hr)} rows")

            # Normalize types / columns
            hr["game_date"] = pd.to_datetime(hr.get("game_date"), errors="coerce").dt.date

            if "bat_team" in hr.columns:
                hr["home"] = (hr["home_team"] == hr["bat_team"]).fillna(False)
                print("[info] Computed 'home' using 'bat_team' vs 'home_team'")
            elif "team" in hr.columns:
                hr["home"] = (hr["home_team"] == hr["team"]).fillna(False)
                print("[info] Computed 'home' using 'team' vs 'home_team'")
            else:
                hr["home"] = False
                print("[warn] Neither 'bat_team' nor 'team' present; defaulting 'home' to False")

            cache = {}
            try:
                hr["venue_name"] = hr["game_pk"].apply(lambda pk: venue_name(int(pk), cache))
            except Exception as e:
                print("[warn] Venue lookup failed (continuing):", e)
                hr["venue_name"] = ""

            keep = [
                "game_date","venue_name","home","home_team","away_team",
                "launch_speed","launch_angle","hit_distance_sc",
                "hc_x","hc_y","pitch_type","release_speed","p_throws",
                "player_name","pitcher","game_pk"
            ]
            for c in keep:
                if c not in hr.columns:
                    hr[c] = pd.NA
            df = hr[keep].sort_values("game_date", ascending=False)

    df.to_json(OUT_JSON, orient="records", date_format="iso")
    df.to_csv(OUT_CSV, index=False)
    print(f"[done] Wrote {len(df)} rows -> {OUT_JSON} and {OUT_CSV}")

if __name__ == "__main__":
    main()
