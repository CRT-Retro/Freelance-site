PRAGMA foreign_keys = ON;

INSERT INTO users (username, email, password_hash, role, job_title, location) VALUES
('negin', 'negin@gmail.com', '123456789', 'freelancer', 'Backend Developer', 'Tehran'),
('sadra', 'sadra@gmail.com', '123456789', 'freelancer', 'Data Engineer', 'Tehran'),
('ali', 'ali@gmail.com', '123456789', 'freelancer', 'Data Analyst', 'Tehran'),
('mohammad', 'mohammad@gmail.com', '123456789', 'freelancer', 'Data Engineer', 'Tehran'),
('sajjad', 'sajjad@gmail.com', '123456789', 'employer', 'Startup Founder', 'Zanjan'),
('majid', 'majid@gmail.com', '123456789', 'employer', 'Project Manager', 'Zanjan'),
('radman', 'radman@gmail.com', '123456789', 'admin', 'Database Admin', 'Zanjan'),
('ronika', 'ronika@gmail.com', '123456789', 'admin', 'Backend Admin', 'Tehran'),
('sedigh', 'sedigh@gmail.com', '123456789', 'admin', 'Frontend Admin', 'Kerman');
