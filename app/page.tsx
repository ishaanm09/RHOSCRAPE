'use client';

import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [csvData, setCsvData] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setCsvData(null);

    try {
      const response = await fetch('/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });

      if (!response.ok) {
        throw new Error('Failed to scrape data');
      }

      const data = await response.text();
      setCsvData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (!csvData) return;

    const blob = new Blob([csvData], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'portfolio_companies.csv';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="w-full max-w-2xl space-y-8">
        <h1 className="text-4xl font-medium text-left text-white">
          Rho VC Portfolio Scraper
        </h1>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex gap-4">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter VC portfolio URL..."
              required
              className="flex-1 px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="px-6 py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Scraping...' : 'Scrape'}
            </button>
          </div>
        </form>

        {error && (
          <div className="p-4 rounded-lg bg-red-900/50 border border-red-700 text-red-200">
            {error}
          </div>
        )}

        {csvData && !error && (
          <div className="space-y-4">
            <div className="p-4 rounded-lg bg-green-900/50 border border-green-700 text-green-200">
              Successfully scraped portfolio companies!
            </div>
            <button
              onClick={handleDownload}
              className="w-full px-6 py-3 rounded-lg bg-green-600 text-white font-medium hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              Download CSV
            </button>
          </div>
        )}
      </div>
    </main>
  );
} 