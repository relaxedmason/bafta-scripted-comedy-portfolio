# scripts/get_raleigh_hr.py
from datetime import date
from pathlib import Path
import pandas as pd
import requests

from pybaseball import playerid_lookup, statcast_batter

OUT_JSON = Path("assets/data/raleigh_hr.json")
OUT_CSV  = Path("assets/data/raleigh_hr.csv")

def season_start(today: date) -> date:
    # If it's preseason, start Jan 1; otherwise Mar 1 is plenty for Statcast season
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

def main():
    today = date.today()
    start = season_start(today)

    # Cal Raleigh MLBAM id (looked up dynamically for safety)
    pid = playerid_lookup('Raleigh', 'Cal')["key_mlbam"].iloc[0]

    df = statcast_batter(start, today, pid)
    if df is None or df.empty:
        hr = pd.DataFrame(columns=[
            "game_date","venue_name","home","home_team","away_team",
            "launch_speed","launch_angle","hit_distance_sc",
            "hc_x","hc_y","pitch_type","release_speed","p_throws",
            "player_name","pitcher","game_pk"
        ])
    else:
        hr = df[df["events"] == "home_run"].copy()
        if hr.empty:
            hr = pd.DataFrame(columns=[
                "game_date","venue_name","home","home_team","away_team",
                "launch_speed","launch_angle","hit_distance_sc",
                "hc_x","hc_y","pitch_type","release_speed","p_throws",
                "player_name","pitcher","game_pk"
            ])
        else:
            hr["game_date"] = pd.to_datetime(hr["game_date"]).dt.date
            hr["home"] = (hr["home_team"] == hr["team"]).fillna(False)

            # Venue lookup (park-aware)
            cache = {}
            hr["venue_name"] = hr["game_pk"].apply(lambda pk: venue_name(int(pk), cache))

            keep = [
                "game_date","venue_name","home","home_team","away_team",
                "launch_speed","launch_angle","hit_distance_sc",
                "hc_x","hc_y","pitch_type","release_speed","p_throws",
                "player_name","pitcher","game_pk"
            ]
            hr = hr.reindex(columns=keep).sort_values("game_date", ascending=False)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    hr.to_json(OUT_JSON, orient="records", date_format="iso")
    hr.to_csv(OUT_CSV, index=False)
    print(f"Wrote {len(hr)} rows → {OUT_JSON.name}, {OUT_CSV.name}")

if __name__ == "__main__":
    main()
