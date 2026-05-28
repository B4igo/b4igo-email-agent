# frontend

React + Vite single-page app (port 5173) where the user signs in, links email
accounts, and reviews and confirms parsed entries. It also builds as a Chromium
browser extension.

## Talking to the backend

All API calls go through axios with an absolute base URL (`src/API/Auth.ts`),
configured by the `VITE_BACKEND_URL` build-time variable and defaulting to
`http://localhost:5000/api`. There is no dev-server proxy. Set `VITE_BACKEND_URL`
when running or building against a non-default backend.

## Develop

```bash
cd frontend
npm install
npm run dev
```

## Build as a browser extension

```bash
cd frontend
npm run build
```

Then load `frontend/dist` as an unpacked extension from `chrome://extensions/` with
developer mode on. The extension's allowed hosts and content-script matches are in
`public/manifest.json`; update them to your production domain before building for
release.

## Configuration

`VITE_BACKEND_URL` (see `docs/CONFIGURATION.md`). For credentialed requests to
succeed, the backend's `B4IGO_CORS_ORIGINS` must include this app's origin (and the
`chrome-extension://<id>` origin when running as an extension).

## Tests

No automated tests yet (see `docs/ROADMAP.md`).
