document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    
    const resultContainer = document.getElementById('result-container');
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const resultMessage = document.getElementById('result-message');
    
    const probContainer = document.getElementById('prob-container');
    const probValue = document.getElementById('prob-value');
    const probFill = document.getElementById('prob-fill');
    
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');

    // SVG Icons
    const successIcon = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
    `;

    const dangerIcon = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
    `;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI State
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        probContainer.classList.add('hidden');
        
        // Set Loading State
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';

        const payload = {
            cgpa: parseFloat(document.getElementById('cgpa').value),
            internships: parseInt(document.getElementById('internships').value),
            projects: parseInt(document.getElementById('projects').value),
            communication: parseFloat(document.getElementById('communication').value)
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                let errorMessage = 'Failed to get prediction from server.';
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.error || errorMessage;
                } catch (e) {
                    errorMessage = `Server Error: ${response.status} ${response.statusText}. Please check the server logs.`;
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();

            // Artificial delay to show off the cool loader (optional, remove in prod)
            await new Promise(resolve => setTimeout(resolve, 800));

            displayResult(data);

        } catch (error) {
            displayError(error.message);
        } finally {
            // Restore Button State
            submitBtn.disabled = false;
            btnText.style.display = 'block';
            btnLoader.style.display = 'none';
        }
    });

    function displayResult(data) {
        resultContainer.classList.remove('hidden');
        
        const isPlaced = data.prediction === 1;
        let displayProb = data.probability;
        if (!isPlaced && displayProb !== null) {
            displayProb = 1 - displayProb;
        }
        const probability = displayProb !== null ? (displayProb * 100).toFixed(1) : null;

        // Reset classes
        resultIcon.parentElement.className = 'result-icon-wrapper';
        resultTitle.className = '';
        probFill.className = 'prob-bar-fill';

        if (isPlaced) {
            resultIcon.innerHTML = successIcon;
            resultIcon.parentElement.classList.add('icon-success');
            resultTitle.textContent = "High Chances of Placement!";
            resultTitle.classList.add('text-success');
            resultMessage.textContent = "Your academic profile looks strong. Keep up the good work!";
            probFill.classList.add('fill-success');
        } else {
            resultIcon.innerHTML = dangerIcon;
            resultIcon.parentElement.classList.add('icon-danger');
            resultTitle.textContent = "Needs Improvement";
            resultTitle.classList.add('text-danger');
            resultMessage.textContent = "Focus on improving your skills, projects, or gaining more experience.";
            probFill.classList.add('fill-danger');
        }

        if (probability !== null) {
            probContainer.classList.remove('hidden');
            probValue.textContent = `${probability}%`;
            
            // Animate width
            setTimeout(() => {
                probFill.style.width = `${probability}%`;
            }, 50);
        }
    }

    function displayError(message) {
        errorContainer.classList.remove('hidden');
        errorMessage.textContent = message;
    }
});
