---
layout: default
title: Bavasi's Reign of Terror 
permalink: /sports/baseball/bavasi/depth-chart/
---

## A Journey through the Seattle Mariner's Depth Charts from 2003–2008

⚠️ **Warning!!!** Click at your own risk — these images might induce painful baseball memories.

<!-- Navigation Buttons -->
<div style="text-align:center; margin-top: 20px;">
  <button onclick="changeYearBy(-1)" class="nav-button">⟵ Prev</button>
  <button onclick="changeYearBy(1)" class="nav-button">Next ⟶</button>
</div>

<!-- Image Display -->
<div id="depthChartContainer" style="text-align:center; margin-top:20px;">
  <img id="depthChartImage" 
       src="/assets/images/sports/bavasi/depth-chart/mariners_2003_depth_chart_final_final.png" 
       style="max-width:100%; height:auto; border:1px solid #ccc; box-shadow:2px 2px 5px rgba(0,0,0,0.2);">
  <p id="yearLabel"><strong>2003</strong></p>
</div>

<!-- Year Buttons (wrapped for mobile) -->
<div id="yearButtons" style="display:flex; flex-wrap:wrap; justify-content:center; gap:8px; margin-top: 10px;">
  <button class="year-button" onclick="changeYear(0)">2003</button>
  <button class="year-button" onclick="changeYear(1)">2004</button>
  <button class="year-button" onclick="changeYear(2)">2005</button>
  <button class="year-button" onclick="changeYear(3)">2006</button>
  <button class="year-button" onclick="changeYear(4)">2007</button>
  <button class="year-button" onclick="changeYear(5)">2008</button>
</div>

<!-- Script -->
<script>
  const imageFilenames = [
    "mariners_2003_depth_chart_final_final.png",
    "mariners_2004_depth_chart_final.png",
    "mariners_2005_depth_chart_final_final.png",
    "mariners_2006_depth_chart_final.png",
    "mariners_2007_depth_chart_final.png",
    "mariners_2008_depth_chart_final.png"
  ];

  const yearLabels = ["2003", "2004", "2005", "2006", "2007", "2008"];
  let currentIndex = 0;

  function updateChart(index) {
    const image = document.getElementById("depthChartImage");
    const label = document.getElementById("yearLabel");
    image.src = `/assets/images/sports/bavasi/depth-chart/${imageFilenames[index]}`;
    label.innerHTML = `<strong>${yearLabels[index]}</strong>`;
    currentIndex = index;
  }

  function changeYear(index) {
    updateChart(index);
  }

  function changeYearBy(delta) {
    let newIndex = currentIndex + delta;
    if (newIndex < 0) newIndex = 0;
    if (newIndex >= imageFilenames.length) newIndex = imageFilenames.length - 1;
    updateChart(newIndex);
  }
</script>

<!-- Mobile-Friendly Styling -->
<style>
  .nav-button,
  .year-button {
    padding: 10px 16px;
    font-size: 16px;
    margin: 4px;
    border: none;
    background-color: #2c3e50;
    color: white;
    border-radius: 5px;
    cursor: pointer;
  }

  .nav-button:hover,
  .year-button:hover {
    background-color: #34495e;
  }

  @media (max-width: 600px) {
    .nav-button,
    .year-button {
      font-size: 14px;
      padding: 8px 12px;
    }
  }
</style>


