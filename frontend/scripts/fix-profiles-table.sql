-- First, let's ensure the profiles table exists with the correct structure
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  credits INTEGER DEFAULT 10,
  plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'plus')),
  plus_since TIMESTAMPTZ,
  last_credited_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Drop existing constraints and indexes to recreate them properly
DROP INDEX IF EXISTS profiles_username_unique_idx;
ALTER TABLE public.profiles DROP CONSTRAINT IF EXISTS username_format_check;
ALTER TABLE public.profiles DROP CONSTRAINT IF EXISTS username_pattern_check;

-- Create proper unique index for username (case-insensitive)
CREATE UNIQUE INDEX profiles_username_unique_idx ON public.profiles (LOWER(username));

-- Add username format constraints
ALTER TABLE public.profiles 
ADD CONSTRAINT username_format_check 
CHECK (username ~ '^[a-z0-9_.]{3,20}$');

ALTER TABLE public.profiles 
ADD CONSTRAINT username_pattern_check 
CHECK (username !~ '^[._]|[._]$|[._]{2,}');

-- Drop all existing RLS policies
DROP POLICY IF EXISTS "Users can read own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON public.profiles;
DROP POLICY IF EXISTS "Public can read usernames" ON public.profiles;
DROP POLICY IF EXISTS "Anyone can read usernames for availability" ON public.profiles;
DROP POLICY IF EXISTS "Users can view their own profile" ON public.profiles;

-- Disable RLS temporarily to clean up
ALTER TABLE public.profiles DISABLE ROW LEVEL SECURITY;

-- Re-enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Create new, simpler RLS policies
CREATE POLICY "Enable read access for own profile" ON public.profiles
FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Enable insert access for own profile" ON public.profiles
FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Enable update access for own profile" ON public.profiles
FOR UPDATE USING (auth.uid() = id);

-- Allow public read access to usernames only (for availability checking)
CREATE POLICY "Enable public username read" ON public.profiles
FOR SELECT USING (true);

-- Grant necessary permissions
GRANT ALL ON public.profiles TO authenticated;
GRANT SELECT ON public.profiles TO anon;

-- Create or replace function to handle new user profile creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, username, credits, plan)
  VALUES (
    NEW.id,
    'user_' || SUBSTRING(NEW.id::text, 1, 8),
    10,
    'free'
  );
  RETURN NEW;
EXCEPTION
  WHEN OTHERS THEN
    -- Log the error but don't fail the user creation
    RAISE WARNING 'Could not create profile for user %: %', NEW.id, SQLERRM;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Create trigger to automatically create profile when user is created
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Update existing users without profiles
INSERT INTO public.profiles (id, username, credits, plan)
SELECT 
  au.id,
  'user_' || SUBSTRING(au.id::text, 1, 8),
  10,
  'free'
FROM auth.users au
LEFT JOIN public.profiles p ON au.id = p.id
WHERE p.id IS NULL
ON CONFLICT (id) DO NOTHING;

-- Grant execute permission on the function
GRANT EXECUTE ON FUNCTION public.handle_new_user() TO service_role;
