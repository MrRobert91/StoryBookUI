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

-- Drop existing trigger and function to recreate them
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user();

-- Create improved function to handle new user profile creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
DECLARE
  temp_username TEXT;
  profile_exists BOOLEAN;
BEGIN
  -- Check if profile already exists
  SELECT EXISTS(SELECT 1 FROM public.profiles WHERE id = NEW.id) INTO profile_exists;
  
  IF profile_exists THEN
    RAISE WARNING 'Profile already exists for user %', NEW.id;
    RETURN NEW;
  END IF;
  
  -- Generate a unique temporary username
  temp_username := 'user_' || SUBSTRING(NEW.id::text, 1, 8);
  
  -- Insert profile with error handling
  BEGIN
    INSERT INTO public.profiles (id, username, credits, plan, created_at)
    VALUES (NEW.id, temp_username, 10, 'free', NOW());
    
    RAISE LOG 'Profile created successfully for user %', NEW.id;
  EXCEPTION
    WHEN unique_violation THEN
      -- If username already exists, try with timestamp
      temp_username := 'user_' || SUBSTRING(NEW.id::text, 1, 8) || '_' || EXTRACT(EPOCH FROM NOW())::INTEGER;
      INSERT INTO public.profiles (id, username, credits, plan, created_at)
      VALUES (NEW.id, temp_username, 10, 'free', NOW());
      
      RAISE LOG 'Profile created with timestamped username for user %', NEW.id;
    WHEN OTHERS THEN
      -- Log error but don't fail user creation
      RAISE WARNING 'Could not create profile for user %: %', NEW.id, SQLERRM;
  END;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

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
  profile_exists BOOLEAN;
BEGIN
  FOR user_record IN 
    SELECT au.id, au.email
    FROM auth.users au
    LEFT JOIN public.profiles p ON au.id = p.id
    WHERE p.id IS NULL
  LOOP
    temp_username := 'user_' || SUBSTRING(user_record.id::text, 1, 8);
    
    -- Double check profile doesn't exist
    SELECT EXISTS(SELECT 1 FROM public.profiles WHERE id = user_record.id) INTO profile_exists;
    
    IF NOT profile_exists THEN
      BEGIN
        INSERT INTO public.profiles (id, username, credits, plan, created_at)
        VALUES (user_record.id, temp_username, 10, 'free', NOW());
      EXCEPTION
        WHEN unique_violation THEN
          temp_username := 'user_' || SUBSTRING(user_record.id::text, 1, 8) || '_' || EXTRACT(EPOCH FROM NOW())::INTEGER;
          INSERT INTO public.profiles (id, username, credits, plan, created_at)
          VALUES (user_record.id, temp_username, 10, 'free', NOW());
        WHEN OTHERS THEN
          RAISE WARNING 'Could not create profile for existing user %: %', user_record.id, SQLERRM;
      END;
    END IF;
  END LOOP;
END $$;
