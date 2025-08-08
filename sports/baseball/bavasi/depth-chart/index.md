---
layout: default
title: Bavasi's Reign of Terror 
permalink: /sports/baseball/bavasi/depth-chart/
---

## A Journey through the Seattle Mariner's Depth Charts from 2003–2008

⚠️ **Warning!!!** Click at your own risk — these images might induce painful baseball memories.

<!-- Prev/Next Buttons -->
<div style="text-align:center; margin-top: 20px;">
  <button onclick="changeYearBy(-1)">⟵ Prev</button>
  <button onclick="changeYearBy(1)">Next ⟶</button>
</div>

<!-- Image Display -->
<div id="depthChartContainer" style="text-align:center; margin-top:20px;">
  <img id="depthChartImage" 
       src="/assets/images/sports/bavasi/depth-chart/mariners_2003_depth_chart_final_final.png" 
       style="max-width:100%; height:auto; border: 1px solid #ccc; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); cursor: pointer;"
       onclick="enlargeImage()">
  <p id="yearLabel"><strong>2003 — 93–69</strong></p>
</div>

<!-- Year Buttons -->
<div id="yearButtons" style="text-align:center; margin-top: 10px;">
  <button onclick="changeYear(0)">2003</button>
  <button onclick="changeYear(1)">2004</button>
  <button onclick="changeYear(2)">2005</button>
  <button onclick="changeYear(3)">2006</button>
  <button onclick="changeYear(4)">2007</button>
  <button onclick="changeYear(5)">2008</button>
</div>

<!-- Image Enlarging Modal (Hidden by Default) -->
<div id="modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:1000; text-align:center;">
  <img id="modalImage" src="" style="max-width:90%; max-height:90%; margin-top:40px;" onclick="closeModal()">
</div>

<!-- Scripts -->
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
  const records = ["93–69", "63–99", "69–93", "78–84", "88–74", "61–101"];
  let currentIndex = 0;

  function updateChart(index) {
    const image = document.getElementById("depthChartImage");
    const label = document.getElementById("yearLabel");
    image.src = `/assets/images/sports/bavasi/depth-chart/${imageFilenames[index]}`;
    label.innerHTML = `<strong>${yearLabels[index]} — ${records[index]}</strong>`;
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

  function enlargeImage() {
    const modal = document.getElementById("modal");
    const modalImage = document.getElementById("modalImage");
    modalImage.src = document.getElementById("depthChartImage").src;
    modal.style.display = "block";
  }

  function closeModal() {
    document.getElementById("modal").style.display = "none";
  }
</script>

<style>
  /* Ensure images shrink on small devices */
  #depthChartImage {
    width: 100%;
    height: auto;
  }

  @media (max-width: 600px) {
    button {
      margin: 5px;
      font-size: 16px;
    }
    #yearButtons {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
    }
  }
</style>
