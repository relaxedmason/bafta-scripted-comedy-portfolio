---
layout: page
title: "Venezuelan WAR — Mariners Focus"
permalink: /sports/baseball/mariners/venezuelan-war/
---

<div style="text-align:center">

## Seattle’s Legacy of Venezuelan Talent

</div>

Baseball has deep roots in Venezuela, producing a remarkable number of elite players who have left their mark on the United States’ national pastime. From Hall of Famers to modern stars, Venezuelan-born players have consistently delivered impact across every facet of Major League Baseball, cementing the country as one of the league’s most vital international pipelines for talent.

The Seattle Mariners have historically leaned into this connection. They invested early in international scouting and development, including establishing academy operations in Venezuela to identify and nurture young prospects. That pipeline has brought in impactful players over the years, strengthening the club’s roster and leaving a lasting mark on the franchise’s identity. While political and logistical challenges have changed how teams operate academies in Venezuela, the Mariners’ legacy of recruiting Venezuelan talent remains an important part of their history.

---

<!-- ===== Page-local styles: keep centered H2s, clamp image width ===== -->
<style>
  /* clamp each visualization container (images will fill this box) */
  .viz-block{
    width:100%;
    max-width:720px;   /* adjust to taste */
    margin:2rem auto;  /* centers the viz within your page */
  }
  /* optional presets if you want different widths per viz */
  .viz-sm{ max-width:560px; }
  .viz-md{ max-width:720px; }
  .viz-lg{ max-width:840px; }

  .viz-img{width:100%;height:auto;border-radius:12px}
  .zoomable{cursor:zoom-in}
</style>

<!-- ===== Theme-aware images (no button) + Lightbox ===== -->
<script>
document.addEventListener('DOMContentLoaded', () => {
  // Swap images based on the site's current theme (set on <html data-theme="...">)
  const imgs = document.querySelectorAll('img[data-src-light][data-src-dark]');
  function applyThemeToImages(){
    const theme = document.documentElement.getAttribute('data-theme') || 'light';
    imgs.forEach(img => {
      img.src = (theme === 'dark') ? img.dataset.srcDark : img.dataset.srcLight;
    });
  }
  applyThemeToImages();

  // If your global theme toggler changes data-theme, update images live
  const obs = new MutationObserver(applyThemeToImages);
  obs.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  // --- Lightbox (click to enlarge) ---
  const overlay = document.createElement('div');
  overlay.id = 'lightbox';
  overlay.style.cssText = 'display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:9999;align-items:center;justify-content:center;padding:2rem';
  overlay.innerHTML = '<img id="lightboxImg" alt="" style="max-width:95%;max-height:95%;box-shadow:0 10px 30px rgba(0,0,0,.5);border-radius:12px;cursor:zoom-out">';
  document.body.appendChild(overlay);
  overlay.addEventListener('click', () => overlay.style.display = 'none');

  document.addEventListener('click', e => {
    const target = e.target.closest('img.zoomable');
    if (!target) return;
    document.getElementById('lightboxImg').src = target.src;
    overlay.style.display = 'flex';
  });
});
</script>

<div style="text-align:center">

## Franchises powered by Venezuelan talent

</div>

<div class="viz-block viz-md">
  <img
    class="viz-img zoomable"
    src="{{ '/assets/images/sports/mariners/top_10_MLB_Team_WAR_Venezuela_light.png' | relative_url }}"
    data-src-light="{{ '/assets/images/sports/mariners/top_10_MLB_Team_WAR_Venezuela_light.png' | relative_url }}"
    data-src-dark="{{ '/assets/images/sports/mariners/top_10_MLB_Team_WAR_Venezuela_dark.png' | relative_url }}"
    alt="Top 10 MLB team WAR by Venezuelan-born players with Mariners highlighted">
</div>

---

<div style="text-align:center">

## Mariners legends from Venezuela

</div>

<div class="viz-block viz-md">
  <img
    class="viz-img zoomable"
    src="{{ '/assets/images/sports/mariners/top_10_MLB_Team_WAR_Venezuelans_Map_light.png' | relative_url }}"
    data-src-light="{{ '/assets/images/sports/mariners/top_10_MLB_Team_WAR_Venezuelans_Map_light.png' | relative_url }}"
    data-src-dark="{{ '/assets/images/sports/mariners/top_10_MLB_Team_WAR_Venezuelans_Map_dark.png' | relative_url }}"
    alt="Top 5 Mariners of Venezuelan birth (all-time), mapped">
</div>
