CREATE TABLE IF NOT EXISTS user_credits (
  id uuid PRIMARY KEY REFERENCES auth.users(id),
  credits integer NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now()
);
