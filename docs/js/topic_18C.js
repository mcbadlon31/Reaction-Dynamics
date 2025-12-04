/**
 * Topic 18C: Transition-State Theory
 * Interactive elements script
 */

// ==========================================================================
// 1. Eyring Plot Generator
// ==========================================================================
const EyringPlot = {
    init: function () {
        const container = document.getElementById('eyringPlot');
        if (!container) return;

        this.sliderH = document.getElementById('sliderH');
        this.sliderS = document.getElementById('sliderS');
        this.displayH = document.getElementById('displayH');
        this.displayS = document.getElementById('displayS');

        this.sliderH.addEventListener('input', () => this.updatePlot());
        this.sliderS.addEventListener('input', () => this.updatePlot());

        this.updatePlot();
    },

    updatePlot: function () {
        const dH = parseFloat(this.sliderH.value); // kJ/mol
        const dS = parseFloat(this.sliderS.value); // J/(mol K)

        this.displayH.textContent = dH;
        this.displayS.textContent = dS;

        // Constants
        const R = 8.314; // J/(mol K)
        const kB = 1.380649e-23;
        const h = 6.62607015e-34;
        const ln_kB_h = Math.log(kB / h); // approx 23.76

        // Generate data for Eyring Plot: ln(k/T) vs 1/T
        // Equation: ln(k/T) = -dH/R * (1/T) + (dS/R + ln(kB/h))

        const xValues = []; // 1/T
        const yValues = []; // ln(k/T)

        // Temperature range: 200K to 400K
        // 1/T range: 0.0025 to 0.005

        for (let T = 200; T <= 400; T += 10) {
            const invT = 1 / T;
            const ln_k_T = -(dH * 1000 / R) * invT + (dS / R + ln_kB_h);

            xValues.push(invT);
            yValues.push(ln_k_T);
        }

        const trace = {
            x: xValues,
            y: yValues,
            mode: 'lines',
            name: 'Eyring Plot',
            line: { color: '#3b82f6', width: 3 }
        };

        const layout = {
            title: 'Eyring Plot: ln(k/T) vs 1/T',
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#f1f5f9' },
            xaxis: {
                title: '1/T (K⁻¹)',
                gridcolor: '#334155',
                tickformat: '.4f'
            },
            yaxis: {
                title: 'ln(k/T)',
                gridcolor: '#334155'
            },
            margin: { t: 40, r: 20, b: 50, l: 60 },
            annotations: [
                {
                    x: xValues[Math.floor(xValues.length / 2)],
                    y: yValues[Math.floor(yValues.length / 2)],
                    text: `Slope = -ΔH‡/R = -${(dH * 1000 / R).toFixed(0)} K`,
                    showarrow: true,
                    arrowhead: 2,
                    ax: 0,
                    ay: -40,
                    font: { color: '#f1f5f9' }
                }
            ]
        };

        Plotly.newPlot('eyringPlot', [trace], layout, { displayModeBar: false });
    }
};

