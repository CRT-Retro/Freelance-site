-- نمایش کاربران و مهارت‌ها (هر مهارت یک ردیف)
SELECT
  u.id   AS user_id,
  u.username,
  u.job_title,
  u.location,
  s.skill
FROM users u
LEFT JOIN skills s ON u.id = s.user_id
ORDER BY u.username, s.skill;

-- نمایش پروفایل هر کاربر با مهارت‌ها به صورت یکجا
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
