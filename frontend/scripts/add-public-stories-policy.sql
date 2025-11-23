-- Create policy to allow anonymous users to view public stories
CREATE POLICY "Anyone can view public stories" ON stories
  FOR SELECT USING (visibility = 'public');

-- Ensure the policy is applied correctly
-- This policy allows anyone (including anonymous users) to read stories that are marked as public
-- The existing policies for authenticated users remain unchanged

-- Verify current policies (for reference)
-- SELECT * FROM pg_policies WHERE tablename = 'stories';
