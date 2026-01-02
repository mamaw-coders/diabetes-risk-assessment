# GlucoSense - Frontend

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
├── index.html          # Main entry (4-step wizard form)
├── css/
│   └── style.css       # Custom styling (28KB)
└── js/
    └── app.js          # Form handling & API calls
```

## Features

- **4-Step Wizard Form**: Basics → Medical History → Lifestyle → Health Status
- **Live Validation**: Real-time form validation with Bootstrap
- **Risk Visualization**: Color-coded results with risk meter
- **Print Support**: Print-friendly results page
- **Responsive Design**: Mobile-first Bootstrap layout

## Configuration

Edit `js/app.js` to set the API base URL:

```javascript
const API_URL = "http://localhost:5000";
```

## Sections

| Section      | Description                |
| ------------ | -------------------------- |
| Hero         | Landing with image collage |
| How It Works | 3-step process explanation |
| About        | Early detection benefits   |
| Assessment   | 4-step wizard form         |
| FAQ          | Common questions accordion |
| Footer       | Disclaimer & credits       |

## Dependencies

All loaded via CDN:

- Bootstrap 5.3.2
- Google Fonts (Inter, Plus Jakarta Sans)
