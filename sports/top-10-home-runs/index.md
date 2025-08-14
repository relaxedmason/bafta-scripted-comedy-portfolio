---
layout: default
title: Statcast-Era Home Run Rankings
permalink: /sports/top-10-home-runs-at-Safeco-Field/
---

# Statcast-Era Home Run Rankings

_At T-Mobile Park (Safeco Field), 2015 – present_

<!-- Styles for the lightbox -->
<style>
  .hr-figure { max-width: min(100%, 1300px); margin: 2rem auto; text-align: center; }
  .hr-figure img {
    width: 100%; height: auto; border: 1px solid #ddd; border-radius: 12px;
    box-shadow: 0 6px 24px rgba(0,0,0,.15); cursor: zoom-in;
  }
  dialog.img-lightbox {
    width: 90vw; max-width: 1600px; border: none; padding: 0; background: transparent;
  }
  dialog.img-lightbox::backdrop { background: rgba(0,0,0,.6); }
  .img-lightbox img { width: 100%; height: auto; display: block; border-radius: 12px; cursor: zoom-out; }
</style>

<figure class="hr-figure">
  <img
    id="hrImage"
    src="{{ '/assets/images/sports/mariners/top_10_home_run_safeco_field.png' | relative_url }}"
    alt="Top 10 Longest Home Runs at T-Mobile Park (Statcast era)">
  <figcaption>Click/tap to zoom. Click outside (or the image) to close.</figcaption>
</figure>

<dialog id="imgModal" class="img-lightbox">
  <img src="{{ '/assets/images/sports/mariners/top_10_home_run_safeco_field.png' | relative_url }}" alt="">
</dialog>

<script>
  const img = document.getElementById('hrImage');
  const modal = document.getElementById('imgModal');
  img.addEventListener('click', () => modal.showModal());
  modal.addEventListener('click', () => modal.close());
</script>


## Data & Methodology

- **Source:** MLB Statcast via Python `pybaseball`  


<div style="text-align:center; margin:2rem 0;">
  <a href="{{ '/<a href="{{ '/assets/top_10_homeruns_safeco_field.ipynb' | relative_url }}" class="btn btn-primary">📓 View the Notebook</a>
' | relative_url }}" class="btn btn-primary">📓 View the Notebook</a>
</div>

<a href="{{ '/' | relative_url }}" class="back-link">← Back to home</a>

