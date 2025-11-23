-- Create function to check if email exists in auth.users
CREATE OR REPLACE FUNCTION public.check_email_exists(email_to_check TEXT)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  -- Check if email exists in auth.users table
  RETURN EXISTS (
    SELECT 1 
    FROM auth.users 
    WHERE email = LOWER(TRIM(email_to_check))
  );
EXCEPTION
  WHEN OTHERS THEN
    -- Return false on any error to not block registration
    RETURN FALSE;
END;
$$;

-- Create alternative function that returns more detailed info
CREATE OR REPLACE FUNCTION public.check_user_exists_by_email(email_to_check TEXT)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  user_exists BOOLEAN;
  result JSON;
BEGIN
  -- Check if email exists in auth.users table
  SELECT EXISTS (
    SELECT 1 
    FROM auth.users 
    WHERE email = LOWER(TRIM(email_to_check))
  ) INTO user_exists;
  
  -- Return JSON with exists flag
  result := json_build_object('exists', user_exists);
  
  RETURN result;
EXCEPTION
  WHEN OTHERS THEN
    -- Return false on any error
    RETURN json_build_object('exists', false);
END;
$$;

-- Grant execute permissions
GRANT EXECUTE ON FUNCTION public.check_email_exists(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.check_email_exists(TEXT) TO anon;
GRANT EXECUTE ON FUNCTION public.check_user_exists_by_email(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION public.check_user_exists_by_email(TEXT) TO anon;
