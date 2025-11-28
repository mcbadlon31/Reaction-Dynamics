document.addEventListener('DOMContentLoaded', () => {
    const preExpInput = document.getElementById('pre-exponential');
    const activationEnergyInput = document.getElementById('activation-energy');
    const temperatureInput = document.getElementById('temperature');
    const tempDisplay = document.getElementById('temp-display');
    const rateResult = document.getElementById('rate-result');

    const R = 8.314; // Gas constant in J/(mol*K)

    function calculateRate() {
        const A = parseFloat(preExpInput.value);
        const Ea_kJ = parseFloat(activationEnergyInput.value);
        const T = parseFloat(temperatureInput.value);

        if (isNaN(A) || isNaN(Ea_kJ) || isNaN(T)) {
            rateResult.textContent = "Invalid Input";
            return;
        }

        // Convert Ea from kJ/mol to J/mol
        const Ea = Ea_kJ * 1000;

        // Arrhenius Equation: k = A * exp(-Ea / (R * T))
        const k = A * Math.exp(-Ea / (R * T));

        // Format the result
        rateResult.textContent = k.toExponential(3) + " s⁻¹";
        tempDisplay.textContent = T + " K";
    }

    // Add event listeners
    preExpInput.addEventListener('input', calculateRate);
    activationEnergyInput.addEventListener('input', calculateRate);
    temperatureInput.addEventListener('input', calculateRate);

    // Initial calculation
    calculateRate();
});
