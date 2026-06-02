document.addEventListener(
    "DOMContentLoaded",
    () => {

        startPipeline();

    }
);

function startPipeline() {

    const steps = [

        {
            text:
            "Extracting Symptoms...",
            element:
            "step1"
        },

        {
            text:
            "Predicting Diseases...",
            element:
            "step2"
        },

        {
            text:
            "Assessing Risk...",
            element:
            "step3"
        },

        {
            text:
            "Detecting Emergencies...",
            element:
            "step4"
        },

        {
            text:
            "Finding Specialist...",
            element:
            "step5"
        },

        {
            text:
            "Generating Report...",
            element:
            "step6"
        }

    ];

    let current = 0;

    const progressBar =
        document.getElementById(
            "progressBar"
        );

    const progressPercent =
        document.getElementById(
            "progressPercent"
        );

    const currentStep =
        document.getElementById(
            "currentStep"
        );

    const interval =
        setInterval(() => {

            if (
                current >=
                steps.length
            ) {

                clearInterval(
                    interval
                );

                currentStep.innerText =
                    "Analysis Complete";

                return;
            }

            const percentage =
                Math.round(

                    (
                        (current + 1)
                        /
                        steps.length
                    )
                    * 100

                );

            progressBar.style.width =
                percentage + "%";

            progressPercent.innerText =
                percentage + "%";

            currentStep.innerText =
                steps[current].text;

            document
                .getElementById(
                    steps[current]
                    .element
                )
                .classList.add(
                    "active-step"
                );

            current++;

        }, 1200);

}