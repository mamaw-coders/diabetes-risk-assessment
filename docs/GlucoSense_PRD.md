# GlucoSense – Product Requirements Document (PRD)

**Course:** CSST 102  
**Project:** GlucoSense - Diabetes Risk Assessment AI

---

## Document Metadata

| Field               | Value                                  |
| ------------------- | -------------------------------------- |
| **Project Name**    | GlucoSense                             |
| **Version**         | 1.0 (Finals Submission)                |
| **Status**          | Complete                               |
| **Date**            | December 30,2025                       |
| **Author**          | Mamaw Coders                           |
| **Target Audience** | General Public / Academic Review Board |

---

## 1.0 Executive Summary

### 1.1 Problem Statement

Type 2 Diabetes is a silent epidemic in the Philippines and globally. A significant portion of the population exists in a _pre-diabetic_ or high-risk state but remains undiagnosed due to the cost of medical screening, lack of awareness, and fear of invasive procedures.

Existing digital solutions often focus on management for diagnosed patients (e.g., glucometer logs) rather than accessible, early-stage detection for the general public.

### 1.2 Proposed Solution

**GlucoSense** is a web-based artificial intelligence tool designed to democratize access to health screening. By leveraging machine learning (**Random Forest Classification**) trained on over **70,000 clinical records**, the application provides users with an instant, data-driven assessment of their diabetes risk profile.

### 1.3 Success Criteria

- **Accuracy:** The underlying model achieves a recall rate sufficient to minimize false negatives (missing a high-risk patient).
- **Accessibility:** The web application loads in under **2 seconds** on standard mobile networks and requires **no user registration**.
- **Usability:** A guest user can complete the assessment and understand their risk status in **under 30 seconds**.

---

## 2.0 Goals & Non-Goals

### 2.1 Primary Goals (Sprint Scope)

- **Professional User Interface:** Develop a responsive, medical-grade interface using **Bootstrap 5** that instills trust and clarity.
- **Machine Learning Integration:** Deploy a **Python Flask backend** that serves real-time inference from a pre-trained Random Forest Classifier.
- **Localization:** Adapt the US-centric dataset (BRFSS 2015) to Filipino contexts by implementing automatic unit conversion (kg/cm → BMI).
- **Privacy-First Design:** Ensure no personal health data is persisted in a database, adhering to strict ethical standards for student projects.

### 2.2 Non-Goals (Out of Scope)

- **User Authentication:** No login, signup, or password management features.
- **Long-Term Tracking:** The system will not store historical data or track user progress.
- **Medical Diagnosis:** The tool is explicitly for screening and educational purposes only.
- **Native Mobile Application:** Limited to a responsive web application.

---

## 3.0 Stakeholders

| Role           | Description                        | Key Interests                                               |
| -------------- | ---------------------------------- | ----------------------------------------------------------- |
| **Guest User** | General public (Age 18+)           | Fast results, privacy, mobile compatibility, clear language |
| **Evaluator**  | Course Instructor / Academic Board | Model validity, code quality (PEP-8), UI polish             |
| **Developer**  | Project Team                       | Feasibility within 1-week sprint, successful deployment     |

---

## 4.0 Functional Requirements

### 4.1 AI & Backend Logic (Flask)

- **FR-01 (Inference Engine):** RESTful endpoint (`/predict`) accepts POST requests with JSON data.
- **FR-02 (Model Loading):** Backend loads `model.pkl` on startup for low-latency inference.
- **FR-03 (Input Validation):** Marshmallow schemas validate all inputs before processing.

### 4.2 User Interface (Bootstrap/HTML)

- **FR-04 (Responsive Layout):** Bootstrap Grid for mobile/desktop support.
- **FR-05 (4-Step Wizard):** Form split into: Basics → Medical History → Lifestyle → Health Status.
- **FR-06 (Result Visualization):** Risk meter, probability display, contributing factors list.

### 4.3 Business Logic & Localization

- **FR-07 (BMI Calculation):** `BMI = weight_kg / (height_cm / 100)²`
- **FR-08 (Age Mapping):** Maps age to BRFSS categorical integers (1-13 scale).

---

## 5.0 System Architecture

Decoupled frontend/backend architecture for independent deployment.

### 5.1 Technology Stack

