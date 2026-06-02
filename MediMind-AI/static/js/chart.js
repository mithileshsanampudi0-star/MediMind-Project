document.addEventListener("DOMContentLoaded", () => {

    renderRiskChart();
    renderOverviewChart();

    console.log("Analytics Loaded");

    const scoreElement = document.getElementById("healthScore");

    if (scoreElement) {

        let score = parseInt(scoreElement.innerText);

        if (score >= 80) {
            scoreElement.style.color = "#00ff88";
        }
        else if (score >= 50) {
            scoreElement.style.color = "#ffcc00";
        }
        else {
            scoreElement.style.color = "#ff4d6d";
        }
    }

});

function renderRiskChart() {

    const low = parseInt(
        document.getElementById("lowRisk").value
    );

    const medium = parseInt(
        document.getElementById("mediumRisk").value
    );

    const high = parseInt(
        document.getElementById("highRisk").value
    );

    const ctx = document.getElementById("riskChart");

    if (!ctx) return;

    new Chart(ctx, {

        type: "doughnut",

        data: {
            labels: ["Low", "Medium", "High"],
            datasets: [{
                data: [low, medium, high],
                backgroundColor: [
                    "#22c55e",
                    "#f59e0b",
                    "#ef4444"
                ],
                borderWidth: 0
            }]
        },

        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: "#ffffff"
                    }
                }
            }
        }

    });
}

function renderOverviewChart() {

    const total = parseInt(
        document.getElementById("totalRecords").value
    );

    const emergency = parseInt(
        document.getElementById("emergencyCases").value
    );

    const normal = total - emergency;

    const ctx = document.getElementById("analysisChart");

    if (!ctx) return;

    new Chart(ctx, {

        type: "bar",

        data: {
            labels: ["Normal", "Emergency"],
            datasets: [{
                label: "Cases",
                data: [normal, emergency],
                backgroundColor: [
                    "#06b6d4",
                    "#ef4444"
                ],
                borderRadius: 8
            }]
        },

        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: "#ffffff"
                    }
                },
                x: {
                    ticks: {
                        color: "#ffffff"
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }

    });
}