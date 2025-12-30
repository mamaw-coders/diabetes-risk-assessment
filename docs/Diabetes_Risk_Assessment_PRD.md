# Diabetes Risk Assessment AI – Product Requirements Document (PRD)

**Course:** CSST 101  
**Project:** Diabetes Risk Assessment AI (Sprint Edition)

---

## Document Metadata

| Field               | Value                                   |
| ------------------- | --------------------------------------- |
| **Project Name**    | Diabetes Risk Predictor (Flask Edition) |
| **Version**         | 1.0 (Finals Submission)                 |
| **Status**          | In Development                          |
| **Date**            | December 30, 2025                       |
| **Author**          | Mamaw Coders                            |
| **Target Audience** | General Public / Academic Review Board  |

---

## 1.0 Executive Summary

### 1.1 Problem Statement

Type 2 Diabetes is a silent epidemic in the Philippines and globally. A significant portion of the population exists in a _pre-diabetic_ or high-risk state but remains undiagnosed due to the cost of medical screening, lack of awareness, and fear of invasive procedures.

Existing digital solutions often focus on management for diagnosed patients (e.g., glucometer logs) rather than accessible, early-stage detection for the general public.

### 1.2 Proposed Solution

The **Diabetes Risk Predictor** is a web-based artificial intelligence tool designed to democratize access to health screening. By leveraging machine learning (**Random Forest Classification**) trained on over **70,000 clinical records**, the application provides users with an instant, data-driven assessment of their diabetes risk profile.

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

- **User Authentication:** No login, signup, or password management features will be implemented to reduce user friction.
- **Long-Term Tracking:** The system will not store historical data or track user progress over time.
- **Medical Diagnosis:** The tool is explicitly for screening and educational purposes, not for medical diagnosis or prescription.
- **Native Mobile Application:** The project is limited to a responsive web application; no iOS/Android binaries will be released.

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

- **FR-01 (Inference Engine):** The application shall expose a RESTful endpoint (`/predict`) capable of accepting POST requests containing JSON data.
- **FR-02 (Model Loading):** The backend must load the serialized model artifact (`model.pkl`) into memory upon application startup to ensure low-latency inference.
- **FR-03 (Input Validation):** The system must sanitize all inputs to prevent errors (e.g., ensuring Age > 0, Weight > 0) before passing data to the model.

### 4.2 User Interface (Bootstrap/HTML)

- **FR-04 (Responsive Layout):** The input form shall utilize the Bootstrap Grid System to stack interface elements vertically on mobile devices and horizontally on desktops.
- **FR-05 (Grouped Inputs):** Inputs shall be logically categorized into distinct sections: "Demographics," "Vitals," "Medical History," "Lifestyle," and "Health Status," using Bootstrap Cards.
- **FR-06 (Result Visualization):** Inference results must be displayed prominently via a styled results section (Green for Low Risk, Red for High Risk), appearing immediately after form submission.

### 4.3 Business Logic & Localization

- **FR-07 (BMI Calculation):** The application must accept Weight in Kilograms (kg) and Height in Centimeters (cm). The system will execute the following transformation before inference:
  ```
  BMI = weight_kg / (height_cm / 100)²
  ```
- **FR-08 (Age Mapping):** The system must map user-provided age values to the specific categorical integers required by the BRFSS dataset schema (1-13 scale).

---

## 5.0 System Architecture

The application follows a **decoupled frontend/backend architecture** for independent deployment and scalability.

### 5.1 Technology Stack

| Layer                        | Technologies                                                         |
| ---------------------------- | -------------------------------------------------------------------- |
| **Frontend (View)**          | HTML5, CSS3, Bootstrap 5.3 (UI Framework), Vanilla JavaScript (ES6+) |
| **Backend (Controller)**     | Python 3.9+, Flask (Micro-framework), Marshmallow (Validation)       |
| **Machine Learning (Model)** | Scikit-Learn (Random Forest Classifier), Joblib (Serialization)      |
| **Infrastructure**           | Render (Cloud PaaS) or similar Python-compatible hosting             |

### 5.2 Data Flow

```
┌─────────────────┐                    ┌─────────────────┐
│     Client      │                    │     Server      │
│  (Bootstrap 5)  │                    │    (Flask)      │
└────────┬────────┘                    └────────┬────────┘
         │                                      │
         │  1. User submits form                │
         │─────────────────────────────────────>│
         │     POST /predict (JSON)             │
         │                                      │
         │                              2. Validate inputs
         │                              3. Calculate BMI
         │                              4. model.predict()
         │                                      │
         │  5. Return JSON response             │
         │<─────────────────────────────────────│
         │     {risk_level, probability, ...}   │
         │                                      │
         │  6. Render results in UI             │
         │                                      │
```

---

## 6.0 Data Dictionary & Schema

The following table defines how user inputs are mapped to the machine learning model's expected features.

