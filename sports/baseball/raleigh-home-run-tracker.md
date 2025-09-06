---
layout: default
title: Cal Raleigh Home Run Tracker
description: Auto-updating record of Cal Raleigh home runs with mode toggle (Date vs Distance) and ballpark filter.
permalink: /sports/baseball/mariners/raleigh-home-run-tracker/
---

<h1>Cal Raleigh Home Run Tracker</h1>
<p id="hrCountLine" class="subtitle bigcount" aria-live="polite">—</p>

<!-- Controls: one chart, two modes; ballpark filter appears only in Distance mode -->
<div class="controls">
  <div class="modes">
    <button id="mode-date" type="button" class="chip active" aria-pressed="true">By Date</button>
    <button id="mode-dist" type="button" class="chip" aria-pressed="false">By Distance</button>
  </div>

  <label id="venueWrap" for="venueFilter" class="venue" style="display:none;">
    Ballpark:
    <select id="venueFilter">
      <option value="__ALL__">All ballparks</option>
    </select>
  </label>
</div>

<div class="downloads" style="margin:0 0 1rem 0;">
  <a class="chip" href="{{ '/assets/data/raleigh_hr.csv' | relative_url }}" download>⬇️ Download CSV</a>
</div>

<!-- Make the chart FULL-BLEED (edge-to-edge) so it's wide enough -->
<div class="chart-wrap fullbleed">
  <canvas id="hrChart" aria-label="Home runs chart"></canvas>
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
    document.getElementById('hrChart').insertAdjacentHTML(
      'beforebegin',
      '<p style="color:var(--muted)">No data available yet. Try again after the next update.</p>'
    );
    document.getElementById('hrCountLine').textContent = '0 HR';
    return;
  }

  if (!Array.isArray(data) || data.length === 0) {
    document.getElementById('hrChart').insertAdjacentHTML(
      'beforebegin',
      '<p style="color:var(--muted)">No regular-season home runs found.</p>'
    );
    document.getElementById('hrCountLine').textContent = '0 HR';
    return;
  }

  // -------- Normalize to rows[] we control --------
  const rows = data.map(d => {
    const gd = d.game_date ? new Date(d.game_date) : null;
    const distance = (d.distance_ft != null && d.distance_ft !== '')
                      ? Number(d.distance_ft)
                      : (d.hit_distance_sc != null && d.hit_distance_sc !== '' ? Number(d.hit_distance_sc) : null);
    const homeTeam = d.home_team || '—';
    const awayTeam = d.away_team || '—';
    const isHome   = (d.home === true) || (String(d.inning_topbot || '').toLowerCase() === 'bot');
    return {
      game_date: gd && !isNaN(gd) ? gd : null,
      venue_name: d.venue_name || '—',
      home_team: homeTeam,
      away_team: awayTeam,
      opp: isHome ? awayTeam : homeTeam,
      dist: distance,
      ev:   (d.launch_speed    != null ? Number(d.launch_speed)    : null),
      la:   (d.launch_angle    != null ? Number(d.launch_angle)    : null),
      pitcher: d.pitcher || '—'
    };
  }).filter(r => r.game_date instanceof Date && !isNaN(r.game_date));

  // -------- Big subtitle count (season total) --------
  const countEl = document.getElementById('hrCountLine');
  const seasonTotal = rows.length;
  countEl.textContent = `${seasonTotal} HR`;

  // -------- Populate ballpark filter for Distance mode --------
  const sel = document.getElementById('venueFilter');
  const venueWrap = document.getElementById('venueWrap');
  const venues = Array.from(new Set(rows.filter(r => r.dist != null).map(r => r.venue_name))).sort();
  venues.forEach(v => sel.append(new Option(v, v)));

  // Sorted views for table
  const ascAll  = rows.slice().sort((a,b)=> a.game_date - b.game_date);
  const descAll = rows.slice().sort((a,b)=> b.game_date - a.game_date);

  // -------- Chart setup (single canvas, two modes) --------
  const ctx = document.getElementById('hrChart').getContext('2d');
  let chart;
  let mode = 'date';          // 'date' | 'distance'
  let currentVenue = '__ALL__';

  function seriesByDate() {
    // ALL parks, cumulative
    const sorted = ascAll;
    return sorted.map((r, i) => ({ x: r.game_date, y: i + 1, venue: r.venue_name, opp: r.opp }));
  }

  function seriesByDistance(venueVal) {
    let arr = rows.filter(r => r.dist != null);
    if (venueVal && venueVal !== '__ALL__') {
      arr = arr.filter(r => r.venue_name === venueVal);
    }
    // Longest → shortest
    arr.sort((a,b)=> b.dist - a.dist);
    return arr;
  }

  function renderChart() {
    if (chart) chart.destroy();

    if (mode === 'date') {
      const pts = seriesByDate();
      const minDate = pts.length ? new Date(pts[0].x.getTime() - 3*24*3600*1000) : undefined;
      const maxDate = pts.length ? new Date(pts[pts.length-1].x.getTime() + 3*24*3600*1000) : undefined;

      chart = new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [{
            label: 'Cumulative HR',
            data: pts, stepped: true, tension: 0, pointRadius: 1.5, fill: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,   // let the parent control height/width
          parsing: false,
          layout: { padding: { right: 8, left: 8 } }, // a touch of breathing room on full-bleed
          scales: {
            x: {
              type: 'time', time: { unit: 'day', round: 'day' },
              min: minDate, max: maxDate, offset: true,
              ticks: {
                autoSkip: true,
                maxTicksLimit: 14,  // avoid overcrowding on super-wide rows
                maxRotation: 0
              },
              title: { display: true, text: 'Game date' }
            },
            y: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: 'Cumulative HR' } }
          },
          plugins: {
            legend: { display: false },
            title: { display: true, text: 'Home Runs Over Time (All Ballparks)' },
            tooltip: {
              intersect: false, mode: 'nearest',
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
    } else {
      const arr = seriesByDistance(currentVenue);
      const labels = arr.map((r,i)=> `${i+1}. ${r.game_date.toLocaleDateString()} — ${r.venue_name}`);
      const values = arr.map(r=> r.dist);

      chart = new Chart(ctx, {
        type: 'bar',
        data: { labels, datasets: [{ data: values }] },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: { padding: { right: 8, left: 8 } },
          scales: {
            x: { display: false },
            y: { beginAtZero: true, title: { display: true, text: 'Feet' } }
          },
          plugins: {
            legend: { display: false },
            title: { display: true, text: `Home Runs by Distance (${currentVenue === '__ALL__' ? 'All Ballparks' : currentVenue})` },
            tooltip: {
              callbacks: {
                title: (items) => {
                  const i = items[0].dataIndex;
                  const r = arr[i];
                  return `${r.game_date.toLocaleDateString()} — ${r.venue_name}`;
                },
                label: (item) => `${Math.round(item.raw)} ft`
              }
            }
          }
        }
      });
    }
  }

  // -------- Compact table --------
  const tbody = document.querySelector('#hrTable tbody');
  const BTN_BATCH = 10;
  let shown = 0;

  function fmt(n, d=0){ return (n==null || isNaN(n)) ? '—' : Number(n).toFixed(d); }

  function currentTableDataDesc(){
    if (currentVenue === '__ALL__') return descAll;
    return rows.filter(r => r.venue_name === currentVenue).sort((a,b)=> b.game_date - a.game_date);
  }

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

  // -------- Wire controls --------
  const btnDate = document.getElementById('mode-date');
  const btnDist = document.getElementById('mode-dist');

  function updateBigNumber(){
    if (mode === 'distance' && currentVenue !== '__ALL__') {
      countEl.textContent = `${seriesByDistance(currentVenue).length} HR`;
    } else {
      countEl.textContent = `${seasonTotal} HR`;
    }
  }

  function setMode(newMode){
    mode = newMode;
    const isDate = mode === 'date';
    btnDate.classList.toggle('active', isDate);
    btnDist.classList.toggle('active', !isDate);
    btnDate.setAttribute('aria-pressed', isDate ? 'true' : 'false');
    btnDist.setAttribute('aria-pressed', !isDate ? 'true' : 'false');

    // Show venue dropdown only for Distance mode
    venueWrap.style.display = isDate ? 'none' : 'inline-flex';
    if (isDate) {
      currentVenue = '__ALL__';
      sel.value = '__ALL__';
    }
    renderChart();
    renderRows(currentTableDataDesc(), true);
    updateBigNumber();
  }

  btnDate.addEventListener('click', () => setMode('date'));
  btnDist.addEventListener('click', () => setMode('distance'));
  sel.addEventListener('change', (e) => {
    currentVenue = e.target.value;
    if (mode === 'distance') renderChart();
    renderRows(currentTableDataDesc(), true);
    updateBigNumber();
  });

  document.getElementById('showMore').addEventListener('click', () => {
    renderRows(currentTableDataDesc(), false);
  });

  // Initial paint
  setMode('date');
})();
</script>

