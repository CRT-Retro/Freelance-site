-- Insert freelancers
INSERT INTO users (username, email, password_hash, role, photo, job_title, location)
VALUES
('negin', 'negin@gmail.com', '123456789', 'freelancer', NULL, 'Backend Developer', 'Tehran'),
('sadra', 'sadra@gmail.com', '123456789', 'freelancer', NULL, 'Data Engineer', 'tehran'),
('ali', 'ali@gmail.com', '123456789', 'freelancer', NULL, 'Data Analyst', 'tehran');

-- Insert employers
INSERT INTO users (username, email, password_hash, role, photo, job_title, location)
VALUES
('sajjad', 'sajjad@gmail.com', '123456789', 'employer', NULL, 'Startup Founder', 'Zanjan'),
('majid', 'majid@gmail.com', '123456789', 'employer', NULL, 'Project Manager', 'Zanjan');

-- Insert admins
INSERT INTO users (username, email, password_hash, role, photo, job_title, location)
VALUES
('radman', 'radman@gmail.com', '123456789', 'admin', NULL, 'Database Admin', 'Zanjan'),
('ronika', 'ronika@gmail.com', '123456789', 'admin', NULL, 'Backend Admin', 'tehran'),
('sedigh', 'sedigh@gmail.com', '123456789', 'admin', NULL, 'frontend Admin', 'kerman');