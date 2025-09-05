---
layout: default
title: Cal Raleigh Home Run Tracker
description: Auto-updating record of Cal Raleigh home runs with distance, EV, LA, and ballpark filter.
permalink: /sports/baseball/mariners/raleigh-home-run-tracker/
---


<h1>Cal Raleigh Home Run Tracker</h1>
<p class="subtitle">Auto-updating via GitHub Actions · Filter by ballpark · Download CSV</p>

<label for="venueFilter" class="sr-only">Filter by ballpark</label>
<select id="venueFilter" style="margin:0 0 1rem 0;">
  <option value="all">All ballparks</option>
</select>

<div style="margin: 0 0 1rem 0;">
  <a class="chip" href="{{ '/assets/data/raleigh_hr.csv' | relative_url }}" download>⬇️ Download CSV</a>
</div>

<canvas id="hrTimeline" width="900" height="360" aria-label="Home run distance over time"></canvas>

<h2 style="margin-top:1.25rem;">Home Runs (compact table)</h2>
<div class="table-wrap">
  <table id="hrTable" class="compact">
    <thead>
      <tr>
        <th>Date</th>
        <th>Opponent</th>
        <th>Venue</th>
        <th>Dist (ft)</th>
        <th>EV (mph)</th>
        <th>LA (°)</th>
        <th>Pitcher</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>
</div>
<button id="showMore" type="button" style="margin-top:.75rem;">Show more</button>

<!-- Chart.js + date adapter -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@3"></script>

<script>
(async function(){
  const url = '{{ "/assets/data/raleigh_hr.json" | relative_url }}?v={{ site.github.build_revision }}';
  let raw = [];
  try {
    const res = await fetch(url, { cache: 'no-store' });
    if (!res.ok) throw new Error('fetch failed: ' + res.status);
    raw = await res.json();
  } catch (e) {
    console.error('Could not load data:', e);
    document.getElementById('hrTimeline').insertAdjacentHTML(
      'beforebegin',
      '<p style="color:var(--muted)">No data available yet. Try again after the next update.</p>'
    );
    return;
  }
  if (!Array.isArray(raw) || raw.length === 0) {
    document.getElementById('hrTimeline').insertAdjacentHTML(
      'beforebegin',
      '<p style="color:var(--muted)">No regular-season home runs found for the selected window.</p>'
    );
    return;
  }

  // ...your existing sorting/chart/table code...
})();
</script>


<style>
/* compact table styling (feel free to move into custom.css) */
.table-wrap{ overflow:auto; border:1px solid var(--border); border-radius:8px; }
table.compact{ width:100%; border-collapse: collapse; font-size:.95rem; }
table.compact thead th{
  position: sticky; top: 0; background: var(--surface);
  text-align:left; padding:.5rem .6rem; border-bottom:1px solid var(--border);
}
table.compact tbody td{ padding:.45rem .6rem; border-bottom:1px solid var(--border); white-space:nowrap; }
table.compact tbody tr:hover{ background: rgba(0,0,0,.03); }
</style>
