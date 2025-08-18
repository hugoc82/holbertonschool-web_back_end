-- 9. Optimize search and score
-- Creates a composite index on the first letter of name AND score in table names

CREATE INDEX idx_name_first_score
ON names (name(1), score);

