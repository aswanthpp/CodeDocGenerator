function loadUrl() {
  var url = document.getElementById("urlInput").value.trim();
  var language = document.getElementById("languageSelect").value;

  document.getElementById('query').value = '';
  document.getElementById('response').innerHTML = ''; 
  document.getElementById("loadedUrlText").innerText = '';
  document.getElementById("loadedUrl").style.display = "none";

  var loadButton = document.getElementById("loadButton");
  var loadingSpinner = document.getElementById("loadingSpinner");

  // Disable the button to prevent multiple clicks during the fetch
  loadButton.disabled = true;
  loadButton.style.display = "none";

  // Display the loading spinner
  loadingSpinner.style.display = "inline-block";

  var gitUrlRegex =
    /^(https?:\/\/)?(www\.)?github\.com\/[a-zA-Z0-9\-._~:/?#[\]@!$&'()*+,;=]+$/;

  if (gitUrlRegex.test(url)) {
    fetch("http://localhost:5050/load", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ path: url, language: language }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.status == "Success") {
          showResponseBubble(data.message, true);

          document.getElementById("loadedUrlText").innerText = url;
          document.getElementById("loadedUrl").style.display = "block";
        } else {
          showResponseBubble(data.message, false);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        showResponseBubble("Error occurred during fetch", false);
      })
      .finally(() => {
        // Enable the button after fetch operation (whether successful or not)
        loadButton.disabled = false;
        // Hide the loading spinner
        loadingSpinner.style.display = "none";
        loadButton.style.display = "inline-block";
      });
  } else {
    showResponseBubble("Please Enter Valid Github URL", false);

    // Enable the button after fetch operation (whether successful or not)
    loadButton.disabled = false;
    // Hide the loading spinner
    loadingSpinner.style.display = "none";
    loadButton.style.display = "inline-block";
  }
}

function isDocumentLoaded() {
  var documentLoaded = document.getElementById("loadedUrl").style.display;
  if (documentLoaded == "block") {
    return true;
  } else return false;
}
function getResponse() {
  var query = document.getElementById("query").value;
  var queryButton = document.getElementById("queryButton");
  var querySpinner = document.getElementById("querySpinner");
  var response = document.getElementById("response");
  response.innerText = "";

  // Disable the button to prevent multiple clicks during the fetch
  queryButton.disabled = true;
  queryButton.style.display = "none";

  // Display the loading spinner
  querySpinner.style.display = "inline-block";

  if (isDocumentLoaded()) {
    // Make a POST request to the server
    fetch("http://localhost:5050/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: query }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        response.innerText = data.message;
      })
      .catch((error) => {
        console.error("Error:", error);
      })
      .finally(() => {
        // Enable the button after fetch operation (whether successful or not)
        queryButton.disabled = false;
        // Hide the loading spinner
        querySpinner.style.display = "none";
        queryButton.style.display = "inline-block";
      });
  } else {
    showResponseBubble(
      "Please Load the Document, then use Chat interface",
      false
    );

    // Enable the button after fetch operation (whether successful or not)
    queryButton.disabled = false;
    // Hide the loading spinner
    querySpinner.style.display = "none";
    queryButton.style.display = "inline-block";
  }
}

function showResponseBubble(message, status) {
  var responseBubble = document.getElementById("responseBubble");

  responseBubble.style.backgroundColor = status ? "green" : "red";

  responseBubble.innerText = message;
  responseBubble.style.display = "block";

  // Hide the bubble after 3 seconds (adjust the timeout as needed)
  setTimeout(function () {
    responseBubble.style.display = "none";
  }, 3000);
}
