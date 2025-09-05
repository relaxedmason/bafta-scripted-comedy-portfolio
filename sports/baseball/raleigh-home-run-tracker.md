---
layout: default
title: Cal Raleigh Home Run Tracker
description: Auto-updating record of Cal Raleigh home runs with distance, EV, LA, and ballpark filter.
permalink: /sports/baseball/mariners/raleigh-home-run-tracker/
---


<h1>Cal Raleigh Home Run Tracker</h1>
<p class="subtitle">Auto-updating via GitHub Actions · Filter by ballpark · Download CSV</p>
<div id="hrTotal" class="kpi" aria-live="polite">—</div>

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
  // 1. Fetch JSON, build rows[] ...
  // (this part stays as you already have)

  // 2. KPI number
  // (stays the same)

  // 3. Chart code (REPLACE with the cumulative line version I gave you)
  const ctx = document.getElementById('hrTimeline').getContext('2d');
  let chart;

  function toCumulative(dataset){
    const sorted = dataset.slice().sort((a,b)=> a.game_date - b.game_date);
    return sorted.map((r, i) => ({ x: r.game_date, y: i + 1, venue: r.venue_name, opp: r.opp }));
  }

  function buildChart(dataset){
    const pts = toCumulative(dataset);
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: 'line',
      data: { datasets: [{ label: 'Cumulative HR', data: pts, tension: 0.25, pointRadius: 2 }] },
      options: {
        parsing: false,
        scales: {
          x: { type: 'time', time: { unit: 'week' }, title: { display:true, text:'Game date' } },
          y: { title: { display:true, text:'Cumulative HR' }, beginAtZero:true, ticks:{precision:0} }
        },
        plugins: { legend: { display:false } }
      }
    });
  }

  // 4. Table rendering
  // (keep your renderRows() etc.)

  // 5. Filtering wiring (REPLACE just this small part)
  function filteredRows(){
    const v = document.getElementById('venueFilter').value;
    return (v === 'all')
      ? rows.slice().sort((a,b)=> b.game_date - a.game_date)
      : rows.filter(r => r.venue_name === v).sort((a,b)=> b.game_date - a.game_date);
  }

  // Initial render
  buildChart(rows);
  renderRows(filteredRows(), true);

  document.getElementById('venueFilter').addEventListener('change', () => {
    const v = document.getElementById('venueFilter').value;
    const asc = (v === 'all')
      ? rows.slice().sort((a,b)=> a.game_date - b.game_date)
      : rows.filter(r => r.venue_name === v).sort((a,b)=> a.game_date - b.game_date);

    buildChart(asc);
    renderRows(filteredRows(), true);
  });

  document.getElementById('showMore').addEventListener('click', () => {
    renderRows(filteredRows(), false);
  });
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
