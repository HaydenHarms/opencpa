-- Practice splits multiple-choice questions and simulations into separate sessions, as the exam
-- splits them into separate testlets. 'questions' and 'simulations' are Practice sessions; a
-- Library topic session keeps both kinds and is 'mixed'. Each mode keeps its own active session.
ALTER TABLE practice_sessions ADD COLUMN mode TEXT NOT NULL DEFAULT 'questions';
UPDATE practice_sessions SET mode = 'mixed' WHERE topic IS NOT NULL;
CREATE INDEX practice_sessions_mode ON practice_sessions(user_id, section, mode, status);
