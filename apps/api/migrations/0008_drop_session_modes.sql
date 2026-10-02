-- Undo 0007. Practice keeps one session per section again, with its questions and simulations
-- on separate tabs, so sessions don't need a mode. Simulation-only sessions made under 0007 are
-- ended; their answers still count toward mastery and review scheduling.
UPDATE practice_sessions SET status = 'abandoned' WHERE mode = 'simulations' AND status = 'active';
DROP INDEX practice_sessions_mode;
ALTER TABLE practice_sessions DROP COLUMN mode;
