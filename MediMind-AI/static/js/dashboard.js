// =====================================
// MediMind AI Dashboard Scripts
// =====================================

document.addEventListener("DOMContentLoaded", () => {

    initializeCounters();
    initializeCards();
    initializeButtons();
    initializeSidebarToggle();

});

// =====================================
// Sidebar Toggle
function initializeSidebarToggle() {
    const toggleButton = document.getElementById("sidebarToggle");
    const appLayout = document.querySelector(".app-layout");
    const sidebar = document.querySelector(".sidebar");

    if (!toggleButton || !appLayout || !sidebar) {
        return;
    }

    toggleButton.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
        appLayout.classList.toggle("sidebar-collapsed");
    });
}

// =====================================
// Animated Counters
// =====================================

function initializeCounters() {

    const counters = document.querySelectorAll(
        ".stat-card h2"
    );

    counters.forEach(counter => {

        const target = parseInt(
            counter.innerText
        );

        if (isNaN(target)) {
            return;
        }

        let current = 0;

        const increment = Math.max(
            1,
            Math.ceil(target / 50)
        );

        const interval = setInterval(() => {

            current += increment;

            if (current >= target) {

                counter.innerText = target;
                clearInterval(interval);

            } else {

                counter.innerText = current;

            }

        }, 25);

    });

}

// =====================================
// Reveal Animation
// =====================================

function initializeCards() {

    const cards = document.querySelectorAll(
        ".card, .stat-card, .hospital-card"
    );

    const observer = new IntersectionObserver(

        entries => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    entry.target.classList.add(
                        "fade-in"
                    );

                }

            });

        },

        {
            threshold: 0.15
        }

    );

    cards.forEach(card => {

        observer.observe(card);

    });

}

// =====================================
// Button Effects
// =====================================

function initializeButtons() {

    const buttons = document.querySelectorAll(
        ".btn, .auth-btn, .action-btn"
    );

    buttons.forEach(button => {

        button.addEventListener(
            "mouseenter",
            () => {

                button.style.transform =
                    "translateY(-3px)";

            }
        );

        button.addEventListener(
            "mouseleave",
            () => {

                button.style.transform =
                    "translateY(0px)";

            }
        );

    });

}

// =====================================
// Loading State
// =====================================

function showLoading(button) {

    const originalText =
        button.innerHTML;

    button.innerHTML =
        "Processing...";

    button.disabled = true;

    return originalText;

}

// =====================================
// Form Loading UX
// =====================================

document.addEventListener(
    "submit",
    function(event) {

        const submitButton =
            event.target.querySelector(
                "button[type='submit']"
            );

        if (submitButton) {

            showLoading(
                submitButton
            );

        }

    }
);