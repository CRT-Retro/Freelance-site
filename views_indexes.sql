-- View ترکیب کاربران و مهارت‌ها
CREATE VIEW IF NOT EXISTS user_skills_view AS
SELECT u.id AS user_id, u.username, u.job_title, u.location, s.skill
FROM users u
LEFT JOIN skills s ON u.id = s.user_id;

-- Index برای جستجوی سریع روی نام کاربر
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Index برای جستجوی سریع روی user_id در skills
CREATE INDEX IF NOT EXISTS idx_skills_user_id ON skills(user_id);

-- Index برای جستجوی سریع روی مهارت
CREATE INDEX IF NOT EXISTS idx_skills_skill ON skills(skill);
