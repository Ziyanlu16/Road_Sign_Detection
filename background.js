chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.message == "open_window") {
        window.open('https://www.example.com', '_blank', 'width=500,height=500');
    }
});
