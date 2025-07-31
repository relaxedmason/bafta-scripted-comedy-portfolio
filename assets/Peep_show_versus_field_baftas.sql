WITH peep_show_nominations AS (
  SELECT
    awardyear,
    imdbtitle AS peep_title,
    tconst AS peep_tconst,
    bafta_status AS peep_status
  FROM bafta_comedy_awards
  WHERE imdbtitle = 'Peep Show'
    AND awardtitle = 'Best Scripted Comedy'
),
yearly_winners AS (
  SELECT
    awardyear,
    imdbtitle AS winning_title,
    tconst AS winner_tconst
  FROM bafta_comedy_awards
  WHERE bafta_status = 'winner'
    AND awardtitle = 'Best Scripted Comedy'
)
SELECT 
  n.awardyear,
  n.peep_title,
  n.peep_tconst,
  n.peep_status,
  CASE 
    WHEN n.peep_status = 'winner' THEN '✅ Yes'
    ELSE '❌ No'
  END AS bafta_winner,
  w.winning_title,
  w.winner_tconst
FROM peep_show_nominations n
JOIN yearly_winners w ON n.awardyear = w.awardyear
ORDER BY n.awardyear;