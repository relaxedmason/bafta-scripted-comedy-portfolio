---
layout: default
title: "The Top 5 Least Deserving Wins in BAFTA Scripted Comedy History"
permalink: /bafta-comedy-awards/rating-check/
---

## 📉 Top 5 Least Deserving Wins in BAFTA Scripted Comedy History

A data-driven look at the biggest rating gaps between BAFTA winners and their higher-rated nominees for “Best Scripted Comedy.”

<p align="center">
  <img src="/assets/images/bafta_top5.png" alt="Top 5 Least Deserving Wins" style="max-width: 100%; width: 800px; height: auto;">
</p>

🟥 *Red numbers indicate how much lower the winning show's IMDb rating was compared to the highest-rated nominee that year.*

---

### 📊 How This Was Calculated

- **Data Source:** IMDb + BAFTA awards history  
- **Criteria:** Shows with the largest negative rating difference between winner and top-rated nominee  
- **Tools Used:**
  - SQL Server (to query and join BAFTA + IMDb data)  
  - Python (`matplotlib`, `Pillow`, `requests`)  
  - [TMDb API](https://www.themoviedb.org/) for poster images  

---

### 🛠️ Reproduce This Visualization

You can view the full Python notebook here:  
👉 [bafta_top5.ipynb](https://github.com/your-username/your-repo/blob/main/assets/bafta_top5.ipynb)

> _(Replace `your-username/your-repo` with your actual repo path if you're publishing to GitHub Pages)_
