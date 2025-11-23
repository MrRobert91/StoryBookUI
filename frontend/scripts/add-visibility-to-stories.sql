-- Add visibility column to stories table
ALTER TABLE stories 
ADD COLUMN IF NOT EXISTS visibility TEXT NOT NULL DEFAULT 'private';

-- Add constraint to ensure only valid values
ALTER TABLE stories 
ADD CONSTRAINT stories_visibility_check 
CHECK (visibility IN ('public', 'private'));

-- Create index for faster queries by visibility
CREATE INDEX IF NOT EXISTS idx_stories_visibility ON stories(visibility);

-- Update existing stories to be private by default (if any exist)
UPDATE stories SET visibility = 'private' WHERE visibility IS NULL;

-- Add comment to document the column
COMMENT ON COLUMN stories.visibility IS 'Story visibility: public or private (default: private)';
