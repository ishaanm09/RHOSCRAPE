import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';
import { promises as fs } from 'fs';

const isProd = process.env.NODE_ENV === 'production';

export async function POST(req: NextRequest) {
  try {
    const { url } = await req.json();
    if (!url) {
      return NextResponse.json({ error: 'URL is required' }, { status: 400 });
    }

    if (isProd) {
      // In production, forward the request to our Python API
      const apiUrl = process.env.PYTHON_API_URL;
      if (!apiUrl) {
        throw new Error('PYTHON_API_URL environment variable is not set');
      }
      
      console.log('Calling API URL:', apiUrl);
      const response = await fetch(`${apiUrl}/scrape`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const error = await response.text();
        console.error('API Error:', error);
        throw new Error(`API Error: ${error}`);
      }

      const csvData = await response.text();
      return new NextResponse(csvData, {
        status: 200,
        headers: {
          'Content-Type': 'text/csv',
          'Content-Disposition': 'attachment; filename=portfolio_companies.csv'
        }
      });
    } else {
      // In development, use local Python process
      const scriptPath = path.join(process.cwd(), 'vc_scraper.py');
      const pythonProcess = spawn('.venv/bin/python', [scriptPath, url], {
        cwd: process.cwd(),
      });

      let output = '';
      let errorOutput = '';

      pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
        console.log('Python output:', data.toString());
      });

      pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
        console.error('Python error:', data.toString());
      });

      const exitCode = await new Promise((resolve, reject) => {
        pythonProcess.on('close', (code) => {
          console.log('Python process exited with code:', code);
          if (code === 0) {
            resolve(code);
          } else {
            reject(new Error(`Python process exited with code ${code}\nError: ${errorOutput}`));
          }
        });
      });

      const csvPath = path.join(process.cwd(), 'portfolio_companies.csv');
      try {
        const csvData = await fs.readFile(csvPath, 'utf-8');
        return new NextResponse(csvData, {
          status: 200,
          headers: {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=portfolio_companies.csv'
          }
        });
      } catch (err) {
        console.error('Error reading CSV file:', err);
        return NextResponse.json({ error: 'No data was scraped' }, { status: 500 });
      }
    }
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to scrape data' },
      { status: 500 }
    );
  }
} 