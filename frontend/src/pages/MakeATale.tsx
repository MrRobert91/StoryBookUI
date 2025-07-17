import React, { useState } from 'react';

interface Chapter {
  title: string;
  text: string;
}

export default function MakeATale() {
  const [prompt, setPrompt] = useState('');
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [current, setCurrent] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const apiUrl = import.meta.env.VITE_API_URL;

  async function handleGenerate() {
    setLoading(true);
    setError('');
    setChapters([]);
    setCurrent(0);

    try {
      const res = await fetch(`${apiUrl}/generate-story-ai`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      if (data.chapters) {
        setChapters(data.chapters);
      } else {
        setError(data.error || 'No chapters found');
      }
    } catch (err) {
      setError('Error generating story: ' + (err instanceof Error ? err.message : String(err)));
    } finally {
      setLoading(false);
    }
  }

  function prevChapter() {
    setCurrent((c) => Math.max(0, c - 1));
  }

  function nextChapter() {
    setCurrent((c) => Math.min(chapters.length - 1, c + 1));
  }

  return (
    <div className="max-w-xl mx-auto mt-8">
      <h2 className="text-2xl font-bold mb-4">Genera tu cuento</h2>
      <input
        type="text"
        className="border p-2 w-full mb-2"
        placeholder="Describe tu cuento..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded mb-4"
        onClick={handleGenerate}
        disabled={loading || !prompt}
      >
        {loading ? 'Generando...' : 'Generar cuento'}
      </button>
      {error && <div className="text-red-500 mb-2">{error}</div>}
      {chapters.length > 0 && (
        <div className="border p-4 rounded shadow">
          <h3 className="text-xl font-semibold mb-2">{chapters[current].title}</h3>
          <p className="mb-4">{chapters[current].text}</p>
          <div className="flex justify-between">
            <button
              className="bg-gray-300 px-3 py-1 rounded"
              onClick={prevChapter}
              disabled={current === 0}
            >
              Anterior
            </button>
            <span>
              Capítulo {current + 1} de {chapters.length}
            </span>
            <button
              className="bg-gray-300 px-3 py-1 rounded"
              onClick={nextChapter}
              disabled={current === chapters.length - 1}
            >
              Siguiente
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
