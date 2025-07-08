---
layout: home
title: "BAFTA Scripted Comedy Awards: Winners & Nominees"
---

# BAFTA Scripted Comedy Awards: Winners & Nominees (2016–2025)

![Main montage]({{ "/assets/images/bafta_scripted_comedy_visualization.png" | relative_url }}){: style="max-width:100%;height:auto;" }


---

## 🖼️ Preview

<picture>
  <!-- mobile for viewports up to 600px -->
  <source media="(max-width: 600px)" srcset="{{ '/assets/images/bafta_mobile_final.jpg' | relative_url }}">
  <!-- HD for anything larger -->
  <source media="(min-width: 601px)" srcset="{{ '/assets/images/bafta_scripted_two_row_montage_hires.png' | relative_url }}">
  <!-- fallback -->
  <img 
    src="{{ '/assets/images/bafta_scripted_two_row_montage_hires.png' | relative_url }}"
    alt="BAFTA Scripted Comedy Awards Montage"
    style="max-width:100%; height:auto;" 
  />
</picture>

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
  …
)
SELECT *
FROM nom_with_meta
ORDER BY awardyear DESC;
```         

> **Full SQL** → [scripts/last_10_Bafta_scripted_comedy_winner.sql](scripts/last_10_Bafta_scripted_comedy_winner.sql)
---

## License

**Code & write-up:** [MIT](LICENSE)

**Data & images:**  
- IMDb data © IMDb  
- TMDb API (posters) terms apply  
- Wikipedia content under CC BY-SA  



