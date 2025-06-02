# Rho VC Portfolio Scraper

A web application that scrapes portfolio company information from VC websites. Built with Next.js for the frontend and Python (Flask) for the backend.

## Features

- Modern UI built with Next.js and Tailwind CSS
- Python scraper using Playwright for JavaScript-heavy sites
- CSV export functionality
- Easy-to-use interface

## Tech Stack

- Frontend:
  - Next.js
  - React
  - Tailwind CSS
  - TypeScript

- Backend:
  - Python
  - Flask
  - Playwright
  - BeautifulSoup4

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd rho-vc-scraper
```

2. Install frontend dependencies:
```bash
npm install
```

3. Set up Python environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install chromium
```

5. Start the development servers:

In one terminal (Flask backend):
```bash
source .venv/bin/activate
python api_server.py
```

In another terminal (Next.js frontend):
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Deployment

The application is set up for deployment on:
- Frontend: Vercel
- Backend: Railway or Heroku

See deployment documentation for more details.

## Environment Variables

Frontend (.env.local):
```
PYTHON_API_URL=your-backend-url
```

Backend (.env):
```
ALLOWED_ORIGINS=your-frontend-url
PORT=5000
```

## License

MIT 