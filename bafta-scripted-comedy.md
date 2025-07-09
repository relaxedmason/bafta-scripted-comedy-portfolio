---
layout: default
title: "BAFTA Scripted Comedy Awards: Winners & Nominees"
permalink: /bafta-scripted-comedy/
---

# BAFTA Scripted Comedy Awards  
## Winners & Nominees (2016–2025)

---

## 1. Business Question  
**Which scripted comedies have dominated the BAFTAs over the last decade?**  
- Did the highest-rated IMDb show win each year?  
- Which series beat *Peep Show*, a seven-time nominee?

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
), nominees AS (
  …
)
SELECT *
  FROM nom_with_meta
 ORDER BY awardyear DESC;
<!-- responsive montage just beneath the SQL, before the license --> <picture> <!-- Mobile (<600px) --> <source media="(max-width: 600px)" srcset="{{ '/assets/images/bafta_mobile_scripted_comedy_winners_final.jpg' | relative_url }}"> <!-- Desktop (601px+) --> <source media="(min-width: 601px)" srcset="{{ '/assets/images/bafta_scripted_comedy_visualization.png' | relative_url }}"> <!-- Fallback --> <img src="{{ '/assets/images/bafta_scripted_comedy_visualization.png' | relative_url }}" alt="BAFTA Scripted Comedy Awards montage (2016–2025)" style="max-width:100%; height:auto;" /> </picture>
License
Code & write-up: MIT
Data & images: IMDb © IMDb · TMDb API (posters) · Wikipedia CC BY-SA
