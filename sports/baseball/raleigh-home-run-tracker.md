---
layout: default
title: Cal Raleigh Home Run Tracker
description: Auto-updating record of Cal Raleigh home runs with venue filter and cumulative chart.
permalink: /sports/baseball/mariners/raleigh-home-run-tracker/
---

<h1>Cal Raleigh Home Run Tracker</h1>
<p id="hrCountLine" class="subtitle bigcount" aria-live="polite">—</p>

<label for="venueFilter" class="sr-only">Filter by ballpark</label>
<select id="venueFilter" style="margin:0 0 1rem 0;">
  <option value="all">All ballparks</option>
</select>

<div style="margin: 0 0 1rem 0;">
  <a class="chip" href="{{ '/assets/data/raleigh_hr.csv' | relative_url }}" download>⬇️ Download CSV</a>
</div>

<!-- Make the chart responsive by sizing its container; Chart.js fills it -->
<div class="chart-wrap">
  <canvas id="hrTimeline" aria-label="Cumulative home runs over time"></canvas>
</div>

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
  // -------- Fetch JSON (cache-busted) --------
  const url = '{{ "/assets/data/raleigh_hr.json" | relative_url }}?v={{ site.github.build_revision }}';
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
    document.getElementById('hrCountLine').textContent = '0 HR';
    return;
  }

  if (!Array.isArray(data) || data.length === 0) {
    document.getElementById('hrTimeline').insertAdjacentHTML(
      'beforebegin',
      '<p style="color:var(--muted)">No regular-season home runs found.</p>'
    );
    document.getElementById('hrCountLine').textContent = '0 HR';
    return;
  }

  // -------- Normalize to rows[] we control --------
  const rows = data.map(d => {
    const gd = d.game_date ? new Date(d.game_date) : null;
    return {
      game_date: gd && !isNaN(gd) ? gd : null,
      venue_name: d.venue_name || '—',
      home: !!d.home,
      home_team: d.home_team || '—',
      away_team: d.away_team || '—',
      opp: d.home ? (d.away_team || '—') : (d.home_team || '—'),
      dist: (d.hit_distance_sc != null ? Number(d.hit_distance_sc) : null),
      ev:   (d.launch_speed    != null ? Number(d.launch_speed)    : null),
      la:   (d.launch_angle    != null ? Number(d.launch_angle)    : null),
      pitcher: d.pitcher || '—'
    };
  }).filter(r => r.game_date instanceof Date && !isNaN(r.game_date));

  // Big subtitle: just the count (season total)
  const total = rows.length;
  const countEl = document.getElementById('hrCountLine');
  if (countEl) countEl.textContent = `${total} HR`;

  // -------- Populate ballpark filter --------
  const sel = document.getElementById('venueFilter');
  const venues = Array.from(new Set(rows.map(r => r.venue_name).filter(Boolean))).sort();
  venues.forEach(v => sel.append(new Option(v, v)));

  // Sorted views
  const ascAll  = rows.slice().sort((a,b)=> a.game_date - b.game_date);
  const descAll = rows.slice().sort((a,b)=> b.game_date - a.game_date);

  // -------- Cumulative line chart (by date; stepped; daily spacing) --------
  const ctx = document.getElementById('hrTimeline').getContext('2d');
  let chart;

  function toCumulative(dataset){
    const sorted = dataset.slice().sort((a,b)=> a.game_date - b.game_date);
    return sorted.map((r, i) => ({ x: r.game_date, y: i + 1, venue: r.venue_name, opp: r.opp }));
  }

  function buildChart(dataset){
    const pts = toCumulative(dataset);
    const minDate = pts.length ? new Date(pts[0].x.getTime() - 3*24*3600*1000) : undefined;
    const maxDate = pts.length ? new Date(pts[pts.length-1].x.getTime() + 3*24*3600*1000) : undefined;

    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: 'line',
      data: {
        datasets: [{
          label: 'Cumulative HR',
          data: pts,
          stepped: true,
          tension: 0,
          pointRadius: 1.5,
          fill: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        parsing: false,
        scales: {
          x: {
            type: 'time',
            time: { unit: 'day', round: 'day' },
            min: minDate,
            max: maxDate,
            offset: true,
            ticks: { autoSkip: true, maxRotation: 0 },
            title: { display:true, text:'Game date' }
          },
          y: {
            title: { display:true, text:'Cumulative HR' },
            beginAtZero: true,
            ticks: { precision: 0 }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            intersect: false,
            mode: 'nearest',
            callbacks: {
              label: c => {
                const d = c.raw;
                const n = c.parsed.y;
                const date = new Date(d.x).toLocaleDateString();
                return `#${n} on ${date} — ${d.venue || 'Unknown park'} vs ${d.opp || '?'}`;
              }
            }
          }
        },
        elements: { line: { borderWidth: 2 } }
      }
    });
  }

  // -------- Compact table --------
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
  function filteredDesc(){
    const v = sel.value;
    return (v === 'all') ? descAll
                         : rows.filter(r => r.venue_name === v).sort((a,b)=> b.game_date - a.game_date);
  }
  function filteredAsc(){
    const v = sel.value;
    return (v === 'all') ? ascAll
                         : rows.filter(r => r.venue_name === v).sort((a,b)=> a.game_date - b.game_date);
  }

  // Initial render
  buildChart(ascAll);
  renderRows(descAll, true);

  sel.addEventListener('change', () => {
    buildChart(filteredAsc());
    renderRows(filteredDesc(), true);
  });

  document.getElementById('showMore').addEventListener('click', () => {
    renderRows(filteredDesc(), false);
  });
})();
</script>

<style>
/* Big, clean count in the subtitle line */
.bigcount{
  font-size: clamp(2.5rem, 7vw, 3.75rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: .35rem auto 1rem;
}

/* Chart container controls final height; canvas fills it */
.chart-wrap{
  width: 100%;
  height: 420px;              /* tweak to taste */
  margin: .5rem 0 1rem;
}
#hrTimeline{
  display:block;
  width:100% !important;
  height:100% !important;     /* fill the 420px parent */
  max-width:none;
}

/* compact table styling */
.table-wrap{ overflow:auto; border:1px solid var(--border); border-radius:8px; }
table.compact{ width:100%; border-collapse: collapse; font-size:.95rem; }
table.compact thead th{
  position: sticky; top: 0; background: var(--surface);
  text-align:left; padding:.5rem .6rem; border-bottom:1px solid var(--border);
}
table.compact tbody td{ padding:.45rem .6rem; border-bottom:1px solid var(--border); white-space:nowrap; }
table.compact tbody tr:hover{ background: rgba(0,0,0,.03); }
</style>
