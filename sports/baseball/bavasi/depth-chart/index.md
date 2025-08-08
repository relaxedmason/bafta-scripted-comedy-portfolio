---
layout: default
title: Bavasi's Reign of Terror 
permalink: /sports/baseball/bavasi/depth-chart/
---

## - A Journey through the Seattle Mariner's Depth Charts from 2003-2008

Warning!!! Click at your own risk, this interactive slider might induce painful baseball memories. 

<input type="range" min="0" max="5" value="0" id="yearSlider" style="width:100%; margin-top: 20px;">

<div id="depthChartContainer" style="text-align:center; margin-top:20px;">
  <img id="depthChartImage" 
       src="/assets/images/sports/baseball/bavasi/depth-chart/mariners_2003_depth_chart_final_final.png" 
       style="max-width:100%; border: 1px solid #ccc; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
  <p id="yearLabel"><strong>2003</strong></p>
</div>

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

  const slider = document.getElementById("yearSlider");
  const image = document.getElementById("depthChartImage");
  const label = document.getElementById("yearLabel");

  slider.addEventListener("input", function() {
    const i = parseInt(this.value);
    const filename = imageFilenames[i];
    const year = yearLabels[i];
    image.src = `/assets/images/sports/baseball/bavasi/depth-chart/${filename}`;
    label.innerHTML = `<strong>${year}</strong>`;
  });
</script>
