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

<div class="chart-wrap">
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
      'beforebegin','<p class="muted">No data available yet.</p>'
    );
    document.getElementById('hrCountLine').textContent = '0 HR';
    return;
  }

  if (!Array.isArray(data) || data.length === 0) {
    document.getElementById('hrChart').insertAdjacentHTML(
      'beforebegin','<p class="muted">No home runs found.</p>'
    );
    document.getElementById('hrCountLine').textContent = '0 HR';
    return;
  }

  // -------- Normalize rows --------
  const rows = data.map(d => {
    const gd = d.game_date ? new Date(d.game_date) : null;
    const dist = (d.distance_ft != null ? Number(d.distance_ft)
                : (d.hit_distance_sc != null ? Number(d.hit_distance_sc) : null));
    const homeTeam = d.home_team || '—';
    const awayTeam = d.away_team || '—';
    const isHome   = (d.home === true) || (String(d.inning_topbot||'').toLowerCase()==='bot');
    return {
      game_date: gd && !isNaN(gd) ? gd : null,
      venue_name: d.venue_name || '—',
      home_team: homeTeam,
      away_team: awayTeam,
      opp: isHome ? awayTeam : homeTeam,
      dist: dist,
      ev: d.launch_speed != null ? Number(d.launch_speed) : null,
      la: d.launch_angle != null ? Number(d.launch_angle) : null,
      pitcher: d.pitcher || '—'
    };
  }).filter(r => r.game_date instanceof Date && !isNaN(r.game_date));

  // Subtitle count
  const countEl = document.getElementById('hrCountLine');
  const seasonTotal = rows.length;
  countEl.textContent = `${seasonTotal} HR`;

  // Filters + sorted views
  const sel = document.getElementById('venueFilter');
  const venueWrap = document.getElementById('venueWrap');
  const venues = Array.from(new Set(rows.filter(r=>r.dist!=null).map(r=>r.venue_name))).sort();
  venues.forEach(v => sel.append(new Option(v, v)));

  const ascAll  = rows.slice().sort((a,b)=> a.game_date - b.game_date);
  const descAll = rows.slice().sort((a,b)=> b.game_date - a.game_date);

  // -------- Chart setup (one canvas, two modes) --------
  const ctx = document.getElementById('hrChart').getContext('2d');
  let chart;
  let mode = 'date';
  let currentVenue = '__ALL__';

  // Build a clean cumulative series (By Date)
  function seriesByDate() {
    return ascAll.map((r,i)=>({x:r.game_date,y:i+1,venue:r.venue_name,opp:r.opp}));
  }

  // Build a distance-sorted series (By Distance)
  function seriesByDistance(v) {
    let arr = rows.filter(r=>r.dist!=null);
    if (v && v!=='__ALL__') arr = arr.filter(r=>r.venue_name===v);
    arr.sort((a,b)=> b.dist - a.dist);
    return arr;
  }

  // Force x-axis to show ALL months from first → last HR month (so it always shows months)
  function monthBoundsAndTicks(dataset) {
    if (!dataset.length) return {};
    const first = new Date(dataset[0].x);
    const last  = new Date(dataset[dataset.length - 1].x);
    const start = new Date(first.getFullYear(), first.getMonth(), 1);
    const end   = new Date(last.getFullYear(),  last.getMonth() + 1, 0);

    const ticks = [];
    const cur = new Date(start);
    while (cur <= end) {
      ticks.push(new Date(cur));
      cur.setMonth(cur.getMonth() + 1);
      cur.setDate(1);
    }
    return { start, end, ticks };
  }

  function renderChart() {
    if (chart) chart.destroy();

    if (mode === 'date') {
      const pts = seriesByDate();
      const { start, end, ticks } = monthBoundsAndTicks(pts);

      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ticks || [], // ensures all months appear
          datasets: [{
            label: 'Cumulative HR',
            data: pts,
            parsing: false,
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
              time: { unit: 'month', displayFormats: { month: 'MMM' } },
              min: start,
              max: end,
              ticks: { autoSkip: false, maxRotation: 0 }
            },
            y: {
              beginAtZero: true,
              ticks: { precision: 0 },
              title: { display: true, text: 'Cumulative HR' }
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
    } else {
      const arr = seriesByDistance(currentVenue);
      chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: arr.map((r,i)=>`${i+1}. ${r.game_date.toLocaleDateString()} — ${r.venue_name}`),
          datasets: [{ data: arr.map(r=>r.dist) }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { display: false },
            y: { beginAtZero: true, title: { display: true, text: 'Feet' } }
          },
          plugins: {
            legend: { display: false },
            title: { display: true, text: `Home Runs by Distance (${currentVenue === '__ALL__' ? 'All Parks' : currentVenue})` },
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

  // -------- Table --------
  const tbody=document.querySelector('#hrTable tbody');
  let shown=0; const BTN_BATCH=10;
  function fmt(n,d=0){return(n==null||isNaN(n))?'—':Number(n).toFixed(d);}
  function currentTableData(){if(currentVenue==='__ALL__')return descAll;return rows.filter(r=>r.venue_name===currentVenue).sort((a,b)=>b.game_date-a.game_date);}
  function renderRows(dataset,reset=false){
    if(reset){tbody.innerHTML='';shown=0;}
    const slice=dataset.slice(shown,shown+BTN_BATCH);
    slice.forEach(r=>{
      const tr=document.createElement('tr');
      tr.innerHTML=`<td>${r.game_date.toLocaleDateString()}</td><td>${r.opp}</td><td>${r.venue_name}</td><td>${fmt(r.dist,0)}</td><td>${fmt(r.ev,0)}</td><td>${fmt(r.la,0)}</td><td>${r.pitcher}</td>`;
      tbody.appendChild(tr);
    });
    shown+=slice.length;
    document.getElementById('showMore').disabled = shown >= dataset.length;
  }

  // -------- Controls --------
  const btnDate=document.getElementById('mode-date');
  const btnDist=document.getElementById('mode-dist');

  function updateBigNumber(){
    if(mode==='distance'&&currentVenue!=='__ALL__'){countEl.textContent=`${seriesByDistance(currentVenue).length} HR`;}
    else{countEl.textContent=`${seasonTotal} HR`;}
  }
  function setMode(m){
    mode=m; const isDate=mode==='date';
    btnDate.classList.toggle('active',isDate);
    btnDist.classList.toggle('active',!isDate);
    btnDate.setAttribute('aria-pressed',isDate);
    btnDist.setAttribute('aria-pressed',!isDate);
    venueWrap.style.display = isDate ? 'none' : 'inline-flex';
    if(isDate){ currentVenue='__ALL__'; sel.value='__ALL__'; }
    renderChart();
    renderRows(currentTableData(), true);
    updateBigNumber();
  }
  btnDate.addEventListener('click',()=>setMode('date'));
  btnDist.addEventListener('click',()=>setMode('distance'));
  sel.addEventListener('change',e=>{
    currentVenue=e.target.value;
    if(mode==='distance') renderChart();
    renderRows(currentTableData(), true);
    updateBigNumber();
  });
  document.getElementById('showMore').addEventListener('click',()=>renderRows(currentTableData(),false));

  // Initial paint
  setMode('date');
})();
</script>

<style>
/* Big count */
.bigcount{
  font-size: clamp(2.5rem, 7vw, 3.75rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: .35rem auto 1rem;
}

/* Controls */
.controls{ display:flex; gap:.75rem; align-items:center; flex-wrap:wrap; margin:.25rem 0 1rem 0; }
.controls .modes{ display:flex; gap:.5rem; }
.controls .venue select{
  margin-left:.4rem; padding:.4rem .6rem;
  border:1px solid var(--border, #c9c9c9); border-radius:8px;
  background: var(--surface, #fff); color: var(--text, #111);
}

/* HIGH-CONTRAST CHIPS (so the By Distance button is visible in dark mode) */
button.chip, .chip{
  -webkit-appearance: none; appearance: none;
  background: var(--chip-bg, #f4f4f5);
  color: var(--chip-fg, #111);
  border: 1px solid var(--chip-border, #c9c9c9);
  padding: .4rem .75rem; border-radius: 999px;
  cursor: pointer; text-decoration: none; line-height: 1;
}
button.chip:hover, .chip:hover{ filter: brightness(0.95); }
button.chip.active, .chip.active{
  background: var(--chip-active-bg, #e6f0ff);
  border-color: var(--chip-active-border, #8ab4ff);
}
button.chip:focus-visible{
  outline: 2px solid var(--chip-focus, #8ab4ff);
  outline-offset: 2px;
}

/* Dark mode overrides for strong contrast */
@media (prefers-color-scheme: dark){
  :root{
    --text: #e8e8e8;
    --surface: #151515;
    --border: rgba(255,255,255,.22);

    --chip-bg: rgba(255,255,255,.10);
    --chip-fg: #e8e8e8;
    --chip-border: rgba(255,255,255,.32);
    --chip-active-bg: rgba(59,130,246,.28);      /* visible blue-ish */
    --chip-active-border: rgba(59,130,246,.65);
    --chip-focus: #93c5fd;
  }

  .controls .venue select{
    background: var(--surface);
    color: var(--text);
    border-color: var(--border);
  }
}

/* Chart sizing */
.chart-wrap{ width:100%; height:420px; margin:.5rem 0 1rem; }
#hrChart{ display:block; width:100% !important; height:100% !important; max-width:none; }

/* Table */
.table-wrap{ overflow:auto; border:1px solid var(--border, #ddd); border-radius:8px; }
table.compact{ width:100%; border-collapse: collapse; font-size:.95rem; color: var(--text, #111); }
table.compact thead th{
  position: sticky; top: 0;
  background: var(--surface, #fff);
  text-align:left; padding:.5rem .6rem; border-bottom:1px solid var(--border, #ddd);
}
table.compact tbody td{
  padding:.45rem .6rem; border-bottom:1px solid var(--border, #eee); white-space:nowrap;
}
table.compact tbody tr:hover{ background: var(--surface-2, rgba(0,0,0,.06)); }

.muted{ color: var(--muted, #777); }
@media (prefers-color-scheme: dark){
  .muted{ color:#aaa; }
}
</style>

