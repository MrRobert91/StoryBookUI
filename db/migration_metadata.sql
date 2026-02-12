-- Migration script to add metadata columns safely
-- Execute this in your Supabase SQL Editor

DO $$ 
BEGIN 
    -- Add story_type column if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='stories' AND COLUMN_NAME='story_type') THEN
        ALTER TABLE stories ADD COLUMN story_type TEXT DEFAULT 'open';
        COMMENT ON COLUMN stories.story_type IS 'Type of story: open or guided';
    END IF;

    -- Add metadata column if it doesn't exist
    IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='stories' AND COLUMN_NAME='metadata') THEN
        ALTER TABLE stories ADD COLUMN metadata JSONB DEFAULT '{}';
        COMMENT ON COLUMN stories.metadata IS 'Metadata parameters used to build the story';
    END IF;
END $$;
