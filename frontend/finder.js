console.log("B4iGo Agentic Email Parser: Login script injected.");

function checkTokenAndSend() {
    const keys = localStorage.getItem("allPrivateKeys");

    if (keys) {
        console.log("B4iGo Agentic Email Parser: Found");

        chrome.runtime.sendMessage({
            type: "B4IGO_KEYS_FOUND",
            token: keys
        });

        return true;
    }
    return false;
}

let found = checkTokenAndSend();

if (!found) {
    let attempts = 0;

    const tokenInterval = setInterval(() => {
        attempts++;
        if (checkTokenAndSend()) {
            clearInterval(tokenInterval);
        }
    }, 1000 + attempts * 100);
}