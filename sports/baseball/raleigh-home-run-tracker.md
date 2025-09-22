---
layout: default
title: Cal Raleigh Home Run Tracker
description: Auto-updating record of Cal Raleigh home runs with mode toggle (Date vs Distance vs Game #), ballpark filter, plus comparison overlay and a Catchers tab.
permalink: /sports/baseball/mariners/raleigh-home-run-tracker/
---

<h1>Cal Raleigh Home Run Tracker</h1>
<p id="hrCountLine" class="subtitle bigcount" aria-live="polite">—</p>

<!-- Controls: one chart, three modes; ballpark filter appears only in Distance mode -->
<div class="controls">
  <div class="modes">
    <button id="mode-date" type="button" class="chip active" aria-pressed="true">By Date</button>
    <button id="mode-dist" type="button" class="chip" aria-pressed="false">By Distance</button>

    <!-- NEW: third mode -->
    <button id="mode-game" type="button" class="chip" aria-pressed="false">By Game #</button>

    <!-- NEW: tabs (show only in Game # mode) -->
    <div id="groupTabs" class="tabs" style="display:none;">
      <button type="button" class="chip tab active" data-group="all" aria-pressed="true">All hitters</button>
      <button type="button" class="chip tab" data-group="catchers" aria-pressed="false">Catchers</button>
    </div>

    <!-- NEW: player picker (show only in Game # mode) -->
    <div id="playerPicker" class="players" style="display:none;">
      <span id="playerDynamic"></span>
    </div>
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

  // NEW: comparison datasets (best season per player; and catchers-only)
  const urlCompAll  = '{{ "/assets/assets/data/hr_compare_top_per_player.json" | relative_url }}?v={{ site.github.build_revision }}';
  const urlCompCats = '{{ "/assets/assets/data/hr_compare_catchers.json"    | relative_url }}?v={{ site.github.build_revision }}';


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

  // NEW: load comparison datasets (non-fatal if missing)
  let compAll = [], compCatchers = [];
  try {
    const [aRes, cRes] = await Promise.all([
      fetch(urlCompAll,  { cache: 'no-store' }),
      fetch(urlCompCats, { cache: 'no-store' })
    ]);
    if (aRes.ok) compAll = await aRes.json();
    if (cRes.ok) compCatchers = await cRes.json();
  } catch (_) {}

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

    // NEW: capture a team game number if your updater provides one
    const gnum = (
      d.team_game_number ?? d.game_number ?? d.team_game_num ?? d.game_no ??
      d.Gtm ?? d['Tm#'] ?? d['Gm#'] ?? d.G
    );

    return {
      game_date: gd && !isNaN(gd) ? gd : null,
      team_game_number: (gnum != null ? Number(gnum) : null),
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

  // -------- Chart setup (one canvas, three modes) --------
  const ctx = document.getElementById('hrChart').getContext('2d');
  let chart;
  let mode = 'date';
  let currentVenue = '__ALL__';

  // NEW: elements & state for Game # mode
  const btnDate = document.getElementById('mode-date');
  const btnDist = document.getElementById('mode-dist');
  const btnGame = document.getElementById('mode-game');
  const groupTabs = document.getElementById('groupTabs');
  const picker = document.getElementById('playerPicker');
  const pickerDyn = document.getElementById('playerDynamic');

  let group = 'all'; // 'all' | 'catchers'
  const DEFAULT_COMPARE_ALL  = ['ruth_1927','maris_1961','bonds_2001','mcgwire_1998','sosa_1998','judge_2022','griffey_1998','bench_1970'];
  const DEFAULT_COMPARE_CATS = ['bench_1970','campanella_1953','lopez_2003','hundley_1996','piazza_1999'];

  // Raleigh always selectable; defaults depend on group
  let selectedPlayers = new Set(['raleigh', ...DEFAULT_COMPARE_ALL]);

  function currentGroupPlayers(){
    if (group === 'catchers') return Array.isArray(compCatchers) ? compCatchers : [];
    return Array.isArray(compAll) ? compAll : [];
  }

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

  // Build Cal’s cumulative by Game # (1..162) from team_game_number
  function raleighSeriesByGame() {
    const pts = rows
      .filter(r => Number.isFinite(r.team_game_number))
      .sort((a,b) => a.team_game_number - b.team_game_number);

    if (!pts.length) return null;

    // count HRs per team game
    const byG = new Map();
    pts.forEach(r => byG.set(r.team_game_number, (byG.get(r.team_game_number) || 0) + 1));

    let cum = 0;
    const series = [];
    for (let g=1; g<=162; g++){
      if (byG.has(g)) cum += byG.get(g);
      series.push({ g, cum });
    }
    // trim trailing zeros
    let last = -1;
    for (let i=series.length-1; i>=0; i--) { if (series[i].cum > 0) { last = i; break; } }
    return series.slice(0, Math.max(last+1, 1));
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

  function buildPlayerPickerUI(){
    pickerDyn.innerHTML = '';
    const arr = currentGroupPlayers().slice();

    // keep defaults first, then alpha
    const pref = new Map((group==='catchers' ? DEFAULT_COMPARE_CATS : DEFAULT_COMPARE_ALL).map((id,i)=>[id,i]));
    arr.sort((a,b)=>{
      const ai = pref.has(a.id) ? pref.get(a.id) : 1e9;
      const bi = pref.has(b.id) ? pref.get(b.id) : 1e9;
      return ai - bi || a.label.localeCompare(b.label);
    });

    arr.forEach(p=>{
      const id = p.id;
      const label = document.createElement('label');
      label.className = 'chip';
      label.style.cssText = 'gap:.4rem; display:inline-flex; align-items:center;';
      label.innerHTML = `<input type="checkbox" value="${id}"> ${p.label}`;
      const input = label.querySelector('input');
      input.checked = selectedPlayers.has(id);
      input.addEventListener('change', e => {
        if (e.target.checked) selectedPlayers.add(id);
        else selectedPlayers.delete(id);
        renderChart();
      });
      pickerDyn.appendChild(label);
    });
  }

  function renderChart() {
    if (chart) chart.destroy();

    // NEW: Game # mode
    if (mode === 'game') {
      const datasets = [];

      // Cal (only if team_game_number present)
      if (selectedPlayers.has('raleigh')) {
        const rs = raleighSeriesByGame();
        if (rs && rs.length) {
          datasets.push({
            label: 'Cal Raleigh — current season',
            data: rs.map(d => ({x:d.g, y:d.cum})),
            parsing: false, stepped: true, pointRadius: 0, tension: 0
          });
        }
      }

      // Comparison players for current group
      const compareArr = currentGroupPlayers();
      compareArr.forEach(p => {
        if (!selectedPlayers.has(p.id)) return;
        const s = (p.series || []).map(d => ({x:d.g, y:d.cum}));
        if (!s.length) return;
        datasets.push({
          label: p.label,
          data: s,
          parsing: false, stepped: true, pointRadius: 0, tension: 0
        });
      });

      chart = new Chart(ctx, {
        type: 'line',
        data: { datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          parsing: false,
          scales: {
            x: { type: 'linear', min: 1, max: 162, ticks: { stepSize: 10 }, title: { display: true, text: 'Game #' } },
            y: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: 'Cumulative HR' } }
          },
          plugins: {
            legend: { display: true },
            title: { display: true, text: group==='catchers' ? 'Cumulative HR by Game — Catchers' : 'Cumulative HR by Game — All hitters' },
            tooltip: {
              intersect: false, mode: 'nearest',
              callbacks: { title: items => `Game ${items[0].parsed.x}`, label: c => `${c.dataset.label}: ${c.parsed.y} HR` }
            }
          },
          elements: { line: { borderWidth: 2 } }
        }
      });
      return; // don't fall through to other modes
    }

    // Existing: Date mode
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
      // Existing: Distance mode
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
  function updateBigNumber(){
    if(mode==='distance'&&currentVenue!=='__ALL__'){countEl.textContent=`${seriesByDistance(currentVenue).length} HR`;}
    else{countEl.textContent=`${seasonTotal} HR`;}
  }
  function setMode(m){
    mode=m;
    const isDate = mode==='date';
    const isDist = mode==='distance';
    const isGame = mode==='game';

    btnDate.classList.toggle('active',isDate);
    btnDist.classList.toggle('active',isDist);
    btnGame.classList.toggle('active',isGame);

    btnDate.setAttribute('aria-pressed',isDate);
    btnDist.setAttribute('aria-pressed',isDist);
    btnGame.setAttribute('aria-pressed',isGame);

    // Venue filter only in Distance; tabs/picker only in Game
    venueWrap.style.display = isDist ? 'inline-flex' : 'none';
    groupTabs.style.display  = isGame ? 'inline-flex' : 'none';
    picker.style.display     = isGame ? 'inline-flex' : 'none';

    if (!isDist){ currentVenue='__ALL__'; sel.value='__ALL__'; }

    if (isGame){
      // reset defaults when entering Game mode
      selectedPlayers = new Set(['raleigh', ...(group==='catchers' ? DEFAULT_COMPARE_CATS : DEFAULT_COMPARE_ALL)]);
      buildPlayerPickerUI();
    }

    renderChart();
    renderRows(currentTableData(), true);
    updateBigNumber();
  }
  btnDate.addEventListener('click',()=>setMode('date'));
  btnDist.addEventListener('click',()=>setMode('distance'));
  btnGame.addEventListener('click',()=>setMode('game'));

  groupTabs.addEventListener('click', (e) => {
    const b = e.target.closest('button.tab'); if (!b) return;
    group = b.dataset.group; // 'all' | 'catchers'
    [...groupTabs.querySelectorAll('.tab')].forEach(btn=>{
      const on = btn.dataset.group===group;
      btn.classList.toggle('active', on);
      btn.setAttribute('aria-pressed', on);
    });
    selectedPlayers = new Set(['raleigh', ...(group==='catchers' ? DEFAULT_COMPARE_CATS : DEFAULT_COMPARE_ALL)]);
    buildPlayerPickerUI();
    renderChart();
  });

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

/* NEW: tabs & player picker */
.controls .tabs { display:flex; gap:.5rem; align-items:center; }
.controls .tabs .tab.active{
  background: var(--chip-active-bg, #e6f0ff);
  border-color: var(--chip-active-border, #8ab4ff);
}
.controls .players{ display:flex; gap:.5rem; flex-wrap:wrap; align-items:center; }

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
