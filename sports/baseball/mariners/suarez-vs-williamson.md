---
layout: default
title: Suárez vs. Williamson — 2025 First Half Comparison
permalink: /sports/baseball/mariners/suarez-vs-williamson/
description: Side-by-side visualization comparing Eugenio Suárez’s 2025 performance with the Diamondbacks vs. Ben Williamson, around the Mariners’ 2025 trade-deadline acquisition.
---

## Comparing Geno Suárez’s First Half to Williamson’s Rookie Season

Seattle acquired **Eugenio Suárez** at the **2025 MLB trade deadline** for three minor league prospects, first baseman Tyler Locklear and right-handers Juan Burgos and Hunter Cranton. This visualization compares Suárez’s first half production with the man he is replacing at the hot corner, rookie **Ben Williamson**.

To provide a balanced snapshot of each player’s performance, this page uses **wRC+**, **BsR**, **DRS**, and **Baseball Savant percentile rankings**. Together these metrics cover offensive value, baserunning, defense, and underlying skill indicators—giving a concise view of each player’s strengths and weaknesses.

<!-- Image (responsive, with mobile asset) -->
<div id="vizContainer" style="text-align:center; margin-top:18px;">
  <picture>
    <source media="(max-width: 640px)" srcset="/assets/images/sports/mariners/suarez_williamson_mobile.png">
    <img
      id="vizImage"
      src="/assets/images/sports/mariners/suarez_williamson_desktop.png"
      alt="Eugenio Suárez (Diamondbacks) vs Ben Williamson comparison, 2025"
      style="max-width:100%; height:auto; border:1px solid #ccc; box-shadow:2px 2px 6px rgba(0,0,0,.15); cursor:pointer"
      onclick="openModal(this.src)"
    />
  </picture>

  <!-- Caption -->
  <p style="font-size:.95em; color:#555; margin-top:10px;">
    Ranks shown #1–#15 (red = top 5, blue = bottom 5). Footnotes indicate league context.
  </p>

  <!-- Quick actions -->
  <div style="margin-top:8px;">
    <a href="/assets/images/sports/mariners/suarez_williamson_desktop.png" download
       style="display:inline-block; padding:8px 12px; border:1px solid #ccc; border-radius:10px; text-decoration:none; margin:0 6px;">
      ⬇️ Download PNG
    </a>
    <button onclick="openModal(document.getElementById('vizImage').src)"
            style="padding:8px 12px; border:1px solid #ccc; border-radius:10px; background:#fff; cursor:pointer; margin:0 6px;">
      🔍 View Large
    </button>
    <a href="/sports/baseball/bavasi/depth-chart/"
       style="display:inline-block; padding:8px 12px; border:1px solid #ccc; border-radius:10px; text-decoration:none; margin:0 6px;">
      ⟵ Back to Depth Charts
    </a>
  </div>
</div>

<!-- Conclusion (placed immediately after the visualization) -->
<div style="max-width:860px; margin:14px auto 0; font-size:1rem; line-height:1.55;">
  <p style="margin:.4rem 0;">
    <strong>Takeaway:</strong> While both are starting-caliber third basemen, their profiles are almost polar opposites —
    <strong>Williamson</strong> grades out as one of the <em>best fielders</em> in the league, whereas <strong>Suárez</strong> ranks among the league’s
    <em>best hitters</em>. <span style="color:#666;">(Or, put simply: <em>Williamson wins with the glove; Suárez wins with the bat.</em>)</span>
  </p>
</div>

<!-- Notes -->
<div style="max-width:860px; margin:18px auto 0; font-size:.95em; line-height:1.5;">
  <p style="margin:.4rem 0; color:#444;">
    *Trade note:* Suárez joined Seattle at the <strong>2025 trade deadline</strong>.
  </p>
  <p style="margin:.4rem 0; color:#666;">
    *Methodology:* 2025 season stats through the trade window. League ranks reflect the player’s primary league at the time of measurement
    (AL for Williamson, NL for Suárez before the trade). Formatting follows my standard: three-decimal AVG/OBP, BB%/K% with one decimal, and counting stats without decimals.
  </p>
</div>

<!-- Modal -->
<div id="imgModal" onclick="this.style.display='none'"
     style="display:none; position:fixed; inset:0; background:rgba(0,0,0,.85); z-index:9999; align-items:center; justify-content:center;">
  <img id="modalImg" style="max-width:92%; max-height:92%; border-radius:8px;" />
</div>

<script>
  function openModal(src){
    const m = document.getElementById('imgModal');
    const i = document.getElementById('modalImg');
    i.src = src;
    m.style.display = 'flex';
  }
</script>

<style>
  @media (max-width: 640px) {
    #vizContainer a, #vizContainer button {
      font-size: 14px;
      padding: 8px 10px;
      margin: 4px 4px;
    }
  }
</style>

