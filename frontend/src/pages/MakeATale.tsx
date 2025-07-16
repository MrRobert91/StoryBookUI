import { useState } from 'react';
import { useSession, useSupabaseClient } from '../context/AuthContext';

export default function MakeATale() {
  const [description, setDescription] = useState('');
  const [tale, setTale] = useState('');
  const [loading, setLoading] = useState(false);
  const supabase = useSupabaseClient();
  const session = useSession();

  async function handleGenerate() {
    setLoading(true);
    const { data, error } = await supabase.functions.invoke('generate_tale', {
      body: { description }
    });
    if (data) setTale(data.tale);
    if (error) alert(error.message);
    setLoading(false);
  }

  const disabled = !session || loading;

  return (
    <div className="max-w-xl mx-auto space-y-4">
      <textarea
        className="w-full border rounded p-2"
        rows={3}
        placeholder="Describe your tale..."
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button
        onClick={handleGenerate}
        disabled={disabled}
        className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {loading ? 'Generating...' : 'Generate'}
      </button>
      {tale && <pre className="whitespace-pre-wrap border p-2">{tale}</pre>}
    </div>
  );
}
