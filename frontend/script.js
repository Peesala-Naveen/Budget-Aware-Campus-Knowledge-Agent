

let processing = false;
let currentController = null; // Used to abort requests

const chat = document.getElementById("chat");
const history = document.getElementById("history");
const input = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");
const toggle = document.getElementById("toggle");
const suggestions = document.getElementById("suggestions");

/* THEME TOGGLE */
toggle.onclick = () => {
    document.body.classList.toggle("light");
    document.body.classList.toggle("dark");
    toggle.innerText = document.body.classList.contains("light") ? "🌙" : "☀️";
};

/* SUGGESTION BUTTONS */
if (suggestions) {
    suggestions.addEventListener("click", (e) => {
        if (e.target.tagName === "BUTTON" && !processing) {
            input.value = e.target.innerText;
            send();
        }
    });
}

/* SEND OR STOP BUTTON LOGIC */
sendBtn.onclick = () => {
    if (processing) {
        stopResponse();
    } else {
        send();
    }
};

/* ABORT FUNCTION */
function stopResponse() {
    if (currentController) {
        currentController.abort(); // Kills the fetch request
        processing = false;
        input.disabled = false;
        sendBtn.innerText = "➤";
        sendBtn.classList.remove("stop-active");

        // Remove loaders from screen
        const loaders = document.querySelectorAll(".loading-msg");
        loaders.forEach(l => l.remove());

        let stopMsg = document.createElement("div");
        stopMsg.className = "bot";
        stopMsg.style.color = "#ef4444";
        stopMsg.innerText = "🛑 Stopped.";
        chat.appendChild(stopMsg);
    }
}

/* SEND FUNCTION */
async function send() {
    let text = input.value.trim();
    if (!text || processing) return;

    const welcome = document.getElementById("welcome");
    if (welcome) welcome.style.display = "none";

    processing = true;
    input.disabled = true;
    input.value = "";

    // UI Change to STOP button
    sendBtn.innerText = "■";
    sendBtn.classList.add("stop-active");

    // Create User Message
    let userDiv = document.createElement("div");
    userDiv.className = "user";
    userDiv.innerText = text;
    chat.appendChild(userDiv);
    userDiv.scrollIntoView({ behavior: "smooth" });

    // Thinking Indicator
    let loader = document.createElement("div");
    loader.className = "bot loading-msg";
    loader.innerText = "⏳ Thinking...";
    chat.appendChild(loader);

    // Initialize AbortController
    currentController = new AbortController();

    try {
        let res = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: text }),
            signal: currentController.signal
        });

        let data = await res.json();
        loader.remove();

        let botDiv = document.createElement("div");
        botDiv.className = "bot";

        let content = data.answer;
        if (data.source_url) {
            content += `<br><br><a href="${data.source_url}" target="_blank" style="color:#818cf8; font-weight:600;">Official Source</a>`;
        }

        botDiv.innerHTML = content;
        chat.appendChild(botDiv);

        // Sidebar History
        let histItem = document.createElement("div");
        histItem.innerText = text.length > 25 ? text.substring(0, 25) + "..." : text;
        histItem.onclick = () => userDiv.scrollIntoView({ behavior: "smooth" });
        history.appendChild(histItem);

        botDiv.scrollIntoView({ behavior: "smooth" });

    } catch (err) {
        if (err.name === 'AbortError') {
            console.log("User stopped request.");
        } else {
            loader.innerText = "❌ Connection Error.";
        }
    } finally {
        processing = false;
        input.disabled = false;
        sendBtn.innerText = "➤";
        sendBtn.classList.remove("stop-active");
        input.focus();
    }
}

/* KEYBOARD SUPPORT */
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !processing) send();
});