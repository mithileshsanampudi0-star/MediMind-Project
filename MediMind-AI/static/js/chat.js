document.addEventListener(
    "DOMContentLoaded",
    () => {

        const sendButton =
            document.getElementById(
                "sendButton"
            );

        const input =
            document.getElementById(
                "messageInput"
            );

        if (sendButton) {

            sendButton.addEventListener(
                "click",
                sendMessage
            );

        }

        if (input) {

            input.addEventListener(
                "keydown",
                function(event) {

                    if (
                        event.key === "Enter" &&
                        !event.shiftKey
                    ) {

                        event.preventDefault();

                        sendMessage();

                    }

                }
            );

        }

    }
);

async function sendMessage() {

    const input =
        document.getElementById(
            "messageInput"
        );

    const message =
        input.value.trim();

    if (!message) {
        return;
    }

    addMessage(
        "You",
        message,
        true
    );

    input.value = "";

    const loadingElement =
        addTypingIndicator();

    try {

        const response =
            await fetch(
                "/chat/send",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            message:
                                message
                        }
                    )
                }
            );

        const data =
            await response.json();

        loadingElement.remove();

        if (data.success) {

            addMessage(
                "MediMind AI",
                data.response,
                false
            );

        } else {

            addMessage(
                "System",
                "Unable to process request.",
                false
            );

        }

    } catch {

        loadingElement.remove();

        addMessage(
            "System",
            "Server connection error.",
            false
        );

    }

}

function addMessage(
    sender,
    text,
    isUser
) {

    const container =
        document.getElementById(
            "chatMessages"
        );

    const message =
        document.createElement(
            "div"
        );

    message.className =
        isUser
        ? "chat-message user-message"
        : "chat-message ai-message";

    message.innerHTML = `

        <div class="message-role">
            ${sender}
        </div>

        <div class="message-content">
            ${text}
        </div>

    `;

    container.appendChild(
        message
    );

    container.scrollTop =
        container.scrollHeight;
}

function addTypingIndicator() {

    const container =
        document.getElementById(
            "chatMessages"
        );

    const typing =
        document.createElement(
            "div"
        );

    typing.className =
        "chat-message ai-message";

    typing.innerHTML = `

        <div class="message-role">
            MediMind AI
        </div>

        <div class="typing-indicator">
            Thinking...
        </div>

    `;

    container.appendChild(
        typing
    );

    container.scrollTop =
        container.scrollHeight;

    return typing;
}