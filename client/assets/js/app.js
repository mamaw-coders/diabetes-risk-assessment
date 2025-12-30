/**
 * Diabetes Risk Assessment - Main Application
 * 
 * Simplified boilerplate for initial development.
 */

// API Configuration
const API_URL = 'http://localhost:5000';

// DOM Elements
const form = document.getElementById('assessmentForm');
const resultsSection = document.getElementById('resultsSection');
const riskIndicator = document.getElementById('riskIndicator');
const retakeBtn = document.getElementById('retakeBtn');

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', () => {
    form.addEventListener('submit', handleSubmit);
    retakeBtn.addEventListener('click', resetForm);
});

/**
 * Handle form submission
 */
async function handleSubmit(e) {
    e.preventDefault();
    
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }

    const formData = collectFormData();
    
    try {
        const result = await predictRisk(formData);
        displayResults(result);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

/**
 * Collect form data
 */
function collectFormData() {
    return {
        age: parseInt(document.getElementById('age').value),
        sex: document.getElementById('sex').value,
        weight: parseFloat(document.getElementById('weight').value),
        height: parseFloat(document.getElementById('height').value),
        high_bp: document.getElementById('highBp').checked,
        high_chol: document.getElementById('highChol').checked,
        smoker: document.getElementById('smoker').checked,
        heart_disease: document.getElementById('heartDisease').checked,
        general_health: parseInt(document.getElementById('generalHealth').value),
        phys_activity: document.getElementById('physActivity').checked,
        // Defaults for simplified form
        stroke: false,
        fruits: true,
        veggies: true,
        heavy_alcohol: false,
        mental_health: 0,
        physical_health: 0,
        difficulty_walking: false
    };
}

/**
 * Send prediction request to API
 */
async function predictRisk(data) {
    const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        throw new Error('Prediction failed');
    }
    
    return response.json();
}

/**
 * Display results
 */
function displayResults(result) {
    const isHighRisk = result.risk_level === 'HIGH';
    
    riskIndicator.innerHTML = `
        <div class="alert alert-${isHighRisk ? 'danger' : 'success'} fs-4">
            <i class="bi bi-${isHighRisk ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
            <strong>${result.risk_level} RISK</strong>
        </div>
        <p class="text-muted">Probability: ${(result.probability * 100).toFixed(1)}%</p>
        <p class="text-muted">BMI: ${result.bmi.toFixed(1)} (${result.bmi_category})</p>
    `;
    
    form.closest('.col-lg-8').querySelector('form').classList.add('d-none');
    resultsSection.classList.remove('d-none');
}

/**
 * Reset to form view
 */
function resetForm() {
    form.reset();
    form.classList.remove('was-validated', 'd-none');
    resultsSection.classList.add('d-none');
}
