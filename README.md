# Darukaa.Earth — Full-Stack Carbon & Biodiversity Platform

## Overview
A full-stack geospatial dashboard prototype for managing carbon and biodiversity projects and their geographical sites.

## Business requirements
- Basic registration/login UI with a JWT-ready FastAPI authentication endpoint.
- Create and view projects.
- View project sites on an interactive map.
- Draw polygons on a map by clicking vertices and create a mapped site.
- Click a site polygon to inspect analytics.
- Interactive Chart.js time-series visualization.
- Automated code-quality/build checks with GitHub Actions.
- Pre-commit configuration using Husky + lint-staged + Prettier/ESLint.

## Architecture
React/Vite frontend → FastAPI REST API → PostgreSQL + PostGIS.
The browser includes seeded data so the UI can be demonstrated without a running backend. The API and database schema are included for full-stack deployment.

## Required stack
Frontend: React, Vite, Leaflet/React-Leaflet for the runnable geospatial map, Chart.js.
Backend: Python FastAPI, JWT, PostgreSQL/PostGIS.
Developer experience: Git, GitHub Actions, Husky, lint-staged, Prettier, ESLint.

## Database schema
- users: authentication accounts.
- projects: project metadata/status.
- sites: project-linked polygons stored as PostGIS `GEOMETRY(POLYGON,4326)` with GiST spatial index.
- site_metrics: dated carbon, biodiversity and biomass measurements.
Relationships: projects 1→N sites; sites 1→N site_metrics.

## Local setup
Frontend:
```bash
cd frontend
npm install
npm run dev
```
Backend:
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API: `http://localhost:8000/health`

PostgreSQL + PostGIS:
```bash
docker compose up --build
```

## Demo login
Email: `admin@darukaa.earth`
Password: `password`

For production, replace demo authentication with database-backed password hashes, environment secrets and HTTPS.

## CI/CD
`.github/workflows/ci.yml` runs on pushes and pull requests to `main`, installs Node 20 dependencies, checks formatting, runs ESLint and builds the frontend. Production deployment can be attached to the workflow using Vercel/Render/Heroku deployment secrets.

## Pre-commit
Husky invokes lint-staged. lint-staged formats changed source files and runs ESLint on JS/JSX files before commits.

## Trade-offs
The challenge specifies Mapbox GL JS. This runnable prototype uses Leaflet/OpenStreetMap so it can run without a Mapbox token. The README is explicit about that substitution; if a Mapbox token is available, the map layer can be replaced with Mapbox GL JS. The persistence architecture remains PostgreSQL/PostGIS.

## Deployment
Recommended: Vercel for frontend, Render for FastAPI backend, and managed PostgreSQL with PostGIS. Set environment variables in the deployment platform and never commit secrets.
