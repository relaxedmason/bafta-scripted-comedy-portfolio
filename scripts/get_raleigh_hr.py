# scripts/get_raleigh_hr.py
from datetime import date
from pathlib import Path
import pandas as pd

from pybaseball import playerid_lookup, statcast_batter
import requests

OUT_DIR = Path("assets/data")
OUT_JSON = OUT_DIR / "raleigh_hr.json"
OUT_CSV  = OUT_DIR / "raleigh_hr.csv"

def season_start(today: date) -> date:
    return date(today.year, 3, 1) if today.month >= 3 else date(today.year, 1, 1)

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

    today = date.today()
    start = season_start(today)

    try:
        pid = playerid_lookup('Raleigh', 'Cal')["key_mlbam"].iloc[0]
    except Exception as e:
        print("Failed to look up Cal Raleigh ID:", e)
        df = tidy_empty_df()
        df.to_json(OUT_JSON, orient="records", date_format="iso")
        df.to_csv(OUT_CSV, index=False)
        return

    try:
        raw = statcast_batter(start, today, pid)
    except Exception as e:
        print("Statcast call failed:", e)
        raw = None

    if raw is None or raw.empty:
        df = tidy_empty_df()
    else:
        hr = raw[raw["events"] == "home_run"].copy()
        if hr.empty:
            df = tidy_empty_df()
        else:
            hr["game_date"] = pd.to_datetime(hr["game_date"]).dt.date
            hr["home"] = (hr["home_team"] == hr["team"]).fillna(False)

            cache = {}
            try:
                hr["venue_name"] = hr["game_pk"].apply(lambda pk: venue_name(int(pk), cache))
            except Exception as e:
                print("Venue lookup failed:", e)
                hr["venue_name"] = ""

            keep = [
                "game_date","venue_name","home","home_team","away_team",
                "launch_speed","launch_angle","hit_distance_sc",
                "hc_x","hc_y","pitch_type","release_speed","p_throws",
                "player_name","pitcher","game_pk"
            ]
            df = hr.reindex(columns=keep).sort_values("game_date", ascending=False)

    df.to_json(OUT_JSON, orient="records", date_format="iso")
    df.to_csv(OUT_CSV, index=False)
    print(f"Wrote {len(df)} rows to {OUT_JSON} and {OUT_CSV}")

if __name__ == "__main__":
    main()

