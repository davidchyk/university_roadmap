-- Drop the old physical path column after moving file storage metadata outside the DB schema.

ALTER TABLE attachments
DROP COLUMN path_a;
