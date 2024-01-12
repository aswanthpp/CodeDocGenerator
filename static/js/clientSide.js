function loadUrl() {
    var url = document.getElementById('urlInput').value;
    var language = document.getElementById('languageSelect').value;

    // Make a POST request to the server
    fetch('http://localhost:5050/load', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({path: url, language: language}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        // Show success message in a disappearing bubble
        showResponseBubble(data.response);

        // Handle the response if needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getResponse() {
    var query = document.getElementById('query').value;

    // Make a POST request to the server
    fetch('http://localhost:5050/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({query: query}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        var response = document.getElementById('response');
        response.innerText = data.response;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function showResponseBubble(message) {
    var responseBubble = document.getElementById('responseBubble');
    responseBubble.innerText = message;
    responseBubble.style.display = 'block';

    // Hide the bubble after 3 seconds (adjust the timeout as needed)
    setTimeout(function () {
        responseBubble.style.display = 'none';
    }, 3000);
}