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

### a) SQL  
Pull the last ten award cycles of nominees vs winners, enriched with IMDb metadata:

```sql
WITH last10 AS (
  SELECT DISTINCT awardyear
  FROM bafta_comedy_awards
  WHERE awardtitle = 'Best Scripted Comedy'
    AND bafta_status = 'winner'
  ORDER BY awardyear DESC
  OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY
),
nominees AS (
  SELECT
    b.awardyear,
    b.bafta_status,
    b.tconst
  FROM bafta_comedy_awards b
  JOIN last10 l
    ON b.awardyear = l.awardyear
  WHERE b.awardtitle = 'Best Scripted Comedy'
)
SELECT *
FROM nom_with_meta
ORDER BY awardyear DESC;
Full SQL → [scripts/last_10_Bafta_scripted_comedy_winner.sql]({{ "/scripts/last_10_Bafta_scripted_comedy_winner.sql" | relative_url }})

3. Visualization
![BAFTA Scripted Comedy Awards Montage]({{ "/assets/images/bafta_scripted_comedy_visualization.png" | relative_url }}){: style="max-width:100%; height:auto;" }

License
Code & write-up: [MIT]({{ "/LICENSE" | relative_url }})
Data & images:

IMDb data © IMDb

Posters via TMDb API (TMDb terms apply)

Wikipedia content under CC BY-SA