<style>
.bigcount{
  font-size: clamp(2.5rem, 7vw, 3.75rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: .35rem auto 1rem;
}

/* Controls */
.controls{
  display:flex; gap:.75rem; align-items:center; flex-wrap:wrap; margin:.25rem 0 1rem 0;
}
.controls .modes{ display:flex; gap:.5rem; }
.controls .venue select{
  margin-left:.4rem; padding:.35rem .5rem; border:1px solid var(--border); border-radius:8px;
}

.chip{
  display:inline-block; padding:.35rem .75rem; border:1px solid var(--border);
  border-radius:999px; text-decoration:none;
}
.chip.active{ background: var(--surface-2, rgba(0,0,0,.05)); }

/* FULL-BLEED CHART: stretches to viewport width, not just the article column */
.chart-wrap{
  position: relative;
  width: 100%;
  margin: .5rem 0 1rem;
}
.chart-wrap.fullbleed{
  width: 100vw;                /* span the entire viewport width */
  left: 50%;
  right: 50%;
  margin-left: -50vw;          /* pull out of the centered content column */
  margin-right: -50vw;
  transform: translateX(0);    /* ensure proper centering across browsers */
}
.chart-wrap canvas{
  display:block;               /* important for correct sizing */
  width: 100% !important;      /* let Chart.js fill parent width */
  height: 480px !important;    /* control height here; Chart.js maintainAspectRatio=false */
}

/* Optional: cap the max-width on very large screens
   (comment these two lines if you want truly edge-to-edge at any size) */
@media (min-width: 1600px){
  .chart-wrap.fullbleed{ max-width: 1500px; margin-left: calc(50% - 750px); margin-right: calc(50% - 750px); }
}

/* Table */
.table-wrap{ overflow:auto; border:1px solid var(--border); border-radius:8px; }
table.compact{ width:100%; border-collapse: collapse; font-size:.95rem; }
table.compact thead th{
  position: sticky; top: 0; background: var(--surface);
  text-align:left; padding:.5rem .6rem; border-bottom:1px solid var(--border);
}
table.compact tbody td{ padding:.45rem .6rem; border-bottom:1px solid var(--border); white-space:nowrap; }
table.compact tbody tr:hover{ background: rgba(0,0,0,.03); }
</style>

