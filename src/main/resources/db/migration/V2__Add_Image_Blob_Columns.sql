-- Add image blob columns to events table
ALTER TABLE events ADD COLUMN image_data MEDIUMBLOB;
ALTER TABLE events ADD COLUMN image_mime_type VARCHAR(255);
