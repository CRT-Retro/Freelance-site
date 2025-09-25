-- Display users and skills (one row for each skill)
SELECT
  u.id   AS user_id,
  u.username,
  u.job_title,
  u.location,
  s.skill
FROM users u
LEFT JOIN skills s ON u.id = s.user_id
ORDER BY u.username, s.skill;

-- Display users and skills (one row for each skill)
SELECT
  u.id,
  u.username,
  u.job_title,
  u.location,
  COALESCE(GROUP_CONCAT(s.skill, ', '), '') AS skills
FROM users u
LEFT JOIN skills s ON u.id = s.user_id
GROUP BY u.id
ORDER BY u.username;
