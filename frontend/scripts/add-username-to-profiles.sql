-- Add username column to profiles table with proper constraints
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS username TEXT;

-- Create unique index for username (case-insensitive)
CREATE UNIQUE INDEX IF NOT EXISTS profiles_username_unique_idx 
ON public.profiles (LOWER(username));

-- Add constraint to ensure username follows the pattern
ALTER TABLE public.profiles 
ADD CONSTRAINT IF NOT EXISTS username_format_check 
CHECK (username ~ '^[a-z0-9_.]{3,20}$');

-- Add constraint to prevent invalid patterns
ALTER TABLE public.profiles 
ADD CONSTRAINT IF NOT EXISTS username_pattern_check 
CHECK (username !~ '^[._]|[._]$|[._]{2,}');

-- Update existing profiles with temporary usernames
UPDATE public.profiles 
SET username = 'user_' || SUBSTRING(id::text, 1, 8)
WHERE username IS NULL;

-- Make username NOT NULL after updating existing records
ALTER TABLE public.profiles 
ALTER COLUMN username SET NOT NULL;

-- Create RLS policies for profiles table
-- Allow users to read their own profile
CREATE POLICY IF NOT EXISTS "Users can read own profile" ON public.profiles
FOR SELECT USING (auth.uid() = id);

-- Allow users to update their own profile
CREATE POLICY IF NOT EXISTS "Users can update own profile" ON public.profiles
FOR UPDATE USING (auth.uid() = id);

-- Allow users to insert their own profile
CREATE POLICY IF NOT EXISTS "Users can insert own profile" ON public.profiles
FOR INSERT WITH CHECK (auth.uid() = id);

-- Allow public read access to usernames for availability checking
CREATE POLICY IF NOT EXISTS "Public can read usernames" ON public.profiles
FOR SELECT USING (true);

-- Enable RLS on profiles table
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Grant necessary permissions
GRANT SELECT, INSERT, UPDATE ON public.profiles TO authenticated;
GRANT SELECT ON public.profiles TO anon;
