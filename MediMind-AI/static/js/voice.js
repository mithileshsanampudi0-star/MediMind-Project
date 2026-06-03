// =====================================
// MediMind AI Voice Input
// =====================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "VOICE JS LOADED"
        );

        initializeVoiceInput();

    }
);

function initializeVoiceInput() {

    const voiceButton =
        document.getElementById(
            "voiceBtn"
        );

    const textarea =
        document.querySelector(
            "textarea[name='symptoms']"
        );

    if (!voiceButton || !textarea) {

        console.log(
            "Voice button or textarea not found"
        );

        return;
    }

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        voiceButton.innerText =
            "Voice Not Supported";

        voiceButton.disabled = true;

        console.log(
            "Speech Recognition not supported"
        );

        return;
    }

    const recognition =
        new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.maxAlternatives = 1;

    // =====================================
    // Start Recording
    // =====================================

    voiceButton.addEventListener(
        "click",
        () => {

            console.log(
                "VOICE BUTTON CLICKED"
            );

            try {

                recognition.start();

                voiceButton.innerText =
                    "🎤 Listening...";

                voiceButton.classList.add(
                    "recording"
                );

            }

            catch(error) {

                console.log(
                    "Start Error:",
                    error
                );

            }

        }
    );

    // =====================================
    // Result
    // =====================================

    recognition.addEventListener(
        "result",
        event => {

            const transcript =
                event.results[0][0]
                .transcript;

            console.log(
                "Transcript:",
                transcript
            );

            textarea.value +=
                transcript + " ";

        }
    );

    // =====================================
    // End Recording
    // =====================================

    recognition.addEventListener(
        "end",
        () => {

            voiceButton.innerText =
                "Start Voice Input";

            voiceButton.classList.remove(
                "recording"
            );

        }
    );

    // =====================================
    // Error Handling
    // =====================================

    recognition.addEventListener(
        "error",
        event => {

            console.log(
                "VOICE ERROR:",
                event.error
            );

            alert(
                "Voice Error: " +
                event.error
            );

            voiceButton.innerText =
                "Voice Error";

            setTimeout(
                () => {

                    voiceButton.innerText =
                        "Start Voice Input";

                },
                2000
            );

        }
    );

}
