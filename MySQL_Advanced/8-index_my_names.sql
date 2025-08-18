-- 8. Optimize simple search
-- Creates an index on the first letter of column name in table names

CREATE INDEX idx_name_first
ON names (name(1));

