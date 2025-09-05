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
  const url = '{{ "/assets/data/raleigh_hr.json" | relative_url }}';
  const res = await fetch(url);
  const raw = await res.json();

  // Sort oldest→newest for the timeline
  const allData = raw.slice().sort((a,b)=> new Date(a.game_date) - new Date(b.game_date));

  // Build venue list
  const venues = Array.from(new Set(allData.map(d => d.venue_name).filter(Boolean))).sort();
  const sel = document.getElementById('venueFilter');
  venues.forEach(v => sel.append(new Option(v, v)));

  // Chart
  const ctx = document.getElementById('hrTimeline').getContext('2d');
  let chart;
  function buildChart(data){
    const pts = data.map(d => ({x:new Date(d.game_date), y:d.hit_distance_sc, venue:d.venue_name}));
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: 'scatter',
      data: { datasets: [{ label: 'HR Distance (ft)', data: pts }] },
      options: {
        parsing: false,
        scales: {
          x: { type: 'time', time: { unit: 'week' }, title: { display:true, text:'Game date' } },
          y: { title: { display:true, text:'Distance (ft)' }, suggestedMin: 300, suggestedMax: 500 }
        },
        plugins: { tooltip: { callbacks: {
          label: ctx => `${ctx.raw.y} ft — ${ctx.raw.venue}`
        }}}
      }
    });
  }

  // Table
  const tbody = document.querySelector('#hrTable tbody');
  const BTN_BATCH = 10;
  let shown = 0;
  function fmtNum(n, d=0){ return (n==null || isNaN(n)) ? '—' : Number(n).toFixed(d); }
  function opponentOf(row){
    // Who Raleigh faced (opponent team)
    return row.home ? row.away_team : row.home_team;
  }
  function renderRows(data, reset=false){
    if (reset){ tbody.innerHTML = ''; shown = 0; }
    const slice = data.slice(shown, shown + BTN_BATCH);
    slice.forEach(d => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${new Date(d.game_date).toLocaleDateString()}</td>
        <td>${opponentOf(d) || '—'}</td>
        <td>${d.venue_name || '—'}</td>
        <td>${fmtNum(d.hit_distance_sc,0)}</td>
        <td>${fmtNum(d.launch_speed,0)}</td>
        <td>${fmtNum(d.launch_angle,0)}</td>
        <td>${d.pitcher || '—'}</td>
      `;
      tbody.appendChild(tr);
    });
    shown += slice.length;
    document.getElementById('showMore').disabled = shown >= data.length;
  }

  // Filtering
  function filtered(){
    const v = sel.value;
    return (v==='all') ? allData : allData.filter(d => d.venue_name === v);
  }

  // Initial render
  buildChart(allData);
  renderRows(allData, true);

  // Handlers
  sel.addEventListener('change', () => {
    const d = filtered();
    buildChart(d);
    renderRows(d, true);
  });
  document.getElementById('showMore').addEventListener('click', () => {
    renderRows(filtered(), false);
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
