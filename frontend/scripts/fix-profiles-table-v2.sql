-- Clean up any duplicate profiles first
DELETE FROM public.profiles 
WHERE id IN (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY id ORDER BY created_at) as rn
    FROM public.profiles
  ) t WHERE t.rn > 1
);

-- Clean up any profiles without corresponding auth users
DELETE FROM public.profiles 
WHERE id NOT IN (SELECT id FROM auth.users);

-- Drop and recreate the profiles table with proper structure
DROP TABLE IF EXISTS public.profiles CASCADE;

CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  credits INTEGER DEFAULT 10 NOT NULL,
  plan TEXT DEFAULT 'free' NOT NULL CHECK (plan IN ('free', 'plus')),
  plus_since TIMESTAMPTZ,
  last_credited_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Create unique index for username (case-insensitive)
CREATE UNIQUE INDEX profiles_username_unique_idx ON public.profiles (LOWER(username));

-- Add username format constraints
ALTER TABLE public.profiles 
ADD CONSTRAINT username_format_check 
CHECK (username ~ '^[a-z0-9_.]{3,20}$');

ALTER TABLE public.profiles 
ADD CONSTRAINT username_pattern_check 
CHECK (username !~ '^[._]|[._]$|[._]{2,}');

-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Enable read access for own profile" ON public.profiles
FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Enable insert access for own profile" ON public.profiles
FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Enable update access for own profile" ON public.profiles
FOR UPDATE USING (auth.uid() = id);

-- Allow public read access to usernames only (for availability checking)
CREATE POLICY "Enable public username read" ON public.profiles
FOR SELECT USING (true);

-- Grant permissions
GRANT ALL ON public.profiles TO authenticated;
GRANT SELECT ON public.profiles TO anon;

-- Create function to handle new user profile creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
DECLARE
  temp_username TEXT;
BEGIN
  -- Generate a unique temporary username
  temp_username := 'user_' || SUBSTRING(NEW.id::text, 1, 8);
  
  -- Insert profile with error handling
  BEGIN
    INSERT INTO public.profiles (id, username, credits, plan)
    VALUES (NEW.id, temp_username, 10, 'free');
  EXCEPTION
    WHEN unique_violation THEN
      -- If username already exists, try with timestamp
      temp_username := 'user_' || SUBSTRING(NEW.id::text, 1, 8) || '_' || EXTRACT(EPOCH FROM NOW())::INTEGER;
      INSERT INTO public.profiles (id, username, credits, plan)
      VALUES (NEW.id, temp_username, 10, 'free');
    WHEN OTHERS THEN
      -- Log error but don't fail user creation
      RAISE WARNING 'Could not create profile for user %: %', NEW.id, SQLERRM;
  END;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Create trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Grant execute permission
GRANT EXECUTE ON FUNCTION public.handle_new_user() TO service_role;

-- Create profiles for existing users who don't have one
DO $$
DECLARE
  user_record RECORD;
  temp_username TEXT;
BEGIN
  FOR user_record IN 
    SELECT au.id, au.email
    FROM auth.users au
    LEFT JOIN public.profiles p ON au.id = p.id
    WHERE p.id IS NULL
  LOOP
    temp_username := 'user_' || SUBSTRING(user_record.id::text, 1, 8);
    
    BEGIN
      INSERT INTO public.profiles (id, username, credits, plan)
      VALUES (user_record.id, temp_username, 10, 'free');
    EXCEPTION
      WHEN unique_violation THEN
        temp_username := 'user_' || SUBSTRING(user_record.id::text, 1, 8) || '_' || EXTRACT(EPOCH FROM NOW())::INTEGER;
        INSERT INTO public.profiles (id, username, credits, plan)
        VALUES (user_record.id, temp_username, 10, 'free');
      WHEN OTHERS THEN
        RAISE WARNING 'Could not create profile for existing user %: %', user_record.id, SQLERRM;
    END;
  END LOOP;
END $$;