// ==========================================================================
// 2. Activation Entropy Visualizer
// ==========================================================================
const EntropyVisualizer = {
    canvas: null,
    ctx: null,
    particles: [],
    mode: 'associative', // 'associative' or 'dissociative'
    animationId: null,

    init: function () {
        this.canvas = document.getElementById('entropyCanvas');
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');

        document.getElementById('btnAssoc').addEventListener('click', () => this.setMode('associative'));
        document.getElementById('btnDissoc').addEventListener('click', () => this.setMode('dissociative'));

        this.resize();
        window.addEventListener('resize', () => this.resize());

        this.setMode('associative');
        this.animate();
    },

    resize: function () {
        if (!this.canvas) return;
        const rect = this.canvas.parentElement.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = 300;
        this.initParticles();
    },

    setMode: function (mode) {
        this.mode = mode;
        document.getElementById('btnAssoc').classList.toggle('active', mode === 'associative');
        document.getElementById('btnDissoc').classList.toggle('active', mode === 'dissociative');
        this.initParticles();
    },

    initParticles: function () {
        this.particles = [];
        const w = this.canvas.width;
        const h = this.canvas.height;

        if (this.mode === 'associative') {
            // Two particles coming together to form an ordered complex
            // We'll simulate many pairs
            for (let i = 0; i < 10; i++) {
                this.particles.push({
                    x1: Math.random() * w,
                    y1: Math.random() * h,
                    x2: Math.random() * w,
                    y2: Math.random() * h,
                    targetX: Math.random() * w,
                    targetY: Math.random() * h,
                    phase: Math.random() * Math.PI * 2,
                    speed: 0.02 + Math.random() * 0.02
                });
            }
        } else {
            // One particle breaking into two (disordered)
            for (let i = 0; i < 10; i++) {
                this.particles.push({
                    x: Math.random() * w,
                    y: Math.random() * h,
                    angle: Math.random() * Math.PI * 2,
                    separation: 0,
                    phase: Math.random() * Math.PI * 2,
                    speed: 0.02 + Math.random() * 0.02
                });
            }
        }
    },

    draw: function () {
        const w = this.canvas.width;
        const h = this.canvas.height;
        this.ctx.clearRect(0, 0, w, h);

        const time = Date.now() * 0.001;

        if (this.mode === 'associative') {
            // Draw pairs coming together
            this.ctx.fillStyle = '#60a5fa';
            this.ctx.strokeStyle = '#60a5fa';

            for (let p of this.particles) {
                // Oscillate between separated and joined
                const t = (Math.sin(time * p.speed * 20 + p.phase) + 1) / 2; // 0 to 1

                // Interpolate positions
                const curX1 = p.x1 + (p.targetX - 10 - p.x1) * t;
                const curY1 = p.y1 + (p.targetY - p.y1) * t;

                const curX2 = p.x2 + (p.targetX + 10 - p.x2) * t;
                const curY2 = p.y2 + (p.targetY - p.y2) * t;

                this.ctx.beginPath();
                this.ctx.arc(curX1, curY1, 8, 0, Math.PI * 2);
                this.ctx.fill();

                this.ctx.beginPath();
                this.ctx.arc(curX2, curY2, 8, 0, Math.PI * 2);
                this.ctx.fill();

                if (t > 0.8) {
                    // Draw "bond" or interaction when close
                    this.ctx.beginPath();
                    this.ctx.moveTo(curX1, curY1);
                    this.ctx.lineTo(curX2, curY2);
                    this.ctx.lineWidth = 2;
                    this.ctx.stroke();

                    // Label TS
                    if (t > 0.95) {
                        this.ctx.fillStyle = 'white';
                        this.ctx.font = '12px Inter';
                        this.ctx.fillText('TS', (curX1 + curX2) / 2 - 8, (curY1 + curY2) / 2 - 10);
                        this.ctx.fillStyle = '#60a5fa';
                    }
                }
            }

            this.ctx.fillStyle = 'white';
            this.ctx.fillText('Associative: A + B → [A-B]‡ (Ordered)', 10, 20);

        } else {
            // Draw molecule vibrating/breaking
            this.ctx.fillStyle = '#ef4444';
            this.ctx.strokeStyle = '#ef4444';

            for (let p of this.particles) {
                // Oscillate separation
                const t = (Math.sin(time * p.speed * 20 + p.phase) + 1) / 2; // 0 to 1
                const sep = 10 + t * 30; // 10 to 40px separation

                const dx = Math.cos(p.angle) * sep / 2;
                const dy = Math.sin(p.angle) * sep / 2;

                const x1 = p.x - dx;
                const y1 = p.y - dy;
                const x2 = p.x + dx;
                const y2 = p.y + dy;

                this.ctx.beginPath();
                this.ctx.arc(x1, y1, 8, 0, Math.PI * 2);
                this.ctx.fill();

                this.ctx.beginPath();
                this.ctx.arc(x2, y2, 8, 0, Math.PI * 2);
                this.ctx.fill();

                // Bond stretches then breaks
                if (t < 0.8) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(x1, y1);
                    this.ctx.lineTo(x2, y2);
                    this.ctx.lineWidth = 3 * (1 - t); // Gets thinner
                    this.ctx.stroke();
                } else {
                    this.ctx.fillStyle = 'white';
                    this.ctx.font = '12px Inter';
                    this.ctx.fillText('TS', p.x - 8, p.y - 10);
                    this.ctx.fillStyle = '#ef4444';
                }
            }

            this.ctx.fillStyle = 'white';
            this.ctx.fillText('Dissociative: A-B → [A...B]‡ (Disordered)', 10, 20);
        }
    },

    animate: function () {
        this.draw();
        this.animationId = requestAnimationFrame(() => this.animate());
    }
};

// ==========================================================================
// 3. Kinetic Salt Effect Calculator
// ==========================================================================
const SaltEffect = {
    init: function () {
        const container = document.getElementById('saltEffectPlot');
        if (!container) return;

        this.selectZa = document.getElementById('selectZa');
        this.selectZb = document.getElementById('selectZb');

        this.selectZa.addEventListener('change', () => this.updatePlot());
        this.selectZb.addEventListener('change', () => this.updatePlot());

        this.updatePlot();
    },

    updatePlot: function () {
        const zA = parseInt(this.selectZa.value);
        const zB = parseInt(this.selectZb.value);
        const product = zA * zB;

        // Debye-Huckel Limiting Law: log(k/k0) = 2 * A * zA * zB * sqrt(I)
        // A approx 0.509
        const A = 0.509;

        const xValues = []; // sqrt(I)
        const yValues = []; // log(k/k0)

        // sqrt(I) from 0 to 0.5 (I from 0 to 0.25 M)
        for (let sqrtI = 0; sqrtI <= 0.5; sqrtI += 0.01) {
            xValues.push(sqrtI);
            yValues.push(2 * A * product * sqrtI);
        }

        const trace = {
            x: xValues,
            y: yValues,
            mode: 'lines',
            name: `zA=${zA}, zB=${zB}`,
            line: {
                color: product > 0 ? '#3b82f6' : (product < 0 ? '#ef4444' : '#94a3b8'),
                width: 4
            }
        };

        // Reference lines for other charge types
        const traceRef1 = {
            x: [0, 0.5], y: [0, 2 * A * 1 * 1 * 0.5],
            mode: 'lines', name: '(+1)(+1)',
            line: { color: '#3b82f6', dash: 'dot', width: 1 }
        };
        const traceRef2 = {
            x: [0, 0.5], y: [0, 2 * A * 1 * (-1) * 0.5],
            mode: 'lines', name: '(+1)(-1)',
            line: { color: '#ef4444', dash: 'dot', width: 1 }
        };

        const layout = {
            title: `Salt Effect (z_A z_B = ${product})`,
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#f1f5f9' },
            xaxis: {
                title: '√I (M½)',
                gridcolor: '#334155'
            },
            yaxis: {
                title: 'log(k/k₀)',
                gridcolor: '#334155'
            },
            margin: { t: 40, r: 20, b: 40, l: 60 },
            showlegend: true,
            legend: { x: 0.05, y: 1 }
        };

        Plotly.newPlot('saltEffectPlot', [traceRef1, traceRef2, trace], layout, { displayModeBar: false });
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    EyringPlot.init();
    EntropyVisualizer.init();
    SaltEffect.init();
});
