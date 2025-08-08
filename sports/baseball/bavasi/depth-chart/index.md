---
layout: default
title: Bavasi's Reign of Terror 
permalink: /sports/baseball/bavasi/depth-chart/
---

## - A Journey through the Seattle Mariner's Depth Charts from 2003-2008

Warning!!! Click at your own risk, these images might induce painful baseball memories. 

<input type="range" min="0" max="5" value="0" id="yearSlider" style="width:100%; margin-top: 20px;">

<!-- Year Buttons -->
<div id="yearButtons" style="text-align:center; margin-top: 20px;">
  <button onclick="changeYear(0)">2003</button>
  <button onclick="changeYear(1)">2004</button>
  <button onclick="changeYear(2)">2005</button>
  <button onclick="changeYear(3)">2006</button>
  <button onclick="changeYear(4)">2007</button>
  <button onclick="changeYear(5)">2008</button>
</div>

<!-- Image Display -->
<div id="depthChartContainer" style="text-align:center; margin-top:20px;">
  <img id="depthChartImage" 
       src="/bafta-scripted-comedy-portfolio/assets/images/sports/bavasi/depth-chart/mariners_2003_depth_chart_final_final.png" 
       style="max-width:100%; border: 1px solid #ccc; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
  <p id="yearLabel"><strong>2003</strong></p>
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

  function changeYear(index) {
    const image = document.getElementById("depthChartImage");
    const label = document.getElementById("yearLabel");
    image.src = `/bafta-scripted-comedy-portfolio/assets/images/sports/bavasi/depth-chart/${imageFilenames[index]}`;
    label.innerHTML = `<strong>${yearLabels[index]}</strong>`;
  }
</script>

