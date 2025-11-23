-- First, let's check and fix any existing temp usernames
UPDATE public.profiles 
SET username = 'user_' || SUBSTRING(id::text, 1, 8)
WHERE username LIKE 'temp_%';

-- Drop and recreate the trigger function with better error handling
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user();

-- Create a simpler function that just creates the basic profile
-- The application will handle the username update
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
DECLARE
  temp_username TEXT;
BEGIN
  -- Generate a temporary username
  temp_username := 'temp_' || SUBSTRING(NEW.id::text, 1, 8);
  
  -- Insert profile with basic data
  BEGIN
    INSERT INTO public.profiles (id, username, credits, plan, created_at)
    VALUES (NEW.id, temp_username, 10, 'free', NOW());
    
    RAISE LOG 'Profile created for user % with temp username %', NEW.id, temp_username;
  EXCEPTION
    WHEN unique_violation THEN
      -- If temp username exists, add timestamp
      temp_username := 'temp_' || SUBSTRING(NEW.id::text, 1, 8) || '_' || EXTRACT(EPOCH FROM NOW())::INTEGER;
      INSERT INTO public.profiles (id, username, credits, plan, created_at)
      VALUES (NEW.id, temp_username, 10, 'free', NOW());
      
      RAISE LOG 'Profile created with timestamped temp username for user %', NEW.id;
    WHEN OTHERS THEN
      RAISE WARNING 'Could not create profile for user %: %', NEW.id, SQLERRM;
  END;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Grant permissions
GRANT EXECUTE ON FUNCTION public.handle_new_user() TO service_role;

-- Create a function to update username that we can call from the application
CREATE OR REPLACE FUNCTION public.update_user_username(user_id UUID, new_username TEXT)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  username_exists BOOLEAN;
BEGIN
  -- Check if username already exists for another user
  SELECT EXISTS(
    SELECT 1 FROM public.profiles 
    WHERE LOWER(username) = LOWER(new_username) 
    AND id != user_id
  ) INTO username_exists;
  
  IF username_exists THEN
    RAISE EXCEPTION 'Username already exists';
  END IF;
  
  -- Update the username
  UPDATE public.profiles 
  SET username = LOWER(TRIM(new_username))
  WHERE id = user_id;
  
  -- Check if update was successful
  IF NOT FOUND THEN
    RAISE EXCEPTION 'User profile not found';
  END IF;
  
  RETURN TRUE;
EXCEPTION
  WHEN OTHERS THEN
    RAISE EXCEPTION 'Failed to update username: %', SQLERRM;
END;
$$;

-- Grant execute permission
GRANT EXECUTE ON FUNCTION public.update_user_username(UUID, TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.update_user_username(UUID, TEXT) TO service_role;