| UI Label           | HTML `name` Attribute | Python Variable   | Dataset Feature      | Data Type    | Notes                        |
| ------------------ | --------------------- | ----------------- | -------------------- | ------------ | ---------------------------- |
| High BP            | `high_bp`             | `high_bp`         | HighBP               | Binary (0/1) | History of Hypertension      |
| High Cholesterol   | `high_chol`           | `high_chol`       | HighChol             | Binary (0/1) | History of High Cholesterol  |
| Weight (kg)        | `weight`              | `weight`          | BMI                  | Float        | Used to calculate BMI        |
| Height (cm)        | `height`              | `height`          | BMI                  | Float        | Used to calculate BMI        |
| Smoker             | `smoker`              | `smoker`          | Smoker               | Binary (0/1) | Smoked >100 cigs in lifetime |
| History of Stroke  | `stroke`              | `stroke`          | Stroke               | Binary (0/1) | Ever diagnosed with stroke   |
| Heart Disease      | `heart_disease`       | `heart_disease`   | HeartDiseaseorAttack | Binary (0/1) | Coronary Heart Disease / MI  |
| Physically Active  | `phys_activity`       | `phys_activity`   | PhysActivity         | Binary (0/1) | Exercise in past 30 days     |
| General Health     | `general_health`      | `gen_hlth`        | GenHlth              | Int (1-5)    | 1=Excellent, 5=Poor          |
| Age                | `age`                 | `age`             | Age                  | Int (1-13)   | 1=18-24 ... 13=80+           |
| Sex                | `sex`                 | `sex`             | Sex                  | Binary (0/1) | 0=Female, 1=Male             |
| Mental Health      | `mental_health`       | `mental_health`   | MentHlth             | Int (0-30)   | Poor mental health days      |
| Physical Health    | `physical_health`     | `physical_health` | PhysHlth             | Int (0-30)   | Poor physical health days    |
| Difficulty Walking | `difficulty_walking`  | `diff_walk`       | DiffWalk             | Binary (0/1) | Difficulty walking/climbing  |
| Fruits             | `fruits`              | `fruits`          | Fruits               | Binary (0/1) | Consumes fruit daily         |
| Veggies            | `veggies`             | `veggies`         | Veggies              | Binary (0/1) | Consumes vegetables daily    |
| Heavy Alcohol      | `heavy_alcohol`       | `heavy_alcohol`   | HvyAlcoholConsump    | Binary (0/1) | Heavy alcohol consumption    |

---

## 7.0 UI/UX Design Specification

### 7.1 Design Philosophy

The interface mimics a standard medical form—clean, sterile, and trustworthy. We utilize a **card-based layout** to reduce cognitive load.

### 7.2 Interface Structure

**Header (Hero Section):**

- Title: "Diabetes Risk Assessment AI"
- Subtitle: Brief description of the tool's purpose
- Key statistics (70K+ records, <30s assessment)

**Form Section:**

- **Card A (Demographics):** Age Input, Sex Dropdown
- **Card B (Vitals):** Weight (kg) Input, Height (cm) Input, Live BMI Preview
- **Card C (Medical History):** Toggle cards for BP, Cholesterol, Stroke, Heart Disease
- **Card D (Lifestyle):** Toggle cards for Smoking, Physical Activity, Diet, Alcohol
- **Card E (Health Status):** General Health dropdown, Mental/Physical health days

**Results Section:**

- Risk level indicator (circle with icon)
- Probability bar
- BMI display with category
- Contributing factors list
- Medical disclaimer

**Footer:**

- Disclaimer: "For educational purposes only. Not a substitute for professional medical advice."
- Attribution: Built by Mamaw Coders, Data from CDC BRFSS 2015

---

## 8.0 Development Sprint Plan (7 Days)

| Day   | Phase             | Key Activities                                                                                             |
| ----- | ----------------- | ---------------------------------------------------------------------------------------------------------- |
| **1** | Data Engineering  | Load `diabetes_binary_5050split.csv`. Train Random Forest model. Evaluate metrics. Export `model.pkl`.     |
| **2** | Backend Setup     | Initialize Flask `app.py`. Create routes. Implement Marshmallow validation. Test local server.             |
| **3** | Frontend Skeleton | Create `index.html`. Implement Bootstrap 5 layout. Build HTML form with all input sections.                |
| **4** | Logic Integration | Create JavaScript modules (api.js, form.js, results.js). Implement BMI calculation. Debug input handling.  |
| **5** | Model Wiring      | Load `model.pkl` in Flask. Implement prediction service. Connect frontend to API. Return results to UI.    |
| **6** | Deployment        | Create `requirements.txt`. Push code to GitHub. Deploy backend to Render. Deploy frontend to GitHub Pages. |
| **7** | Quality Assurance | Mobile responsiveness testing. Add visual polish (colors, icons, animations). Final submission.            |

---

## 9.0 Risks & Mitigations

| Risk Area            | Risk Description                                                                                             | Mitigation Strategy                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **Deployment**       | Hosting Flask on free-tier services (Render) can be complex compared to Streamlit.                           | Allocate Day 6 entirely to deployment. Follow a verified "Flask to Render" tutorial.           |
| **Model Bias**       | The model is trained on US data (BRFSS 2015), which may not accurately reflect Filipino physiological norms. | Explicitly state this limitation in the application footer and presentation slides.            |
| **User Input Error** | Users may input unrealistic values (e.g., Weight: 5kg) which could skew predictions.                         | Implement HTML5 form validation (`min`, `max`, `required`) and backend Marshmallow validation. |

---

## Appendix: Architecture Decision

> **Note:** This project uses a **decoupled architecture** (Static HTML + REST API) instead of traditional Flask/Jinja templates. This decision enables:
>
> - Independent frontend/backend deployment
> - Better separation of concerns
> - Modern industry-standard patterns
> - Potential for future mobile app integration
