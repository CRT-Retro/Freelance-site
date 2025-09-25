-- View user and skill combinations
CREATE VIEW IF NOT EXISTS user_skills_view AS
SELECT u.id AS user_id,
       u.username,
       u.job_title,
       u.location,
       s.skill
FROM users u
LEFT JOIN skills s ON u.id = s.user_id;

-- View for average user rating
CREATE VIEW IF NOT EXISTS user_avg_rating_view AS
SELECT reviewed_id AS user_id,
       AVG(rating) AS avg_rating,
       COUNT(*) AS total_reviews
FROM reviews
GROUP BY reviewed_id;

-- Index for quick search on username
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Index for quick search on user_id in skills
CREATE INDEX IF NOT EXISTS idx_skills_user_id ON skills(user_id);

-- Index for quick search on skills
CREATE INDEX IF NOT EXISTS idx_skills_skill ON skills(skill);

-- Index for quick search on favorites
CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_favorites_favorite_user_id ON favorites(favorite_user_id);

-- FTS virtual table for quick search on user name and job title
CREATE VIRTUAL TABLE IF NOT EXISTS users_fts USING fts5(
    username,
    job_title,
    content='users',
    content_rowid='id'
);
