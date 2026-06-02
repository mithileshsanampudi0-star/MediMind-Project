# MediMind AI

MediMind AI is an intelligent healthcare assistant built using Flask, MongoDB, LangChain, and Groq LLM. The platform analyzes symptoms, predicts possible diseases, assesses health risks, detects emergencies, recommends specialists, finds nearby hospitals, analyzes medical reports, and generates downloadable PDF health reports.

---

## Features

### Symptom Analysis Agent

* AI-powered symptom interpretation
* Detailed medical reasoning
* Context-aware health analysis

### Disease Prediction Agent

* Predicts likely medical conditions
* Differential diagnosis support
* Confidence-based recommendations

### Risk Assessment Agent

* Determines severity level
* Identifies health risks
* Provides urgency assessment

### Emergency Detection Agent

* Detects potential emergency situations
* Recommends immediate actions
* Flags high-risk conditions

### Specialist Recommendation Agent

* Suggests appropriate medical specialists
* Based on symptoms and disease predictions

### Hospital Recommendation Agent

* Finds nearby hospitals using Google Maps API
* Displays hospital ratings and addresses
* Specialist-aware recommendations

### Medical Report Analysis Agent

* Upload and analyze PDF medical reports
* Extracts key findings
* Generates simplified interpretations

### PDF Health Report Generator

* Creates professional downloadable reports
* Includes predictions, risks, recommendations, and hospital information

### Voice Symptom Input

* Browser-based speech recognition
* Hands-free symptom entry

### Healthcare Dashboard

* Modern dark theme
* Analytics dashboard
* Responsive design
* Professional healthcare SaaS interface

---

## Technology Stack

### Backend

* Python 3.12
* Flask
* MongoDB
* LangChain
* Groq API

### AI Layer

* LangChain
* Groq LLM

### Document Processing

* pdfplumber
* reportlab

### APIs

* Google Maps Places API

### Frontend

* HTML5
* CSS3
* JavaScript

---

## Project Structure

```text
MediMind_AI/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── database/
│   └── mongo.py
│
├── agents/
│   ├── symptom_agent.py
│   ├── disease_agent.py
│   ├── risk_agent.py
│   ├── emergency_agent.py
│   ├── hospital_agent.py
│   └── report_agent.py
│
├── services/
│   ├── groq_service.py
│   ├── pdf_service.py
│   ├── maps_service.py
│   ├── voice_service.py
│   ├── report_generator.py
│   └── pdf_extraction_service.py
│
├── routes/
│   ├── dashboard_routes.py
│   ├── symptom_routes.py
│   ├── hospital_routes.py
│   └── report_routes.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── symptom_checker.html
│   ├── upload_report.html
│   ├── analysis_result.html
│   └── hospital_results.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── voice.js
│       └── dashboard.js
│
├── utils/
│   ├── prompts.py
│   └── helpers.py
│
├── uploads/
│
└── generated_reports/
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/MediMind_AI.git

cd MediMind_AI
```

### Create Virtual Environment

Windows:

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install --upgrade pip setuptools wheel

pip install -r requirements.txt
```

---

## MongoDB Setup

Install MongoDB Community Server.

Start MongoDB:

```bash
mongod
```

Default connection:

```text
mongodb://localhost:27017/
```

Database:

```text
medimind_ai
```

---

## Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

MONGO_URI=mongodb://localhost:27017/

DATABASE_NAME=medimind_ai

GROQ_API_KEY=your_groq_api_key

GOOGLE_MAPS_API_KEY=your_google_maps_api_key

FLASK_DEBUG=True

FLASK_HOST=0.0.0.0

FLASK_PORT=5000
```

---

## Running the Application

```bash
python app.py
```

Application URL:

```text
http://127.0.0.1:5000
```

---

## Workflow

```text
Symptoms
        ↓
Symptom Analysis
        ↓
Disease Prediction
        ↓
Risk Assessment
        ↓
Emergency Detection
        ↓
Specialist Recommendation
        ↓
Nearby Hospital Recommendation
        ↓
Generate PDF Report
        ↓
Display Results
```

---

## Key Modules

### Symptom Analysis

Accepts user symptoms and generates detailed AI-based interpretation.

### Disease Prediction

Uses medical reasoning to identify probable conditions.

### Risk Assessment

Calculates severity and urgency levels.

### Emergency Detection

Identifies dangerous symptoms and recommends immediate action.

### Hospital Search

Uses Google Maps API to locate nearby hospitals.

### Medical Report Analysis

Parses PDF reports using pdfplumber and analyzes them using Groq LLM.

### Report Generation

Creates downloadable PDF reports using ReportLab.

---

## Security Recommendations

Before production deployment:

* Enable HTTPS
* Add CSRF protection
* Implement user authentication
* Restrict file upload size
* Validate all form inputs
* Add logging and monitoring
* Secure API keys using environment variables
* Configure MongoDB authentication

---

## Future Enhancements

* User accounts and authentication
* Medical history tracking
* Multi-language support
* Doctor appointment integration
* Health analytics charts
* Email report delivery
* OCR for scanned medical reports
* AI health chatbot
* Mobile application

---

## Disclaimer

MediMind AI is an educational and informational healthcare assistant. It is not a substitute for professional medical advice, diagnosis, or treatment. Users should always consult qualified healthcare professionals for medical concerns.

---

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to deal in the Software without restriction.
