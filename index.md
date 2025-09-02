---
layout: default
title: Mason Colborn — Data Analyst Portfolio
description: SQL • Python • APIs • Data Visualization
---

<header class="hero" role="banner">
  <h1 class="hero__title" id="data-analyst-portfolio">Data Analyst Portfolio</h1>
  <p class="hero__subtitle">SQL • Python • APIs • Data Visualization</p>
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
        <article class="card">
          <h3 class="card__title">BAFTA Scripted Comedy Awards</h3>
          <ul class="card__list">
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
          <h3 class="card__title">Mariners Projects</h3>
          <ul class="card__list">
            <li><a class="link" href="{{ '/sports/baseball/bavasi/depth-chart/'             | relative_url }}">Bavasi’s Reign of Terror: Mariners Depth Charts (2003–2008)</a></li>
            <li><a class="link" href="{{ '/sports/top-10-home-runs-at-Safeco-Field/'       | relative_url }}">The 10 Longest Home Runs at Safeco Field</a></li>
            <li><a class="link" href="{{ '/sports/baseball/mariners/suarez-vs-williamson/' | relative_url }}">Suárez vs. Williamson — 2025 First Half Comparison</a></li>
            <li><a class="link" href="{{ '/sports/baseball/bavasi/carlos-guillen-trade/'   | relative_url }}">The Carlos Guillén Trade</a></li>
            <li><a class="link" href="{{ '/sports/baseball/mariners/venezuelan-war/'       | relative_url }}">Venezuelan WAR — Mariners Focus</a></li>
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
