document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.multi-step-form'); 
    if (!form) {
        console.error("Form element not found.");
        return;
    }

    console.log("Form found:", form);

    const progressBar = form.querySelector('.progress-bar');
    const steps = form.querySelectorAll('.step');
    let currentStep = 0;

    const updateProgress = () => {
        const progress = ((currentStep) / steps.length) * 100;
        const progressDecimal = progress.toFixed(0);
        progressBar.style.width = progressDecimal + '%';
        progressBar.setAttribute('aria-valuenow', progressDecimal);
        progressBar.textContent = progressDecimal + '%'; 
    };
    

    const showStep = (stepNumber) => {
        steps.forEach((step, index) => {
            if (index === stepNumber) {
                step.style.display = 'block';
            } else {
                step.style.display = 'none';
            }
        });
        currentStep = stepNumber;
        updateProgress();
    };

    const goToNextStep = () => {
        if (currentStep < steps.length - 1) {
            showStep(currentStep + 1);
        }
    };

    const goToPrevStep = () => {
        if (currentStep > 0) {
            showStep(currentStep - 1);
        }
    };

    form.querySelectorAll('.next').forEach(button => {
        button.addEventListener('click', goToNextStep);
    });

    form.querySelectorAll('.prev').forEach(button => {
        button.addEventListener('click', goToPrevStep);
    });

    showStep(currentStep);
});
