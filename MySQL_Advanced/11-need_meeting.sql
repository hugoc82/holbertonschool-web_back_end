-- 11. No table for a meeting
-- Creates a view `need_meeting` that lists all students
-- with a score under 80 and no last_meeting OR last_meeting older than 1 month

CREATE OR REPLACE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
  AND (
        last_meeting IS NULL
        OR last_meeting < (CURDATE() - INTERVAL 1 MONTH)
      );

