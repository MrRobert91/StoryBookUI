-- Drop existing trigger and function to recreate them
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user();

-- Create improved function that creates profile with minimal data
-- We'll let the application handle setting the custom username
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
  
  -- Generate a simple temporary username that we'll update immediately
  temp_username := 'temp_' || SUBSTRING(NEW.id::text, 1, 8);
  
  -- Insert profile with minimal data
  BEGIN
    INSERT INTO public.profiles (id, username, credits, plan, created_at)
    VALUES (NEW.id, temp_username, 10, 'free', NOW());
    
    RAISE LOG 'Temporary profile created for user %', NEW.id;
  EXCEPTION
    WHEN OTHERS THEN
      -- Log error but don't fail user creation
      RAISE WARNING 'Could not create temporary profile for user %: %', NEW.id, SQLERRM;
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
