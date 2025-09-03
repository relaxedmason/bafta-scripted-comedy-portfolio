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

        <!-- BAFTA 10 Years -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/bafta_scripted_comedy_visualization.png' | relative_url }}"
            alt="BAFTA Scripted Comedy visualization"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">The Last Ten Years of the BAFTA Scripted Comedy Awards</h3>
          <p class="card__blurb">Visual record of nominees and winners from the most recent decade.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/bafta-comedy-awards/winners-nominees/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <!-- Peep Show -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/peep_show_bafta_thumbnail.jpg' | relative_url }}"
            alt="Peep Show BAFTA thumbnail"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">Peep Show’s BAFTA Record</h3>
          <p class="card__blurb">How the series performed at the BAFTAs across nominations and wins.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/bafta-comedy-awards/peep-show/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <!-- Controversial Wins -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/bafta_top5.png' | relative_url }}"
            alt="BAFTA controversial wins thumbnail"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">Five Controversial BAFTA Scripted Comedy Wins</h3>
          <p class="card__blurb">Highlighting outliers where results diverged from ratings and consensus.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/bafta-comedy-awards/rating-check/' | relative_url }}">View project</a></li>
          </ul>
        </article>

      </div>
    </div>

    <!-- Sports tab -->
    <div class="tab-content" id="sports" role="tabpanel" aria-labelledby="tab-sports-label" hidden>
      <div class="cards">

        <!-- Depth Charts -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/sports/bavasi/depth-chart/mariners_2003_depth_chart_final_final.png' | relative_url }}"
            alt="Mariners depth chart visualization"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">Seattle Mariners Depth Charts, 2003–2008</h3>
          <p class="card__blurb">Season-by-season visuals of roster construction during the Bavasi era.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/baseball/bavasi/depth-chart/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <!-- Home Run Leaders -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/sports/mariners/top_10_home_run_safeco_field.png' | relative_url }}"
            alt="Safeco Field longest home runs"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">Safeco Field: Home Run Distance Leaders</h3>
          <p class="card__blurb">Top-10 ranking of the park’s most powerful blasts.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/top-10-home-runs-at-Safeco-Field/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <!-- Suarez vs Williamson -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/sports/mariners/suarez_williamson_desktop.png' | relative_url }}"
            alt="Suarez vs Williamson comparison"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">Suárez vs. Williamson — First Half 2025</h3>
          <p class="card__blurb">Side-by-side stat comparison across wRC+, DRS, BsR, and WAR.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/baseball/mariners/suarez-vs-williamson/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <!-- Guillen Trade -->
        <article class="card">
          <img
            class="card__thumb"
            src="{{ '/assets/images/sports/mariners/guillen_vs_mariners_weighted_FINAL.png' | relative_url }}"
            alt="Carlos Guillen trade visualization"
            width="1280" height="720" loading="lazy" decoding="async">
          <h3 class="card__title">The Carlos Guillén Trade</h3>
          <p class="card__blurb">Assessing the downstream outcomes and WAR impact of the deal for Seattle.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/baseball/bavasi/carlos-guillen-trade/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <!-- Venezuelan WAR -->
        <article class="card">
          <picture>
            <source
              srcset="{{ '/assets/images/sports/mariners/Top_10_MLB_Team_WAR_Venezuela_dark.png' | relative_url }}"
              media="(prefers-color-scheme: dark)">
            <img
              class="card__thumb"
              src="{{ '/assets/images/sports/mariners/top_10_MLB_Team_WAR_Venezuela_light.png' | relative_url }}"
              alt="Venezuelan WAR visualization"
              width="1280" height="720" loading="lazy" decoding="async">
          </picture>
          <h3 class="card__title">Venezuelan WAR Contributions to the Mariners</h3>
          <p class="card__blurb">Quantifying the franchise-level impact of Venezuelan players over time.</p>
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
