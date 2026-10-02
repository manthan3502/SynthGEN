# SynthGEN frontend

React + Vite + Axios client for the Flask API. Styles use the existing CSS and inline styles.

See the [root README](../README.md) for setup, environment variables, architecture, and limitations.

```sh
npm ci
npm run dev
npm run lint
npm run build
```

`VITE_API_BASE_URL` defaults to `http://localhost:5000`. Vite variables are public;
never put backend credentials in a frontend environment file.
