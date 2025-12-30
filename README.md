# Diabetes Risk Assessment AI

> AI-powered diabetes risk screening trained on 70,000+ clinical records

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

A web-based health screening tool that uses machine learning to assess diabetes risk. Built as a final project for CSST 101.

**Features:**

- 🤖 Random Forest classifier trained on CDC BRFSS 2015 data
- 🏥 BMI auto-calculation (kg/cm inputs)
- 🔒 Privacy-first: no data storage
- 📱 Responsive design

## Project Structure

```
diabetes-risk-assessment/
├── client/                 # Frontend (Bootstrap 5)
│   ├── index.html
│   └── assets/
│       ├── css/
│       └── js/
├── server/                 # Backend (Flask)
│   ├── app/
│   │   ├── api/            # Routes & validation
│   │   ├── services/       # Business logic
│   │   ├── models/         # ML model
│   │   └── utils/          # Helpers
│   ├── artifacts/          # Trained model (.pkl)
│   └── tests/
├── data/                   # BRFSS dataset
└── docs/                   # PRD & documentation
```

## Quick Start

### Backend

```bash
cd server
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Server runs at `http://localhost:5000`

### Frontend

```bash
cd client
python -m http.server 3000
```

Open `http://localhost:3000`

## API

| Method | Endpoint   | Description     |
| ------ | ---------- | --------------- |
| GET    | `/health`  | Health check    |
| POST   | `/predict` | Risk prediction |

**Example Request:**

```json
{
  "age": 45,
  "sex": "male",
  "weight": 85,
  "height": 175,
  "high_bp": true,
  "high_chol": false,
  "smoker": false,
  "heart_disease": false,
  "general_health": 3,
  "phys_activity": true
}
```

**Example Response:**

```json
{
  "risk_level": "LOW",
  "probability": 0.32,
  "bmi": 27.76,
  "bmi_category": "Overweight"
}
```

## Tech Stack

| Layer    | Technology                           |
| -------- | ------------------------------------ |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Backend  | Python, Flask, Marshmallow           |
| ML       | scikit-learn (Random Forest)         |
| Data     | CDC BRFSS 2015                       |

## Team

**Mamaw Coders** – CSST 101 Final Project

## Disclaimer

This tool is for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.

## License

MIT
