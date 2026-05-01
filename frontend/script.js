let processing = false;

const chat = document.getElementById("chat");
const history = document.getElementById("history");
const input = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");
const toggle = document.getElementById("toggle");

/* THEME TOGGLE */
toggle.onclick = () => {
    document.body.classList.toggle("light");
    document.body.classList.toggle("dark");

    if (document.body.classList.contains("light")) {
        toggle.innerText = "🌙"; // switch to dark
    } else {
        toggle.innerText = "☀️"; // switch to light
    }
};

/* SEND FUNCTION */
async function send() {

    if (processing) return;

    let text = input.value.trim();
    if (!text) return;

    processing = true;
    input.disabled = true;

    input.value = "";

    // USER MESSAGE
    let userDiv = document.createElement("div");
    userDiv.className = "user";
    userDiv.innerText = text;
    chat.appendChild(userDiv);

    // SCROLL
    userDiv.scrollIntoView();

    // LOADER
    let loader = document.createElement("div");
    loader.className = "bot";
    loader.innerText = "⏳ Thinking... 0%";
    chat.appendChild(loader);

    let percent = 0;
    let interval = setInterval(() => {
        percent += 10;
        loader.innerText = `⏳ Thinking... ${percent}%`;
        if (percent >= 90) clearInterval(interval);
    }, 100);

    // API CALL
    try {
        let res = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: text })
        });

        let data = await res.json();

        clearInterval(interval);
        loader.remove();

        // BOT MESSAGE
        let botDiv = document.createElement("div");
        botDiv.className = "bot";
        botDiv.innerText = data.answer;
        chat.appendChild(botDiv);

        // HISTORY
        let item = document.createElement("div");
        item.innerText = text;
        item.onclick = () => userDiv.scrollIntoView({ behavior: "smooth" });
        history.appendChild(item);

    } catch (err) {
        loader.innerText = "❌ Error fetching response";
    }

    processing = false;
    input.disabled = false;
}

/* ENTER KEY SUPPORT */
input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") send();
});

/* BUTTON CLICK */
sendBtn.onclick = send;