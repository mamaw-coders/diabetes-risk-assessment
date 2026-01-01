/**
 * Diabetes Risk Assessment App
 * Handles wizard navigation, validation, and API interaction.
 */

document.addEventListener('DOMContentLoaded', () => {
    // State
    let currentStep = 1;
    const totalSteps = 4;
    
    // Elements
    const form = document.getElementById('riskForm');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const progressBar = document.getElementById('progressBar');
    const resultsView = document.getElementById('resultsView');
    const progressSteps = document.querySelectorAll('.progress-step');
    
    // Initialize
    updateWizardUI();
    
    // Event Listeners
    nextBtn.addEventListener('click', handleNext);
    prevBtn.addEventListener('click', handlePrev);
    
    /**
     * Handle Next Button Click
     */
    async function handleNext() {
        if (!validateStep(currentStep)) {
            return;
        }
        
        if (currentStep < totalSteps) {
            currentStep++;
            updateWizardUI();
        } else {
            await submitPrediction();
        }
    }
    
    /**
     * Handle Previous Button Click
     */
    function handlePrev() {
        if (currentStep > 1) {
            currentStep--;
            updateWizardUI();
        }
    }
    
    /**
     * Update UI based on current step
     */
    function updateWizardUI() {
        // Update Progress Bar
        const progress = (currentStep / totalSteps) * 100;
        progressBar.style.width = `${progress}%`;
        
        // Update Progress Steps
        progressSteps.forEach((step, index) => {
            const stepNum = index + 1;
            step.classList.remove('active', 'completed');
            
            if (stepNum < currentStep) {
                step.classList.add('completed');
            } else if (stepNum === currentStep) {
                step.classList.add('active');
            }
        });
        
        // Show/Hide Steps
        document.querySelectorAll('.form-step').forEach(step => {
            step.classList.add('d-none');
            step.classList.remove('active');
            
            if (parseInt(step.dataset.step) === currentStep) {
                step.classList.remove('d-none');
                step.classList.add('active');
            }
        });
        
        // Update Buttons
        prevBtn.disabled = currentStep === 1;
        
        if (currentStep === totalSteps) {
            nextBtn.innerHTML = `
                Calculate Risk
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
            `;
        } else {
            nextBtn.innerHTML = `
                Next Step
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            `;
        }
    }
    
    /**
     * Validate inputs for the current step
     */
    function validateStep(step) {
        const stepEl = document.querySelector(`.form-step[data-step="${step}"]`);
        const inputs = stepEl.querySelectorAll('input[required], select[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value || input.value === '') {
                isValid = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    }
    
    /**
     * Collect data and call API
     */
    async function submitPrediction() {
        // UI Loading State
        nextBtn.disabled = true;
        nextBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status"></span>
            Processing...
        `;
        
        try {
            const formData = new FormData(form);
            const payload = buildPayload(formData);
            
            const API_URL = window.location.hostname === 'localhost' 
                ? 'http://localhost:5000/predict'
                : 'https://glucosense-api-u95g.onrender.com/predict';
            
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || 'Prediction failed');
            }
            
            const result = await response.json();
            showResults(result);
            
        } catch (error) {
            alert('Error: ' + error.message);
            nextBtn.disabled = false;
            nextBtn.innerHTML = 'Calculate Risk';
        }
    }
    
    /**
     * Transform FormData to API Schema
     */
    function buildPayload(formData) {
        const getBool = (name) => {
            const val = formData.get(name);
            return val === 'on' || val === 'true';
        };
        
        return {
            age: parseInt(formData.get('age')),
            sex: formData.get('sex'),
            weight: parseFloat(formData.get('weight')),
            height: parseFloat(formData.get('height')),
            
            high_bp: getBool('high_bp'),
            high_chol: getBool('high_chol'),
            heart_disease: getBool('heart_disease'),
            stroke: getBool('stroke'),
            
            smoker: getBool('smoker'),
            heavy_alcohol: getBool('heavy_alcohol'),
            phys_activity: getBool('phys_activity'),
            fruits: getBool('fruits'),
            veggies: getBool('veggies'),
            
            general_health: parseInt(formData.get('general_health')),
            mental_health: parseInt(formData.get('mental_health')),
            physical_health: parseInt(formData.get('physical_health')),
            difficulty_walking: getBool('difficulty_walking')
        };
    }
    
    /**
     * Display Results
     */
    function showResults(data) {
        form.classList.add('d-none');
        document.querySelector('.wizard-nav').classList.add('d-none');
        document.querySelector('.wizard-progress').classList.add('d-none');
        resultsView.classList.remove('d-none');
        
        // Set print date
        const printDate = new Date().toLocaleDateString('en-US', { 
            year: 'numeric', month: 'long', day: 'numeric' 
        });
        document.querySelector('.wizard-body').setAttribute('data-date', printDate);
        
        const titleEl = document.getElementById('resultTitle');
        const probEl = document.getElementById('resultProbability');
        const iconWrapper = document.getElementById('resultIconWrapper');
        const iconSvg = document.getElementById('resultIconSvg');
        const listEl = document.getElementById('factorsList');
        const meterFill = document.getElementById('riskMeterFill');
        const meterMarker = document.getElementById('riskMeterMarker');
        
        const probability = data.probability * 100;
        
        // Update icon and title based on risk
        if (data.risk_level === 'HIGH') {
            titleEl.textContent = 'Elevated Risk Detected';
            titleEl.style.color = '#EF4444';
            iconWrapper.classList.add('high-risk');
            iconSvg.innerHTML = '<circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/>';
        } else {
            titleEl.textContent = 'Lower Risk Profile';
            titleEl.style.color = '#10B981';
            iconWrapper.classList.add('low-risk');
            iconSvg.innerHTML = '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>';
        }
        
        probEl.textContent = `${probability.toFixed(1)}% estimated probability`;
        
        // Update risk meter
        meterFill.style.width = `${probability}%`;
        meterMarker.style.left = `${probability}%`;
        
        // Set meter color based on probability
        if (probability >= 50) {
            meterFill.style.background = 'linear-gradient(90deg, #FCD34D, #EF4444)';
        } else if (probability >= 30) {
            meterFill.style.background = 'linear-gradient(90deg, #A3E635, #FCD34D)';
        } else {
            meterFill.style.background = 'linear-gradient(90deg, #10B981, #A3E635)';
        }
        
        // Update BMI and Risk Level stats
        document.getElementById('resultBmi').textContent = data.bmi.toFixed(1);
        document.getElementById('resultBmiCategory').textContent = data.bmi_category;
        document.getElementById('resultRiskLevel').textContent = data.risk_level;
        document.getElementById('resultRiskDesc').textContent = 
            data.risk_level === 'HIGH' ? 'Consult a healthcare provider' : 'Continue healthy habits';
        
        // Update factors list
        listEl.innerHTML = '';
        if (data.contributing_factors && data.contributing_factors.length > 0) {
            data.contributing_factors.forEach(factor => {
                const li = document.createElement('li');
                li.textContent = factor;
                listEl.appendChild(li);
            });
        } else {
            listEl.innerHTML = '<li>No major risk factors identified based on your inputs.</li>';
        }

        document.getElementById('disclaimerText').textContent = data.disclaimer;
    }
});

