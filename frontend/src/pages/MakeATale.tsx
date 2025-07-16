import { useState } from 'react';

export default function MakeATale() {
  const [description, setDescription] = useState('');
  const [tale, setTale] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleGenerate() {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/generate-story', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description })
      });
      const data = await res.json();
      if (data.tale) setTale(data.tale);
    } catch {
      alert('Failed to generate tale');
    } finally {
      setLoading(false);
    }
  }

  const disabled = loading || description.trim() === '';

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