| Layer                        | Technologies                                                    |
| ---------------------------- | --------------------------------------------------------------- |
| **Frontend (View)**          | HTML5, CSS3, Bootstrap 5.3, Vanilla JavaScript (ES6+)           |
| **Backend (Controller)**     | Python 3.9+, Flask, Marshmallow (Validation)                    |
| **Machine Learning (Model)** | Scikit-Learn (Random Forest Classifier), Joblib (Serialization) |
| **Infrastructure**           | Render (Backend), Static hosting (Frontend)                     |

### 5.2 Data Flow

```
┌─────────────────┐                    ┌─────────────────┐
│     Client      │                    │     Server      │
│  (Bootstrap 5)  │                    │    (Flask)      │
└────────┬────────┘                    └────────┬────────┘
         │  1. POST /predict (JSON)             │
         │─────────────────────────────────────>│
         │                              2. Validate
         │                              3. Calculate BMI
         │                              4. model.predict()
         │  5. JSON response                    │
         │<─────────────────────────────────────│
         │  6. Render results                   │
```

---

## 6.0 Data Dictionary

| UI Label           | Field Name           | Data Type  | Notes                     |
| ------------------ | -------------------- | ---------- | ------------------------- |
| Age                | `age`                | Int        | User's age                |
| Sex                | `sex`                | String     | "male" / "female"         |
| Weight             | `weight`             | Float      | Kilograms                 |
| Height             | `height`             | Float      | Centimeters               |
| High BP            | `high_bp`            | Boolean    | Hypertension history      |
| High Cholesterol   | `high_chol`          | Boolean    | Elevated LDL              |
| Heart Disease      | `heart_disease`      | Boolean    | CHD or heart attack       |
| Stroke             | `stroke`             | Boolean    | History of stroke         |
| Smoker             | `smoker`             | Boolean    | 100+ cigarettes lifetime  |
| Heavy Alcohol      | `heavy_alcohol`      | Boolean    | Heavy consumption         |
| Physical Activity  | `phys_activity`      | Boolean    | Exercise in past 30 days  |
| Fruits             | `fruits`             | Boolean    | Daily fruit intake        |
| Veggies            | `veggies`            | Boolean    | Daily vegetable intake    |
| General Health     | `general_health`     | Int (1-5)  | 1=Excellent, 5=Poor       |
| Mental Health      | `mental_health`      | Int (0-30) | Poor mental health days   |
| Physical Health    | `physical_health`    | Int (0-30) | Poor physical health days |
| Difficulty Walking | `difficulty_walking` | Boolean    | Mobility issues           |

---

## 7.0 UI/UX Design

### 7.1 Design Philosophy

Clean, medical-grade interface with a **4-step wizard** to reduce cognitive load.

### 7.2 Page Sections

| Section      | Description                           |
| ------------ | ------------------------------------- |
| Hero         | Landing with image collage            |
| How It Works | 3-step process explanation            |
| About        | Early detection benefits              |
| Assessment   | 4-step wizard form                    |
| Results      | Risk meter, BMI, contributing factors |
| FAQ          | Accordion with common questions       |
| Footer       | Disclaimer, credits                   |

---

## 8.0 Development Sprint (7 Days)

| Day | Phase             | Activities                           |
| --- | ----------------- | ------------------------------------ |
| 1   | Data Engineering  | Train model, export `model.pkl`      |
| 2   | Backend Setup     | Flask routes, Marshmallow validation |
| 3   | Frontend Skeleton | Bootstrap layout, HTML form          |
| 4   | Logic Integration | JavaScript modules, BMI calculation  |
| 5   | Model Wiring      | Connect frontend to API              |
| 6   | Deployment        | Deploy to Render + static hosting    |
| 7   | Quality Assurance | Testing, polish, final submission    |

---

## 9.0 Risks & Mitigations

| Risk             | Mitigation                                         |
| ---------------- | -------------------------------------------------- |
| Deployment       | Allocate Day 6 entirely, follow verified tutorials |
| Model Bias       | State BRFSS 2015 US data limitation in footer      |
| User Input Error | HTML5 validation + Marshmallow backend validation  |

---

## Appendix: Architecture Decision

> This project uses a **decoupled architecture** (Static HTML + REST API) instead of Flask/Jinja templates. Benefits:
>
> - Independent frontend/backend deployment
> - Better separation of concerns
> - Modern industry-standard patterns
> - Potential for future mobile app integration
