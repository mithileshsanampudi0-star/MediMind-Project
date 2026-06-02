// =====================================
// MediMind AI Voice Input
// =====================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

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
        return;
    }

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        voiceButton.innerText =
            "Voice Not Supported";

        voiceButton.disabled = true;

        return;
    }

    const recognition =
        new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;

    // =====================================
    // Start Recording
    // =====================================

    voiceButton.addEventListener(
        "click",
        () => {

            recognition.start();

            voiceButton.innerText =
                "Listening...";

            voiceButton.classList.add(
                "recording"
            );

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

            textarea.value +=
                transcript + " ";

        }
    );

    // =====================================
    // End
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
    // Error
    // =====================================

    recognition.addEventListener(
        "error",
        () => {

            voiceButton.innerText =
                "Voice Error";

            setTimeout(() => {

                voiceButton.innerText =
                    "Start Voice Input";

            }, 2000);

        }
    );

}