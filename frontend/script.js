// Function to show the link form and hide the text form
function showLinkForm() {
    document.getElementById('linkForm').style.display = 'block';
    document.getElementById('textForm').style.display = 'none';
}

// Function to show the text form and hide the link form
function showTextForm() {
    console.log("test");
    document.getElementById('linkForm').style.display = 'none';
    document.getElementById('textForm').style.display = 'block';
}

// Function to handle the calculation when the user inputs a link
async function calculateViewsFromLink() {
    const link = document.getElementById('link').value;

    // Send request to scrape data from the provided link
    const response = await sendRequest('scrape', {'url': link});

    // Extract the necessary information from the response
    const { header, body, num_images, num_hyperlinks, num_videos, published_date } = response;

    // Fill out the form fields with the extracted information
    document.getElementById('heading').value = header;
    document.getElementById('body').value = body;
    document.getElementById('numImages').value = num_images;
    document.getElementById('numHyperlinks').value = num_hyperlinks;
    document.getElementById('numVideos').value = num_videos;
    document.getElementById('publishedDate').value = published_date;

    showTextForm();
}

// Function to handle the calculation when the user inputs text directly
async function calculateViewsFromText() {
    const heading = document.getElementById('heading').value;
    const body = document.getElementById('body').value;
    const numImages = parseInt(document.getElementById('numImages').value) || 0;
    const numHyperlinks = parseInt(document.getElementById('numHyperlinks').value) || 0;
    const numVideos = parseInt(document.getElementById('numVideos').value) || 0;
    const publishedDate = document.getElementById('publishedDate').value || '2024-02-18';

    // Send request to the server to calculate views from the provided text
    const response = await sendRequest('calculate', { 'header': heading, 'body': body, 'num_images': numImages, 'num_hyperlinks': numHyperlinks, 'num_videos': numVideos, 'published_date': publishedDate });

    // Handle the response from the server
    handleCalculationResponse(response);
}

// Function to handle giving feedback when the user inputs a link
async function giveFeedback() {
    const link = document.getElementById('link').value;

    // Send request to scrape data from the provided link
    const response = await sendRequest('scrape', {'url': link});

    // Extract the necessary information from the response
    const { heading, body, images, hyperlinks, num_videos, published_date } = response;

    // Fill out the form fields with the extracted information
    document.getElementById('heading').value = heading;
    document.getElementById('body').value = body;
    document.getElementById('numImages').value = images;
    document.getElementById('numHyperlinks').value = hyperlinks;
    document.getElementById('numVideos').value = num_videos;
    document.getElementById('publishedDate').value = published_date;

    // Hide the link form and show the text form
    showTextForm();
}

// Function to handle the response from the backend
function handleCalculationResponse(msg) {
    // Handle the response from the backend
    console.log("Calculation result:");
    console.log(msg.score_msg);
    console.log(msg.msg);
    console.log(msg.details);

    // Display the suggestions
    displaySuggestions(msg.score_msg, msg.msg, msg.details);
}

// Function to display the suggestions
function displaySuggestions(score_msg, msg, details) {
    // Assuming there's a <div> element with the id 'suggestions' in your HTML where you want to display the suggestions
    const sme = document.getElementById('score_msg');
    const me = document.getElementById('msg');
    const de = document.getElementById('details');

    // Clear previous suggestions
    sme.innerHTML = '';
    me.innerHTML = '';
    de.innerHTML = '';

    // Display the suggestion
    const suggestionItem = document.createElement('p');
    suggestionItem.textContent = score_msg;
    sme.appendChild(suggestionItem);

    const item2 = document.createElement('p');
    item2.textContent = msg;
    me.appendChild(item2);

    const item3 = document.createElement('p');
    item3.textContent = 'Details: ' + details;
    de.appendChild(item3);
}

// Populate the form fields with the extracted link information when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Get the link information from the URL
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const link = urlParams.get('link');

    // Populate the form fields with the extracted link information
    document.getElementById('link').value = link;
});

// Define the server URL
const serverURLStr = "http://localhost:9000/";

async function sendRequest(request, params) {
    const serverUrl = new URL(serverURLStr + request)
    serverUrl.search = new URLSearchParams(params)
    serverUrl.headers = {'Access-Control-Allow-Origin': 'http://localhost:9000'}

    let response = await fetch(serverUrl, {mode: 'cors'})
    let msg = await response.json()

    console.log(msg);

    // Return the message received from the server
    return msg;
}