---
layout: default
title: Cal Raleigh Home Run Tracker
description: Auto-updating record of Cal Raleigh home runs with Date, Distance, and Historical Pace (game #) comparison, Catchers tab, Pace Stats, sorting, zoom, and table filters.
permalink: /sports/baseball/mariners/raleigh-home-run-tracker/
---

<h1>Cal Raleigh Home Run Tracker</h1>
<p id="hrCountLine" class="subtitle bigcount" aria-live="polite">—</p>

<!-- Controls: Historical Pace, Date, Distance; venue filter appears only in Distance mode -->
<div class="controls">
  <div class="modes">
    <!-- Historical Pace first -->
    <button id="mode-pace" type="button" class="chip" aria-pressed="false">Historical Pace</button>
    <button id="mode-date" type="button" class="chip active" aria-pressed="true">By Date</button>
    <button id="mode-dist" type="button" class="chip" aria-pressed="false">By Distance</button>

    <!-- Tabs for Historical Pace mode -->
    <div id="groupTabs" class="tabs" style="display:none;">
      <button type="button" class="chip tab active" data-group="all" aria-pressed="true">All hitters</button>
      <button type="button" class="chip tab" data-group="catchers" aria-pressed="false">Catchers</button>
    </div>

    <!-- Player picker for Historical Pace mode -->
    <div id="playerPicker" class="players" style="display:none;">
      <span id="playerDynamic"></span>
    </div>

    <!-- Quick range + zoom (pace mode only) -->
    <div id="rangeQuick" class="quickrange" style="display:none;">
      <button class="chip qr" data-range="1-50">G 1–50</button>
      <button class="chip qr" data-range="51-100">G 51–100</button>
      <button class="chip qr" data-range="101-162">G 101–162</button>
      <button class="chip qr" data-range="full">Full</button>
      <button id="resetZoom" class="chip">Reset zoom</button>
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

<h2 style="margin-top:1.25rem;">Home Runs</h2>

<!-- Table subtabs -->
<div class="subtabs">
  <button id="tblLogBtn"  type="button" class="chip active" aria-pressed="true">Game Log</button>
  <button id="tblPaceBtn" type="button" class="chip" aria-pressed="false">Pace Stats</button>
</div>

<!-- Filters (used by both Game Log and Pace Stats; for Pace Stats, Search filters player names) -->
<div id="tableFilters" class="filters" aria-label="Filter tables">
  <input id="fText" type="search" placeholder="Search opponent / venue / pitcher / player" aria-label="Search text">
  <label>From <input id="fFrom" type="date" aria-label="From date"></label>
  <label>To <input id="fTo" type="date" aria-label="To date"></label>
  <label>Min dist <input id="fMinDist" type="number" inputmode="numeric" step="1" min="0" aria-label="Min distance (ft)"></label>
  <label>Max dist <input id="fMaxDist" type="number" inputmode="numeric" step="1" min="0" aria-label="Max distance (ft)"></label>
  <button id="fClear" type="button" class="chip">Clear</button>
</div>

<!-- Game Log table -->
<div id="logWrap" class="table-wrap">
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

<!-- Pace Stats table (sortable headers) -->
<div id="paceWrap" class="table-wrap" style="display:none; margin-top:.75rem;">
  <table id="paceTable" class="compact">
    <thead>
      <tr>
        <th class="sortable" data-sort="label">Player</th>
        <th class="sortable" data-sort="g">Through G</th>
        <th class="sortable" data-sort="hr">HR</th>
        <th class="sortable" data-sort="pace">Pace / 162</th>
        <th class="sortable" data-sort="g10">G10</th>
        <th class="sortable" data-sort="g20">G20</th>
        <th class="sortable" data-sort="g50">G50</th>
        <th class="sortable" data-sort="g100">G100</th>
        <th class="sortable" data-sort="g150">G150</th>
        <th class="sortable" data-sort="g162">G162</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@3"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@2"></script>

<script>
(async function(){
  // Try to register zoom plugin if exposed
  try{
    if (window['chartjs-plugin-zoom']) { Chart.register(window['chartjs-plugin-zoom']); }
    if (window.ChartZoom) { Chart.register(window.ChartZoom); }
    if (window.chartjsPluginZoom) { Chart.register(window.chartjsPluginZoom); }
  }catch(e){ /* non-fatal */ }

  // -------- Fetch Raleigh JSON --------
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

  // -------- Robust loader for comparison datasets (tries both paths) --------
  const compAllCandidates = [
    '{{ "/assets/data/hr_compare_top_per_player.json" | relative_url }}?v={{ site.github.build_revision }}',
    '{{ "/assets/assets/data/hr_compare_top_per_player.json" | relative_url }}?v={{ site.github.build_revision }}'
  ];
  const compCatsCandidates = [
    '{{ "/assets/data/hr_compare_catchers.json" | relative_url }}?v={{ site.github.build_revision }}',
    '{{ "/assets/assets/data/hr_compare_catchers.json" | relative_url }}?v={{ site.github.build_revision }}'
  ];
  const raleighCandidates = [
    '{{ "/assets/data/hr_compare_raleigh.json" | relative_url }}?v={{ site.github.build_revision }}',
    '{{ "/assets/assets/data/hr_compare_raleigh.json" | relative_url }}?v={{ site.github.build_revision }}'
  ];

  async function loadFirst(candidates){
    for (const u of candidates){
      try{
        const r = await fetch(u, { cache:'no-store' });
        if (!r.ok) { console.warn('[compare]', u, r.status); continue; }
        const txt = await r.text();
        if (!txt.trim()) return [];
        return JSON.parse(txt);
      }catch(e){ console.warn('[compare] error', e); }
    }
    return [];
  }
  function normalizeSeries(series){
    if (!series) return [];
    if (Array.isArray(series) && typeof series[0]==='number'){
      const games = series.slice().map(Number).filter(Number.isFinite).sort((a,b)=>a-b);
      let cum=0, out=[], i=0;
      for(let g=1; g<=162; g++){
        while(i<games.length && games[i]===g){ cum++; i++; }
        out.push({ g, cum });
      }
      let last=out.length-1; while(last>0 && out[last].cum===0) last--;
      return out.slice(0,last+1);
    }
    if (Array.isArray(series)){
      return series.map(pt=>{
        const g = Number(pt.g ?? pt.game ?? pt.x);
        const cum = Number(pt.cum ?? pt.total ?? pt.y);
        return (Number.isFinite(g) && Number.isFinite(cum)) ? { g, cum } : null;
      }).filter(Boolean).sort((a,b)=>a.g-b.g);
    }
    return [];
  }
  function normalizeCompareArray(arr){
    if (!Array.isArray(arr)) return [];
    return arr.map(p=>{
      const id = p.id ?? p.key ?? p.slug;
      const label = p.label ?? p.name ?? p.title ?? id;
      const series = normalizeSeries(p.series ?? p.points ?? p.data);
      return (id && label && series.length) ? { id, label, series } : null;
    }).filter(Boolean);
  }
  let compAll      = normalizeCompareArray(await loadFirst(compAllCandidates));
  let compCatchers = normalizeCompareArray(await loadFirst(compCatsCandidates));
  let compRaleigh  = normalizeCompareArray(await loadFirst(raleighCandidates)); // optional, generated by script

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

    const gnum = d.team_game_number ?? d.game_number ?? d.team_game_num ?? d.game_no ?? d.Gtm ?? d['Tm#'] ?? d['Gm#'] ?? d.G;

    return {
      game_date: gd && !isNaN(gd) ? gd : null,
      team_game_number: (gnum != null ? Number(gnum) : null),
      game_pk: (d.game_pk != null ? Number(d.game_pk) : null),
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

  // ---------- Fallback: hydrate team_game_number via MLB schedule if missing ----------
  async function ensureTeamGameNumbers(list){
    const have = list.filter(r => Number.isFinite(r.team_game_number)).length;
    if (have >= Math.max(1, Math.floor(list.length * 0.5))) return;
    const year = list[0]?.game_date?.getFullYear?.() ?? new Date().getFullYear();
    const TEAM_ID = 136; // Mariners
    const schedUrl = `https://statsapi.mlb.com/api/v1/schedule?teamId=${TEAM_ID}&season=${year}&gameType=R`;
    try{
      const r = await fetch(schedUrl, { cache:'no-store' });
      if (!r.ok) return;
      const j = await r.json();
      const games = [];
      (j.dates||[]).forEach(d=> (d.games||[]).forEach(g=> games.push(g)));
      games.sort((a,b)=> new Date(a.gameDate) - new Date(b.gameDate));
      const map = new Map();
      games.forEach((g,i)=> map.set(Number(g.gamePk), i+1));
      list.forEach(row=>{
        if (!Number.isFinite(row.team_game_number) && Number.isFinite(row.game_pk)) {
          const n = map.get(Number(row.game_pk));
          if (n) row.team_game_number = n;
        }
      });
      console.log('[pace] hydrated team_game_number for', list.filter(r=>Number.isFinite(r.team_game_number)).length, 'of', list.length);
    }catch(e){ console.warn('[pace] schedule hydrate failed', e); }
  }
  await ensureTeamGameNumbers(rows);

  // --- Cap Historical Pace at games already on the schedule (not 162) ---
  let capG = 162;
  async function computeCurrentSeasonGameCap(year){
    try{
      const r = await fetch(`https://statsapi.mlb.com/api/v1/schedule?teamId=136&season=${year}&sportId=1&gameType=R`, { cache:'no-store' });
      if(!r.ok) return;
      const j = await r.json();
      const games = [];
      (j.dates||[]).forEach(d=> (d.games||[]).forEach(g=> games.push(g)));
      games.sort((a,b)=> new Date(a.gameDate)-new Date(b.gameDate));
      const now = new Date();
      let n = 0;
      for (const g of games) if (new Date(g.gameDate) <= now) n += 1;
      capG = Math.min(n, 162);
      console.log('[pace] capG (games to date):', capG);
    }catch(e){ console.warn('[pace] capG fetch failed', e); }
  }
  const year = rows[0]?.game_date?.getFullYear?.() ?? new Date().getFullYear();
  await computeCurrentSeasonGameCap(year);

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

  // -------- Chart setup (Historical Pace, Date, Distance) --------
  const ctx = document.getElementById('hrChart').getContext('2d');
  let chart;
  let mode = 'date'; // default
  let currentVenue = '__ALL__';

  // Elements & state
  const btnPace = document.getElementById('mode-pace');
  const btnDate = document.getElementById('mode-date');
  const btnDist = document.getElementById('mode-dist');
  const groupTabs = document.getElementById('groupTabs');
  const picker = document.getElementById('playerPicker');
  const pickerDyn = document.getElementById('playerDynamic');
  const rangeQuick = document.getElementById('rangeQuick');
  const resetZoomBtn = document.getElementById('resetZoom');

  const tblLogBtn  = document.getElementById('tblLogBtn');
  const tblPaceBtn = document.getElementById('tblPaceBtn');
  const logWrap    = document.getElementById('logWrap');
  const paceWrap   = document.getElementById('paceWrap');
  const filtersBar = document.getElementById('tableFilters');

  let group = 'all'; // 'all' | 'catchers'
  const DEFAULT_COMPARE_ALL  = ['ruth_1927','maris_1961','bonds_2001','mcgwire_1998','sosa_1998','judge_2022','griffey_1998','bench_1970'];
  const DEFAULT_COMPARE_CATS = ['bench_1970','campanella_1953','lopez_2003','hundley_1996','piazza_1999'];
  const MAX_COMPARE_DEFAULT = 4;
  let selectedPlayers = new Set(['raleigh', ...DEFAULT_COMPARE_ALL.slice(0, MAX_COMPARE_DEFAULT)]);

  function currentGroupPlayers(){
    if (group === 'catchers') return Array.isArray(compCatchers) ? compCatchers : [];
    return Array.isArray(compAll) ? compAll : [];
  }

  // Cumulative by Date
  function seriesByDate() {
    return ascAll.map((r,i)=>({x:r.game_date,y:i+1,venue:r.venue_name,opp:r.opp}));
  }

  // Distance list (optional venue filter)
  function seriesByDistance(v) {
    let arr = rows.filter(r=>r.dist!=null);
    if (v && v!=='__ALL__') arr = arr.filter(r=>r.venue_name===v);
    arr.sort((a,b)=> b.dist - a.dist);
    return arr;
  }

  // Raleigh series capped to games-to-date
  function raleighSeriesByGame() {
    const cap = Math.max(1, Math.min(capG || 162, 162));

    // Prefer dedicated JSON; clip to capG
    if (Array.isArray(compRaleigh) && compRaleigh.length && compRaleigh[0].series?.length) {
      return compRaleigh[0].series
        .map(d => ({ g: Number(d.g ?? d.x), cum: Number(d.cum ?? d.y) }))
        .filter(pt => Number.isFinite(pt.g) && pt.g <= cap)
        .sort((a,b)=>a.g-b.g);
    }

    // Fallback: build from HR rows (carry cumulative through capG)
    const pts = rows
      .filter(r => Number.isFinite(r.team_game_number))
      .sort((a,b) => a.team_game_number - b.team_game_number);

    const byG = new Map();
    pts.forEach(r => byG.set(r.team_game_number, (byG.get(r.team_game_number) || 0) + 1));

    let cum = 0, series = [];
    for (let g=1; g<=cap; g++){
      if (byG.has(g)) cum += byG.get(g);
      series.push({ g, cum });
    }
    return series;
  }

  // Month tick helper for Date mode
  function monthBoundsAndTicks(dataset) {
    if (!dataset.length) return {};
    const first = new Date(dataset[0].x);
    const last  = new Date(dataset[dataset.length - 1].x);
    const start = new Date(first.getFullYear(), first.getMonth(), 1);
    const end   = new Date(last.getFullYear(),  last.getMonth() + 1, 0);
    const ticks = [];
    const cur = new Date(start);
    while (cur <= end) { ticks.push(new Date(cur)); cur.setMonth(cur.getMonth() + 1); cur.setDate(1); }
    return { start, end, ticks };
  }

  // ----- Player picker UI (includes Cal first) -----
  function buildPlayerPickerUI(){
    pickerDyn.innerHTML = '';

    // Cal toggle first
    const lab = document.createElement('label');
    lab.className = 'chip';
    lab.style.cssText = 'gap:.4rem; display:inline-flex; align-items:center;';
    lab.innerHTML = `<input type="checkbox" value="raleigh"> Cal Raleigh — current season`;
    const input = lab.querySelector('input');
    input.checked = selectedPlayers.has('raleigh');
    input.addEventListener('change', e=>{
      if (e.target.checked) selectedPlayers.add('raleigh'); else selectedPlayers.delete('raleigh');
      renderChart(); buildPaceTable(); updatePaceHeaderSortClasses();
    });
    pickerDyn.appendChild(lab);

    // Then the rest
    const arr = currentGroupPlayers().slice();
    // prefer the first few defaults in order
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
      const inp = label.querySelector('input');
      inp.checked = selectedPlayers.has(id);
      inp.addEventListener('change', e => {
        if (e.target.checked) selectedPlayers.add(id); else selectedPlayers.delete(id);
        renderChart(); buildPaceTable(); updatePaceHeaderSortClasses();
      });
      pickerDyn.appendChild(label);
    });
  }

  // Zoom config (only effective if plugin loaded)
  function zoomOptions(){
    return {
      zoom: { wheel: { enabled: true }, pinch: { enabled: true }, drag: { enabled: true }, mode: 'x' },
      pan:  { enabled: true, modifierKey: 'shift', mode: 'xy' },
      limits: { x: { min: 1, max: 162 } }
    };
  }

  function renderChart() {
    if (chart) chart.destroy();

    // HISTORICAL PACE (by team game #)
    if (mode === 'pace') {
      const datasets = [];

      // Cal Raleigh
      if (selectedPlayers.has('raleigh')) {
        const rs = raleighSeriesByGame();
        if (rs && rs.length) {
          datasets.push({
            label: 'Cal Raleigh — current season',
            data: rs.map(d => ({x:d.g, y:d.cum})),
            parsing: false, stepped: true, pointRadius: 0, tension: 0, borderWidth: 2.5
          });
        }
      }

      // Comparison lines
      const compareArr = currentGroupPlayers();
      compareArr.forEach(p => {
        if (!selectedPlayers.has(p.id)) return;
        const s = (p.series || []).map(d => ({x:d.g, y:d.cum}));
        if (!s.length) return;
        datasets.push({
          label: p.label,
          data: s,
          parsing: false, stepped: true, pointRadius: 0, tension: 0, borderWidth: 2
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
            x: { type: 'linear', min: 1, max: 162,
                 ticks: { stepSize: 10, callback: v => v },
                 title: { display: true, text: 'Game #' } },
            y: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: 'Cumulative HR' } }
          },
          plugins: {
            legend: { display: true },
            title: { display: true, text: group==='catchers' ? 'Historical Pace — Catchers' : 'Historical Pace — All hitters' },
            tooltip: {
              intersect: false, mode: 'nearest',
              callbacks: { title: items => `Game ${items[0].parsed.x}`, label: c => `${c.dataset.label}: ${c.parsed.y} HR` }
            },
            zoom: zoomOptions()
          },
          elements: { line: { borderWidth: 2 } }
        }
      });
      return;
    }

    // DATE mode
    if (mode === 'date') {
      const pts = seriesByDate();
      const { start, end, ticks } = monthBoundsAndTicks(pts);

      chart = new Chart(ctx, {
        type: 'line',
        data: { labels: ticks || [], datasets: [{
          label: 'Cumulative HR',
          data: pts, parsing: false, stepped: true, tension: 0, pointRadius: 1.5, fill: false, borderWidth: 2.5
        }]},
        options: {
          responsive: true, maintainAspectRatio: false, parsing: false,
          scales: {
            x: { type: 'time', time: { unit: 'month', displayFormats: { month: 'MMM' } },
                 min: start, max: end, ticks: { autoSkip: false, maxRotation: 0 } },
            y: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: 'Cumulative HR' } }
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              intersect: false, mode: 'nearest',
              callbacks: {
                label: c => {
                  const d = c.raw; const n = c.parsed.y; const date = new Date(d.x).toLocaleDateString();
                  return `#${n} on ${date} — ${d.venue || 'Unknown park'} vs ${d.opp || '?'}`;
                }
              }
            },
            zoom: zoomOptions()
          },
          elements: { line: { borderWidth: 2 } }
        }
      });
      return;
    }

    // DISTANCE mode
    const arr = seriesByDistance(currentVenue);
    chart = new Chart(ctx, {
      type: 'bar',
      data: { labels: arr.map((r,i)=>`${i+1}. ${r.game_date.toLocaleDateString()} — ${r.venue_name}`),
              datasets: [{ data: arr.map(r=>r.dist) }] },
      options: {
        responsive: true, maintainAspectRatio: false,
        scales: { x: { display: false }, y: { beginAtZero: true, title: { display: true, text: 'Feet' } } },
        plugins: {
          legend: { display: false },
          title: { display: true, text: `Home Runs by Distance (${currentVenue === '__ALL__' ? 'All Parks' : currentVenue})` },
          tooltip: {
            callbacks: {
              title: (items) => { const i = items[0].dataIndex; const r = arr[i]; return `${r.game_date.toLocaleDateString()} — ${r.venue_name}`; },
              label: (item) => `${Math.round(item.raw)} ft`
            }
          },
          zoom: zoomOptions()
        }
      }
    });
  }

  // -------- Game Log table --------
  const tbody=document.querySelector('#hrTable tbody');
  let shown=0; const BTN_BATCH=10;
  function fmt(n,d=0){return(n==null||isNaN(n))?'—':Number(n).toFixed(d);}
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

  // -------- Pace Stats table (sortable) --------
  const checkpoints = [10,20,50,100,150,162];
  const paceBody = document.querySelector('#paceTable tbody');

  // Sorting state (default: Pace desc)
  let paceSort = { key: 'pace', dir: 'desc' };  // dir: 'desc' | 'asc'
  function paceSortValue(row, key){
    switch((key||'').toLowerCase()){
      case 'label': return String(row.label || '').toLowerCase();
      case 'g':     return Number(row.G)    || 0;
      case 'hr':    return Number(row.HR)   || 0;
      case 'pace':  return Number(row.pace) || 0;
      case 'g10':   return Number(row.checks?.[0]) || 0;
      case 'g20':   return Number(row.checks?.[1]) || 0;
      case 'g50':   return Number(row.checks?.[2]) || 0;
      case 'g100':  return Number(row.checks?.[3]) || 0;
      case 'g150':  return Number(row.checks?.[4]) || 0;
      case 'g162':  return Number(row.checks?.[5]) || 0;
      default:      return 0;
    }
  }
  function applyPaceSort(rowsArr){
    const { key, dir } = paceSort;
    if (!key) return rowsArr;
    const f = (dir === 'asc') ? 1 : -1;
    return rowsArr.slice().sort((a,b)=>{
      const va = paceSortValue(a, key);
      const vb = paceSortValue(b, key);
      if (va < vb) return -1 * f;
      if (va > vb) return  1 * f;
      const la = String(a.label||'').toLowerCase();
      const lb = String(b.label||'').toLowerCase();
      if (la < lb) return -1;
      if (la > lb) return  1;
      return 0;
    });
  }

  function valueAt(series, G){
    let v=0;
    for (let i=0;i<series.length;i++){
      const g = series[i].g ?? series[i].x, y = series[i].cum ?? series[i].y;
      if (g<=G) v=y; else break;
    }
    return v;
  }
  function raleighSeriesRaw(){
    const s = raleighSeriesByGame(); return s ? s : [];
  }
  function selectedCompareSeries(){
    const arr = currentGroupPlayers().filter(p=>selectedPlayers.has(p.id));
    return arr.map(p=>({ id:p.id, label:p.label, series: (p.series||[])}));
  }
  function buildPaceTable(){
    paceBody.innerHTML='';
    const rowsOut = [];

    // Cal row uses capG for "Through G"
    const rSeries = raleighSeriesRaw();
    if (rSeries.length){
      const HR = rSeries[rSeries.length-1].cum;
      const G  = capG || rSeries[rSeries.length-1].g;
      const pace = G>0 ? (HR*162/G) : HR;
      rowsOut.push({ label: 'Cal Raleigh — current season', G, HR, pace, checks: checkpoints.map(cp=>valueAt(rSeries, cp)) });
    }

    selectedCompareSeries().forEach(p=>{
      const s = normalizeSeries(p.series);
      if (!s.length) return;
      const G = s[s.length-1].g, HR = s[s.length-1].cum;
      const pace = G>0 ? (HR*162/G) : HR;
      rowsOut.push({ label: p.label, G, HR, pace, checks: checkpoints.map(cp=>valueAt(s, cp)) });
    });

    // Apply Search filter to Pace Stats (by player label)
    const q = (document.getElementById('fText')?.value || '').trim().toLowerCase();
    const filtered = q ? rowsOut.filter(r => r.label.toLowerCase().includes(q)) : rowsOut;

    // Sort after filtering
    const sorted = applyPaceSort(filtered);

    // Render
    sorted.forEach(r=>{
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${r.label}</td><td>${r.G}</td><td>${r.HR}</td><td>${fmt(r.pace,1)}</td>` +
        checkpoints.map((cp,i)=>`<td>${r.checks[i]}</td>`).join('');
      paceBody.appendChild(tr);
    });
  }

  // Clickable header sorting for Pace Stats
  const paceHead = document.querySelector('#paceTable thead');
  const paceHeaderCells = paceHead ? paceHead.querySelectorAll('th.sortable') : [];
  function updatePaceHeaderSortClasses(){
    paceHeaderCells.forEach(th=>{
      th.classList.remove('sort-asc','sort-desc');
      if (th.dataset.sort && th.dataset.sort.toLowerCase() === paceSort.key){
        th.classList.add(paceSort.dir === 'asc' ? 'sort-asc' : 'sort-desc');
      }
    });
  }
  paceHeaderCells.forEach(th=>{
    th.addEventListener('click', ()=>{
      const k = (th.dataset.sort || '').toLowerCase();
      if (!k) return;
      if (paceSort.key === k){
        paceSort.dir = (paceSort.dir === 'desc') ? 'asc' : 'desc';
      } else {
        paceSort.key = k;
        paceSort.dir = 'desc';
      }
      updatePaceHeaderSortClasses();
      buildPaceTable();
    });
  });
  updatePaceHeaderSortClasses();

  // -------- Table Filters --------
  const fText    = document.getElementById('fText');
  const fFrom    = document.getElementById('fFrom');
  const fTo      = document.getElementById('fTo');
  const fMinDist = document.getElementById('fMinDist');
  const fMaxDist = document.getElementById('fMaxDist');
  const fClear   = document.getElementById('fClear');

  function applyTableFilters(baseRows){
    let out = baseRows;

    const q = (fText?.value || '').trim().toLowerCase();
    if (q) {
      out = out.filter(r => {
        const fields = [r.opp, r.venue_name, r.pitcher].map(v => String(v||'').toLowerCase());
        return fields.some(v => v.includes(q));
      });
    }

    const from = fFrom?.value ? new Date(fFrom.value) : null;
    const to   = fTo?.value   ? new Date(fTo.value)   : null;
    if (from) out = out.filter(r => r.game_date >= from);
    if (to)   out = out.filter(r => r.game_date <= to);

    const minD = fMinDist?.value ? Number(fMinDist.value) : null;
    const maxD = fMaxDist?.value ? Number(fMaxDist.value) : null;
    if (Number.isFinite(minD)) out = out.filter(r => (r.dist ?? -Infinity) >= minD);
    if (Number.isFinite(maxD)) out = out.filter(r => (r.dist ?? Infinity)  <= maxD);

    return out;
  }

  function currentTableData(){
    let base = (currentVenue==='__ALL__')
      ? descAll
      : rows.filter(r=>r.venue_name===currentVenue).sort((a,b)=>b.game_date-a.game_date);
    return applyTableFilters(base);
  }

  [fText, fFrom, fTo, fMinDist, fMaxDist].forEach(el=>{
    el?.addEventListener('input', ()=>{
      // Update both tables if visible
      renderRows(currentTableData(), true);
      buildPaceTable();
      updatePaceHeaderSortClasses();
    });
  });
  fClear?.addEventListener('click', ()=>{
    if (fText)    fText.value = '';
    if (fFrom)    fFrom.value = '';
    if (fTo)      fTo.value = '';
    if (fMinDist) fMinDist.value = '';
    if (fMaxDist) fMaxDist.value = '';
    renderRows(currentTableData(), true);
    buildPaceTable();
    updatePaceHeaderSortClasses();
  });

  // -------- Controls --------
  function updateBigNumber(){
    if(mode==='distance'&&currentVenue!=='__ALL__'){countEl.textContent=`${seriesByDistance(currentVenue).length} HR`;}
    else{countEl.textContent=`${seasonTotal} HR`;}
  }

  function activatePaceTable(){
    tblPaceBtn.classList.add('active'); tblPaceBtn.setAttribute('aria-pressed','true');
    tblLogBtn.classList.remove('active'); tblLogBtn.setAttribute('aria-pressed','false');
    logWrap.style.display='none'; paceWrap.style.display='block';
    document.getElementById('showMore').style.display='none';
    filtersBar.style.display='flex';          // keep filters visible for Pace Stats (search filters players)
    buildPaceTable();
    updatePaceHeaderSortClasses();
  }

  function setMode(m){
    mode=m;
    const isPace = mode==='pace';
    const isDate = mode==='date';
    const isDist = mode==='distance';

    btnPace.classList.toggle('active',isPace);
    btnDate.classList.toggle('active',isDate);
    btnDist.classList.toggle('active',isDist);

    btnPace.setAttribute('aria-pressed',isPace);
    btnDate.setAttribute('aria-pressed',isDate);
    btnDist.setAttribute('aria-pressed',isDist);

    // Venue filter only in Distance; tabs/picker/range only in Historical Pace
    venueWrap.style.display = isDist ? 'inline-flex' : 'none';
    groupTabs.style.display  = isPace ? 'inline-flex' : 'none';
    picker.style.display     = isPace ? 'inline-flex' : 'none';
    rangeQuick.style.display = isPace ? 'inline-flex' : 'none';

    if (!isDist){ currentVenue='__ALL__'; sel.value='__ALL__'; }

    if (isPace){
      // Default to 4 hitters + Raleigh
      const base = (group==='catchers' ? DEFAULT_COMPARE_CATS : DEFAULT_COMPARE_ALL).slice(0, MAX_COMPARE_DEFAULT);
      selectedPlayers = new Set(['raleigh', ...base]);
      buildPlayerPickerUI();
      activatePaceTable(); // flip on Pace Stats automatically
    }

    renderChart();
    renderRows(currentTableData(), true);
    buildPaceTable();
    updatePaceHeaderSortClasses();
    updateBigNumber();
  }

  btnPace.addEventListener('click',()=>setMode('pace'));
  btnDate.addEventListener('click',()=>setMode('date'));
  btnDist.addEventListener('click',()=>setMode('distance'));

  groupTabs.addEventListener('click', (e) => {
    const b = e.target.closest('button.tab'); if (!b) return;
    group = b.dataset.group; // 'all' | 'catchers'
    [...groupTabs.querySelectorAll('.tab')].forEach(btn=>{
      const on = btn.dataset.group===group;
      btn.classList.toggle('active', on);
      btn.setAttribute('aria-pressed', on);
    });
    // Reset to 4 hitters + Raleigh when switching groups
    const base = (group==='catchers' ? DEFAULT_COMPARE_CATS : DEFAULT_COMPARE_ALL).slice(0, MAX_COMPARE_DEFAULT);
    selectedPlayers = new Set(['raleigh', ...base]);
    buildPlayerPickerUI();
    renderChart(); buildPaceTable(); updatePaceHeaderSortClasses();
  });

  sel.addEventListener('change',e=>{
    currentVenue=e.target.value;
    if(mode==='distance') renderChart();
    renderRows(currentTableData(), true);
    updateBigNumber();
  });
  document.getElementById('showMore').addEventListener('click',()=>renderRows(currentTableData(),false));

  // Table subtabs
  tblLogBtn.addEventListener('click', ()=>{
    tblLogBtn.classList.add('active'); tblLogBtn.setAttribute('aria-pressed','true');
    tblPaceBtn.classList.remove('active'); tblPaceBtn.setAttribute('aria-pressed','false');
    logWrap.style.display='block'; paceWrap.style.display='none';
    document.getElementById('showMore').style.display='inline-block';
    filtersBar.style.display='flex';
  });
  tblPaceBtn.addEventListener('click', ()=>{ activatePaceTable(); });

  // Quick range buttons + reset zoom (pace mode)
  document.getElementById('rangeQuick').addEventListener('click', (e)=>{
    const b = e.target.closest('button.qr'); if (!b || !chart) return;
    const r = b.dataset.range;
    if (r === 'full') {
      if (typeof chart.resetZoom === 'function') chart.resetZoom();
      chart.options.scales.x.min = 1; chart.options.scales.x.max = 162; chart.update();
      return;
    }
    const parts = r.split('-').map(n=>Number(n));
    const a = parts[0], bmax = parts[1];
    chart.options.scales.x.min = a;
    chart.options.scales.x.max = bmax;
    chart.update();
  });
  document.getElementById('resetZoom').addEventListener('click', ()=>{
    if (!chart) return;
    if (typeof chart.resetZoom === 'function') chart.resetZoom();
    chart.options.scales.x.min = 1;
    chart.options.scales.x.max = 162;
    chart.update();
  });

  // Initial paint
  setMode('date');                   // change to 'pace' if you want Historical Pace by default
  renderRows(currentTableData(),true);
  buildPaceTable();
  updatePaceHeaderSortClasses();
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
.controls .modes{ display:flex; gap:.5rem; flex-wrap:wrap; align-items:center; }
.controls .venue select{
  margin-left:.4rem; padding:.4rem .6rem;
  border:1px solid var(--border, #c9c9c9); border-radius:8px;
  background: var(--surface, #fff); color: var(--text, #111);
}

/* Tabs & player picker (Historical Pace mode) */
.controls .tabs { display:flex; gap:.5rem; align-items:center; }
.controls .tabs .tab.active{
  background: var(--chip-active-bg, #e6f0ff);
  border-color: var(--chip-active-border, #8ab4ff);
}
.controls .players{ display:flex; gap:.5rem; flex-wrap:wrap; align-items:center; }
.quickrange{ display:flex; gap:.5rem; flex-wrap:wrap; align-items:center; }

/* Table subtabs */
.subtabs{ display:flex; gap:.5rem; align-items:center; margin:.5rem 0; }

/* Filters */
.filters{
  display:flex; gap:.5rem; flex-wrap:wrap; align-items:center;
  margin:.5rem 0 .5rem;
}
.filters input[type="search"],
.filters input[type="date"],
.filters input[type="number"]{
  padding:.35rem .5rem; border:1px solid var(--border,#c9c9c9); border-radius:8px;
  background: var(--surface,#fff); color: var(--text,#111);
}
@media (prefers-color-scheme: dark){
  .filters input{ background: var(--surface); color: var(--text); border-color: var(--border); }
}

/* High-contrast chips */
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

/* Sortable Pace Stats headers */
#paceTable th.sortable{ cursor: pointer; user-select:none; white-space:nowrap; }
#paceTable th.sortable.sort-desc::after{ content:" ▼"; opacity:.7; }
#paceTable th.sortable.sort-asc::after{ content:" ▲"; opacity:.7; }

/* Dark mode */
@media (prefers-color-scheme: dark){
  :root{
    --text: #e8e8e8;
    --surface: #151515;
    --border: rgba(255,255,255,.22);

    --chip-bg: rgba(255,255,255,.10);
    --chip-fg: #e8e8e8;
    --chip-border: rgba(255,255,255,.32);
    --chip-active-bg: rgba(59,130,246,.28);
    --chip-active-border: rgba(59,130,246,.65);
    --chip-focus: #93c5fd;
  }
  .controls .venue select{
    background: var(--surface);
    color: var(--text);
    border-color: var(--border);
  }
}

/* Chart sizing – bigger for readability */
.chart-wrap{ width:100%; height: clamp(480px, 70vh, 680px); margin:.5rem 0 1rem; }
#hrChart{ display:block; width:100% !important; height:100% !important; max-width:none; }

/* Tables */
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

