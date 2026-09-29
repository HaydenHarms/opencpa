-- Question variants: which version of an item was served and answered (0 is the item itself).
ALTER TABLE attempts ADD COLUMN variant INTEGER NOT NULL DEFAULT 0;

-- The version chosen for each item when a session is built: a JSON array parallel to item_ids.
-- NULL (sessions made before variants existed) means version 0 throughout.
ALTER TABLE practice_sessions ADD COLUMN variants TEXT;
