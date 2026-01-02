# Diabetes Risk Assessment AI

> AI-powered diabetes risk screening trained on 70,000+ clinical records

[![CI](https://github.com/mamaw-coders/diabetes-risk-assessment/actions/workflows/ci.yml/badge.svg)](https://github.com/mamaw-coders/diabetes-risk-assessment/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

**GlucoSense** is a web-based health screening tool that uses machine learning to assess diabetes risk. Built as a final project for CSST 102.

**Features:**

- 🤖 Random Forest classifier trained on CDC BRFSS 2015 data (70,000+ records)
- 🏥 BMI auto-calculation (kg/cm inputs)
- 🔒 Privacy-first: no data storage
- 📱 Responsive 4-step wizard interface
- 🖨️ Print-friendly results

## Project Structure

```
diabetes-risk-assessment/
├── client/                 # Frontend (Bootstrap 5)
│   ├── index.html          # 4-step wizard form
│   ├── css/style.css       # Custom styling
│   └── js/app.js           # Form logic & API calls
├── server/                 # Backend (Flask)
│   ├── app/
│   │   ├── api/            # Routes & validation
│   │   ├── services/       # Business logic
│   │   ├── models/         # ML model loader
│   │   └── utils/          # Helpers & constants
│   ├── artifacts/          # Trained model (model.pkl)
│   ├── scripts/            # Training & evaluation
│   └── tests/              # Pytest suite
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
  "stroke": false,
  "phys_activity": true,
  "fruits": true,
  "veggies": true,
  "heavy_alcohol": false,
  "general_health": 3,
  "mental_health": 0,
  "physical_health": 0,
  "difficulty_walking": false
}
```

**Example Response:**

```json
{
  "risk_level": "LOW",
  "probability": 0.32,
  "bmi": 27.76,
  "bmi_category": "Overweight",
  "contributing_factors": ["BMI indicates overweight"],
  "disclaimer": "This is for educational purposes only..."
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

**Mamaw Coders** – CSST 102 Final Project

## Disclaimer

This tool is for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
