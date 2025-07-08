-- 1) List of nominees + winners for Best Scripted Comedy, last 10 years
WITH last10 AS (
    -- pick the last 10 award years
    SELECT DISTINCT awardyear
    FROM bafta_comedy_awards
    WHERE awardtitle = 'Best Scripted Comedy'
      AND bafta_status = 'winner'
    ORDER BY awardyear DESC
    OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY
),
nominees AS (
    -- grab all nominees (incl winners) in that time frame
    SELECT
      b.awardyear,
      b.bafta_status,
      b.imdbtitle,
      b.tconst
    FROM bafta_comedy_awards b
    JOIN last10 l
      ON b.awardyear = l.awardyear
    WHERE b.awardtitle = 'Best Scripted Comedy'
),
ratings AS (
    SELECT tconst, averageRating, numVotes
    FROM title_ratings
),
basics AS (
    SELECT tconst, primaryTitle, startYear
    FROM title_basics
),
nom_with_meta AS (
    SELECT
      n.awardyear,
      n.bafta_status,
      b.primaryTitle    AS title,
      b.startYear       AS year_of_release,
      r.averageRating,
      r.numVotes,
      n.tconst
    FROM nominees n
    LEFT JOIN basics b  ON n.tconst = b.tconst
    LEFT JOIN ratings r ON n.tconst = r.tconst
)
SELECT *
FROM nom_with_meta
ORDER BY awardyear DESC
       , CASE WHEN bafta_status = 'winner' THEN 0 ELSE 1 END  -- winner first
       , averageRating   DESC
       , numVotes        DESC;