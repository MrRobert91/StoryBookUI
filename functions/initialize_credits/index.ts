/// <reference lib="deno.unstable" />
import { serve } from 'https://deno.land/std@0.203.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
  const serviceRole = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
  const supabase = createClient(supabaseUrl, serviceRole);

  const { user } = await req.json();
  if (!user) return new Response('Bad request', { status: 400 });

  await supabase.from('user_credits').insert({ id: user.id, credits: 10 });

  return new Response('ok');
});
