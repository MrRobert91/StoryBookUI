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
    <div className="max-w-2xl mx-auto space-y-4">
      <h1 className="text-3xl font-bold text-center mb-2">Crea tu Cuento</h1>
      <p className="text-center text-gray-600">
        Describe la historia que te gustaría contar y deja que la magia comience.
      </p>
      <div className="bg-white p-4 sm:p-6 rounded shadow space-y-4">
        <textarea
          className="w-full border rounded p-2 focus:outline-none focus:ring"
          rows={3}
          placeholder="Un dragón aventurero en el espacio..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button
          onClick={handleGenerate}
          disabled={disabled}
          className="w-full py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        >
          {loading ? 'Generando...' : 'Generar cuento'}
        </button>
        {tale && (
          <pre className="whitespace-pre-wrap border p-2 bg-gray-50 rounded max-h-96 overflow-y-auto">
            {tale}
          </pre>
        )}
      </div>
      <p className="text-xs text-gray-500 text-center">
        El servicio puede tardar unos segundos en responder.
      </p>
    </div>
  );
}
