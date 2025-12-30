# Diabetes Risk Assessment - Frontend

Bootstrap 5 web interface for the Diabetes Risk Predictor AI.

## Quick Start

1. Serve the files using any static server:

   ```bash
   # Using Python
   python -m http.server 3000

   # Using Node.js
   npx serve .
   ```

2. Open `http://localhost:3000` in your browser

## Structure

```
client/
├── index.html          # Main entry point
└── assets/
    ├── css/
    │   ├── styles.css      # Global styles
    │   └── components.css  # Component styles
    ├── js/
    │   ├── main.js         # App initialization
    │   ├── api.js          # API service
    │   ├── form.js         # Form handling
    │   └── results.js      # Results display
    └── images/
```

## Configuration

Edit `assets/js/api.js` to set the API base URL:

```javascript
const API_BASE_URL = "http://localhost:5000";
```
