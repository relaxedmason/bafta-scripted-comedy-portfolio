---
layout: default
title: Statcast-Era Home Run Rankings
permalink: /sports/top-10-home-runs-at-Safeco-Field/
---

# Statcast-Era Home Run Rankings

_At T-Mobile Park (Safeco Field), 2015 – present_

<div style="text-align:center; margin:2rem 0;">
  <img
    src="{{ '/assets/images/sports/mariners/Top_10_Home_Runs_Safeco.png' | relative_url }}"
    alt="Top 10 Longest Home Runs at T-Mobile Park"
    style="max-width:90%; height:auto; border:1px solid #ddd;"
  >
</div>

## Data & Methodology

- **Source:** MLB Statcast via Python `pybaseball`  
- **Filter:** `events == "home_run"` & `home_team == "SEA"`  
- **Metrics:** distance & exit velocity  

<div style="text-align:center; margin:2rem 0;">
  <a href="{{ '/notebooks/top10_home_runs.ipynb' | relative_url }}" class="btn btn-primary">📓 View the Notebook</a>
</div>

<a href="{{ '/' | relative_url }}" class="back-link">← Back to home</a>

