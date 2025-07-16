/// <reference lib="deno.unstable" />
import { serve } from 'https://deno.land/std@0.203.0/http/server.ts';

serve(async (req) => {
  const { description } = await req.json();
  const supabaseJwt = req.headers.get('Authorization')?.replace('Bearer ', '');
  if (!supabaseJwt) {
    return new Response('Unauthorized', { status: 401 });
  }

  const openAiKey = Deno.env.get('OPENAI_API_KEY');
  if (!openAiKey) {
    return new Response('Missing OpenAI key', { status: 500 });
  }

  const payload = {
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: `Write a short children tale about: ${description}` }]
  };

  const aiRes = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${openAiKey}`
    },
    body: JSON.stringify(payload)
  });
  const aiData = await aiRes.json();
  const tale = aiData.choices?.[0]?.message?.content ?? '';

  // Here you would check credits and decrement 1 credit in your DB
  // This simplified example omits that logic.

  return new Response(JSON.stringify({ tale }), {
    headers: { 'Content-Type': 'application/json' }
  });
});
