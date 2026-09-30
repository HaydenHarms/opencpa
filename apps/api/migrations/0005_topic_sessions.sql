-- Library: practice sessions scoped to one blueprint topic (NULL = a whole-section session).
ALTER TABLE practice_sessions ADD COLUMN topic TEXT;
CREATE INDEX practice_sessions_topic ON practice_sessions(user_id, section, topic, status);
