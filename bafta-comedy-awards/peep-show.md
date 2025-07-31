---
layout: default
title: "Peep Show at the BAFTAs"
permalink: /bafta-comedy-awards/peep-show/
---

# Peep Show at the BAFTAs: 7 Nominations, 1 Win

*Data sources: IMDb non-commercial datasets (self-built), TMDb API, Wikipedia.*  
*Visualization built in Python using poster art; SQL used to pull award/nominee history.*  
*@relaxedmason*

---

## 1. Business Question  
How did *Peep Show* perform at the BAFTA TV Awards for Best Scripted Comedy over time, and in years it was nominated, did it win? Which years did it lose, and to whom?

---

## 2. Data & Plumbing

### a) Data Collection  
I built an internal IMDb title database from IMDb’s non-commercial title datasets, then enriched that with BAFTA Scripted Comedy Awards data scraped from Wikipedia. Poster art and additional metadata were pulled via the TMDb API. All of this was combined to get a full picture of nominees, winners, and their context.

### b) Peep Show vs Winners (SQL)  
This query pulls each year *Peep Show* was nominated, whether it won, and who the eventual winner was.  

<details>
<summary>View excerpt of the SQL</summary>

```sql
WITH peep_show_nominations AS (
  SELECT
    awardyear,
    imdbtitle AS peep_title,
    tconst AS peep_tconst,
    bafta_status AS peep_status
  FROM bafta_comedy_awards
  WHERE imdbtitle = 'Peep Show'
    AND awardtitle = 'Best Scripted Comedy'
),
yearly_winners AS (
  SELECT
    awardyear,
    imdbtitle AS winning_title,
    tconst AS winner_tconst
  FROM bafta_comedy_awards
  WHERE bafta_status = 'winner'
    AND awardtitle = 'Best Scripted Comedy'
)
SELECT 
  n.awardyear,
  n.peep_title,
  n.peep_tconst,
  n.peep_status,
  CASE 
    WHEN n.peep_status = 'winner' THEN '✅ Yes'
    ELSE '❌ No'
  END AS bafta_winner,
  w.winning_title,
  w.winner_tconst
FROM peep_show_nominations n
JOIN yearly_winners w ON n.awardyear = w.awardyear
ORDER BY n.awardyear;
</details>
[Download the full SQL script]({{ "/assets/Peep_show_versus_field_baftas.sql" | relative_url }})

3. Visualization (clickable to open full-size)
[![Peep Show montage showing nomination years and single win]({{ "/assets/images/peep_show_bafta_thumbnail.jpg" | relative_url }}){: style="max-width:100%; height:auto;" alt="Montage of Peep Show BAFTA nomination years with the winning year highlighted" }]
({{ "/assets/images/peep_show_bafta_fullres.jpg" | relative_url }}){: target="_blank" rel="noopener" }

4. Takeaways
Peep Show earned seven BAFTA nominations for Best Scripted Comedy but only one win, a pattern that underscores both its consistent quality and the stiff competition. In its losing years, the trophy went to shows like The Office (UK), The IT Crowd, Rev., and Peter Kay’s Car Share—all well-regarded—but it was only outscored in IMDb rating when it lost to The Thick of It (twice). In 5 of the 7 nomination years, Peep Show actually had a higher IMDb rating than the eventual winner, highlighting how narrowly contested the category was.

License & Credits
Code & write-up: [MIT]({{ "/LICENSE" | relative_url }})
Data sources: IMDb (self-built database from non-commercial datasets), TMDb API (poster art and metadata), Wikipedia (award history) — Wikipedia content under CC BY-SA.
Visualization: Python (Pillow / matplotlib) with poster imagery from TMDb.
