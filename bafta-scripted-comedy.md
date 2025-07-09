---
layout: default
title: "BAFTA Scripted Comedy Awards"
permalink: /bafta-scripted-comedy/
---

# BAFTA Scripted Comedy Awards: Winners & Nominees (2016–2025)

---

## 1. Business Question  
**Which scripted comedies have dominated the BAFTAs over the last decade?**  

---

## 2. Data & Plumbing

I built an end-to-end pipeline in Python, SQL and APIs to go from a Wikipedia page to the final poster montage:

1. **Scraping BAFTA data**  
   - Pulled the [“British Academy Television Award for Best Scripted Comedy” page](https://en.wikipedia.org/wiki/British_Academy_Television_Award_for_Best_Scripted_Comedy) with `requests` + `BeautifulSoup`.  
   - Parsed out year, show title and nominee vs. winner tags.  
   - Saved the raw table to CSV for sanity checks.

2. **IMDB ID matching & database ingestion**  
   - Loaded that CSV into a staging table in my local IMDb SQL Server.  
   - Used a small Python script (`pandas` + `fuzzywuzzy`) to match show titles to IMDb `tconst` IDs.  
   - Populated a `bafta_comedy_awards` table with `awardyear`, `bafta_status` and `tconst`.

3. **Metadata enrichment via TMDb**  
   - For each `tconst`, called TMDb’s “find” endpoint to get the `poster_path`.  
   - Downloaded the “original”-size poster images from TMDb’s CDN.  
   - Cached metadata (title, dimensions, poster URL) in a JSON file.

4. **Visualization**  
   - Wrote a Python script using **Pillow** (and **matplotlib**) to layout a two-row montage: winners large on left, nominees stacked to the right.  
   - Overlaid each poster with a hollow “year” label, keeping text legible and titles uncut.  
   - Produced both a high-resolution PNG and a mobile-optimized JPEG.

> **Full SQL** → [scripts/last_10_Bafta_scripted_comedy_winner.sql]({{ "/scripts/last_10_Bafta_scripted_comedy_winner.sql" | relative_url }})  


## 3. Visualization

![BAFTA Scripted Comedy Awards Montage]({{ "/assets/images/bafta_scripted_comedy_visualization.png" | relative_url }}){: style="max-width:100%; height:auto;" }

---

## License

**Code & write-up:** [MIT]({{ "/LICENSE" | relative_url }})  
**Data & images:**  
- IMDb data © IMDb  
- Posters via TMDb API (terms apply)  
- Wikipedia content under CC BY-SA  

