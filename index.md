---
layout: default
title: Mason Colborn — Data Analyst Portfolio
description: SQL • Python • APIs • Data Visualization
---

<header class="hero">
  <h1 id="data-analyst-portfolio">Data Analyst Portfolio</h1>
  <p class="subtitle">SQL • Python • APIs • Data Visualization</p>
</header>

<section id="projects" aria-labelledby="projects-title">
  <h2 id="projects-title" class="section__title">Projects</h2>

  <div class="tabs" role="tablist" aria-label="Project categories">
    <!-- Tab selectors -->
    <input type="radio" name="tab" id="tab-tv" class="tabs__input" checked>
    <label for="tab-tv" id="tab-tv-label" class="tabs__label" role="tab" aria-controls="tv" aria-selected="true" tabindex="0">TV</label>

    <input type="radio" name="tab" id="tab-sports" class="tabs__input">
    <label for="tab-sports" id="tab-sports-label" class="tabs__label" role="tab" aria-controls="sports" aria-selected="false" tabindex="-1">Sports</label>

    <!-- TV tab -->
    <div class="tab-content" id="tv" role="tabpanel" aria-labelledby="tab-tv-label">
      <div class="cards">

        <!-- BAFTA Scripted Comedy Awards -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/bafta_scripted_comedy_visualization.png' | relative_url }}"
            alt="BAFTA Scripted Comedy — winners and nominees visualization"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">BAFTA Scripted Comedy Awards</h3>
          <p class="card__blurb">IMDb/TMDb enrichment to analyze BAFTA nominations vs. wins (2016–2025).</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/bafta-comedy-awards/winners-nominees/' | relative_url }}">Winners &amp; Nominees (2016–2025)</a></li>
            <li><a class="link" href="{{ '/bafta-comedy-awards/peep-show/'         | relative_url }}">Peep Show’s Record</a></li>
            <li><a class="link" href="{{ '/bafta-comedy-awards/rating-check/'      | relative_url }}">Top 5 Least Deserving Wins</a></li>
          </ul>
        </article>

        <!-- Optional: you can swap the image above to this Peep Show thumb if you prefer that look -->
        <!--
        <img class="card__thumb"
             src="{{ '/assets/images/peep_show_bafta_thumbnail.jpg' | relative_url }}"
             alt="Peep Show at the BAFTAs thumbnail"
             width="1280" height="720" loading="lazy" decoding="async">
        -->
        <!--
        Or use the 'Least deserving wins' visual:
        <img class="card__thumb"
             src="{{ '/assets/images/bafta_top5.png' | relative_url }}"
             alt="Top 5 least deserving BAFTA winners thumbnail"
             width="1280" height="720" loading="lazy" decoding="async">
        -->

      </div>
    </div>

    <!-- Sports tab -->
    <div class="tab-content" id="sports" role="tabpanel" aria-labelledby="tab-sports-label" hidden>
      <div class="cards">

        <!-- Mariners Depth Charts (2003–2008) -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/sports/bavasi/depth-chart/mariners_2003_depth_chart_final_final.png' | relative_url }}"
            alt="Mariners 2003 depth chart visualization"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">Mariners Depth Charts (2003–2008)</h3>
          <p class="card__blurb">Visual depth charts and roster churn during the Bavasi era.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/baseball/bavasi/depth-chart/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <!-- Longest HRs at Safeco Field -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/sports/mariners/top_10_home_run_safeco_field.png' | relative_url }}"
            alt="Top 10 longest home runs at Safeco Field visualization"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">The 10 Longest Home Runs at Safeco Field</h3>
          <p class="card__blurb">Distance leaderboard with context and visuals.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/top-10-home-runs-at-Safeco-Field/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <!-- Suárez vs. Williamson — 2025 First Half -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/sports/mariners/suarez_williamson_desktop.png' | relative_url }}"
            alt="Suárez vs. Williamson 2025 first half comparison"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">Suárez vs. Williamson — 2025 First Half</h3>
          <p class="card__blurb">Compact stat comparison (wRC+, DRS, BsR, WAR) with clear layout.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/baseball/mariners/suarez-vs-williamson/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <!-- Carlos Guillén Trade -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/sports/mariners/guillen_vs_mariners_weighted_FINAL.png' | relative_url }}"
            alt="Carlos Guillén trade impact visualization"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">The Carlos Guillén Trade</h3>
          <p class="card__blurb">Trade tree + outcomes and WAR impact for Seattle.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/baseball/bavasi/carlos-guillen-trade/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <!-- Venezuelan WAR — prefers-color-scheme switch -->
        <article class="card">
          <picture>
            <!-- Prefer dark image if user is in dark mode -->
            <source
              srcset="{{ '/assets/images/sports/mariners/Top_10_MLB_Team_WAR_Venezuela_dark.png' | relative_url }}"
              media="(prefers-color-scheme: dark)">
            <!-- Light image otherwise -->
            <img
              class="card__thumb"
              src="{{ '/assets/images/sports/mariners/top_10_MLB_Team_WAR_Venezuela_light.png' | relative_url }}"
              alt="Top 10 MLB Team WAR (Venezuelan players) visualization"
              width="1280" height="720" loading="lazy" decoding="async">
          </picture>
          <h3 class="card__title">Venezuelan WAR — Mariners Focus</h3>
          <p class="card__blurb">Contribution by Venezuelan players across Mariners history.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/baseball/mariners/venezuelan-war/' | relative_url }}">View project</a></li>
          </ul>
        </article>

      </div>
    </div>
  </div>
</section>

<section id="contact" aria-labelledby="contact-title">
  <h2 id="contact-title" class="section__title">Connect</h2>
  <nav class="social-links" aria-label="Social and contact">
    <a class="chip" href="mailto:masoncolborn@gmail.com">✉️ Email</a>
    <a class="chip" href="https://twitter.com/relaxedmason">🐦 Twitter</a>
    <a class="chip" href="https://github.com/relaxedmason">💻 GitHub</a>
    <a class="chip" href="{{ '/about/' | relative_url }}">ℹ️ About</a>
  </nav>
</section>
