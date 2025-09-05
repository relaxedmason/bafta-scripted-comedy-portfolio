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
  // Cache-bust to avoid stale GitHub Pages/CDN
  const url = '{{ "/assets/data/raleigh_hr.json" | relative_url }}?v={{ site.github.build_revision }}';

  // -------- Fetch & validate --------
  let data = [];
  try {
    const res = await fetch(url, { cache: 'no-store' });
    if (!res.ok) throw new Error('fetch ' + res.status);
    data = await res.json();
  } catch (e) {
    console.error('Could not load JSON:', e);
    document.getElementById('hrTimeline').insertAdjacentHTML(
      'beforebegin',
      '<p style="color:var(--muted)">No data available yet. Try again after the next update.</p>'
    );
    return;
  }
  if (!Array.isArray(data) || data.length === 0) {
    document.getElementById('hrTimeline').insertAdjacentHTML(
      'beforebegin',
      '<p style="color:var(--muted)">No regular-season home runs found for the current season.</p>'
    );
    document.getElementById('hrTotal').textContent = '0';
    return;
  }

  // -------- Normalize/derive fields --------
  const rows = data.map(d => ({
    game_date: d.game_date ? new Date(d.game_date) : null,
    venue_name: d.venue_name || '—',
    home: !!d.home,
    home_team: d.home_team || '—',
    away_team: d.away_team || '—',
    opp: (d.home ? (d.away_team || '—') : (d.home_team || '—')),
    dist: (d.hit_distance_sc != null ? Number(d.hit_distance_sc) : null),
    ev: (d.launch_speed != null ? Number(d.launch_speed) : null),
    la: (d.launch_angle != null ? Number(d.launch_angle) : null),
    pitcher: d.pitcher || '—',
    game_pk: d.game_pk || null
  })).filter(r => r.game_date instanceof Date && !isNaN(r.game_date));

  // KPI (big number)
  const total = rows.length;
  const kpiEl = document.getElementById('hrTotal');
  if (kpiEl) kpiEl.innerHTML = `${total} <small>HR this season</small>`;

  // Sort by date ASC for chart, DESC for table
  const ascByDate  = rows.slice().sort((a,b)=> a.game_date - b.game_date);
  const descByDate = rows.slice().sort((a,b)=> b.game_date - a.game_date);

  // -------- Ballpark filter options --------
  const sel = document.getElementById('venueFilter');
  const venues = Array.from(new Set(rows.map(r => r.venue_name).filter(Boolean))).sort();
  venues.forEach(v => sel.append(new Option(v, v)));

  // -------- Chart --------
  const ctx = document.getElementById('hrTimeline').getContext('2d');
  let chart;
  function buildChart(dataset){
    const pts = dataset
      .filter(r => r.dist != null)
      .map(r => ({ x: r.game_date, y: r.dist, venue: r.venue_name }));
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
          label: c => `${Math.round(c.raw.y)} ft — ${c.raw.venue || 'Unknown park'}`
        }}}
      }
    });
  }

  // -------- Table --------
  const tbody = document.querySelector('#hrTable tbody');
  const BTN_BATCH = 10;
  let shown = 0;
  function fmt(n, d=0){ return (n==null || isNaN(n)) ? '—' : Number(n).toFixed(d); }
  function renderRows(dataset, reset=false){
    if (reset){ tbody.innerHTML = ''; shown = 0; }
    const slice = dataset.slice(shown, shown + BTN_BATCH);
    slice.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${r.game_date.toLocaleDateString()}</td>
        <td>${r.opp}</td>
        <td>${r.venue_name}</td>
        <td>${fmt(r.dist,0)}</td>
        <td>${fmt(r.ev,0)}</td>
        <td>${fmt(r.la,0)}</td>
        <td>${r.pitcher}</td>
      `;
      tbody.appendChild(tr);
    });
    shown += slice.length;
    document.getElementById('showMore').disabled = shown >= dataset.length;
  }

  // -------- Filtering wiring --------
  function filteredRows(){
    const v = sel.value;
    return (v === 'all') ? descByDate : descByDate.filter(r => r.venue_name === v);
  }

  // Initial render
  buildChart(ascByDate);
  renderRows(descByDate, true);

  sel.addEventListener('change', () => {
    const v = sel.value;
    const fAsc  = (v === 'all') ? ascByDate  : ascByDate.filter(r => r.venue_name === v);
    const fDesc = filteredRows();
    buildChart(fAsc);
    renderRows(fDesc, true);
    // Update KPI to reflect filtered count (optional; comment out if you want season total only)
    // if (kpiEl) kpiEl.innerHTML = `${fDesc.length} <small>HR${v==='all'?' this season':''}</small>`;
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
