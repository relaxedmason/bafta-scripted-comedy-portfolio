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
    <!-- Tab selectors (controls) -->
    <input type="radio" name="tab" id="tab-tv" class="tabs__input" checked>
    <label for="tab-tv" id="tab-tv-label" class="tabs__label" role="tab" aria-controls="tv" aria-selected="true" tabindex="0">TV</label>

    <input type="radio" name="tab" id="tab-sports" class="tabs__input">
    <label for="tab-sports" id="tab-sports-label" class="tabs__label" role="tab" aria-controls="sports" aria-selected="false" tabindex="-1">Sports</label>

    <!-- TV tab -->
    <div class="tab-content" id="tv" role="tabpanel" aria-labelledby="tab-tv-label">
      <div class="cards">
        <article class="card">
          <picture>
            <source srcset="{{ '/assets/img/thumbs/bafta-comedy.webp' | relative_url }}" type="image/webp">
            <img
              class="card__thumb"
              src="{{ '/assets/img/thumbs/bafta-comedy.jpg' | relative_url }}"
              alt="BAFTA Scripted Comedy visuals"
              width="1280" height="720" loading="lazy" decoding="async">
          </picture>
          <h3 class="card__title">BAFTA Scripted Comedy Awards</h3>
          <p class="card__blurb">IMDb/TMDb enrichment to analyze BAFTA nominations vs. wins (2016–2025).</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/bafta-comedy-awards/winners-nominees/' | relative_url }}">Winners &amp; Nominees (2016–2025)</a></li>
            <li><a class="link" href="{{ '/bafta-comedy-awards/peep-show/'         | relative_url }}">Peep Show’s Record</a></li>
            <li><a class="link" href="{{ '/bafta-comedy-awards/rating-check/'      | relative_url }}">Top 5 Least Deserving Wins</a></li>
          </ul>
        </article>
      </div>
    </div>

    <!-- Sports tab -->
    <div class="tab-content" id="sports" role="tabpanel" aria-labelledby="tab-sports-label" hidden>
      <div class="cards">
        <article class="card">
          <picture>
            <source srcset="{{ '/assets/img/thumbs/mariners-depth.webp' | relative_url }}" type="image/webp">
            <img
              class="card__thumb"
              src="{{ '/assets/img/thumbs/mariners-depth.jpg' | relative_url }}"
              alt="Mariners depth chart visual"
              width="1280" height="720" loading="lazy" decoding="async">
          </picture>
          <h3 class="card__title">Mariners Depth Charts (2003–2008)</h3>
          <p class="card__blurb">Visual depth charts and roster churn during the Bavasi era.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/baseball/bavasi/depth-chart/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <article class="card">
          <picture>
            <source srcset="{{ '/assets/img/thumbs/safeco-hr.webp' | relative_url }}" type="image/webp">
            <img
              class="card__thumb"
              src="{{ '/assets/img/thumbs/safeco-hr.jpg' | relative_url }}"
              alt="Home run distance chart"
              width="1280" height="720" loading="lazy" decoding="async">
          </picture>
          <h3 class="card__title">The 10 Longest Home Runs at Safeco Field</h3>
          <p class="card__blurb">Distance leaderboard with context and visuals.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/top-10-home-runs-at-Safeco-Field/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <article class="card">
          <picture>
            <source srcset="{{ '/assets/img/thumbs/suarez-williamson.webp' | relative_url }}" type="image/webp">
            <img
              class="card__thumb"
              src="{{ '/assets/img/thumbs/suarez-williamson.jpg' | relative_url }}"
              alt="Stat comparison layout"
              width="1280" height="720" loading="lazy" decoding="async">
          </picture>
          <h3 class="card__title">Suárez vs. Williamson — 2025 First Half</h3>
          <p class="card__blurb">Compact stat comparison (wRC+, DRS, BsR, WAR) with clear layout.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/baseball/mariners/suarez-vs-williamson/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <article class="card">
          <picture>
            <source srcset="{{ '/assets/img/thumbs/guillen-trade.webp' | relative_url }}" type="image/webp">
            <img
              class="card__thumb"
              src="{{ '/assets/img/thumbs/guillen-trade.jpg' | relative_url }}"
              alt="Trade tree graphic for Carlos Guillén"
              width="1280" height="720" loading="lazy" decoding="async">
          </picture>
          <h3 class="card__title">The Carlos Guillén Trade</h3>
          <p class="card__blurb">Trade tree + outcomes and WAR impact for Seattle.</p>
          <ul class="card__links">
            <li><a class="link" href="{{ '/sports/baseball/bavasi/carlos-guillen-trade/' | relative_url }}">View project</a></li>
          </ul>
        </article>

        <article class="card">
          <picture>
            <source srcset="{{ '/assets/img/thumbs/venezuelan-war.webp' | relative_url }}" type="image/webp">
            <img
              class="card__thumb"
              src="{{ '/assets/img/thumbs/venezuelan-war.jpg' | relative_url }}"
              alt="Venezuelan WAR visualization"
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

