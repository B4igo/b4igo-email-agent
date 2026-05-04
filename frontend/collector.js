chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "B4IGO_KEYS_FOUND") {
        chrome.storage.local.set({ allPrivateKeys: message.keys }, () => {
            console.log("Keys found and stored");
        });
    }
});