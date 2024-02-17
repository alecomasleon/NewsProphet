function scrollToResult() {
    setTimeout(function() {
        console.log("here")
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }, 100); // Adjust the delay time as needed (in milliseconds)
}

function showLinkForm() {
    document.getElementById('linkForm').style.display = 'block';
    document.getElementById('textForm').style.display = 'none';
}

function showTextForm() {
    document.getElementById('linkForm').style.display = 'none';
    document.getElementById('textForm').style.display = 'block';
}

function calculateViewsFromLink() {
    const link = document.getElementById('link').value;
    // Navigate to the new page with the link information
    sendRequest('scrape', {'url': link});
    // window.location.href = 'result.html?link=' + encodeURIComponent(link);
    scrollToResult();
}

function calculateViewsFromText() {
    const heading = document.getElementById('heading').value;
    const body = document.getElementById('body').value;
    const images = parseInt(document.getElementById('images').value) || 0;
    const videos = parseInt(document.getElementById('videos').value) || 0;

    // call sendRequest
    
    // Dummy calculation for demonstration
    const views = Math.floor(Math.random() * 10000) + 1;

    // Display the result
    document.getElementById('result').style.display = 'block';
    document.getElementById('views').innerText = views;
    scrollToResult();
}

document.addEventListener('DOMContentLoaded', function() {
    // Get the link information from the URL
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const link = urlParams.get('link');

    // Populate the form fields with the extracted link information
    document.getElementById('link').value = link;
});

const serverURLStr = "http://localhost:9000/";
async function sendRequest(request, params) {
    console.log("HEREHERE")
    const serverUrl = new URL(serverURLStr + request)
    serverUrl.search = new URLSearchParams(params)
    serverUrl.headers = {'Access-Control-Allow-Origin': 'http://localhost:9000'}
    let response = await fetch( serverUrl, {mode:'cors'} )
    var msg = await response.json()
    console.log("msg")
    console.log(msg)

    // Do what you want to do with the message
}
