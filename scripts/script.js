import { API_KEY } from './config.js';  // Import the API Key from config.js

const SHEET_ID = "1OntEp66GXDfsbt2fqLWZ9qqZ6QJPzQctMkPqg-zlQTE";  // Your Google Sheets ID
const RANGE = "Sheet1!A2:D";  // Adjust range according to your Google Sheets structure

async function fetchApplicants() {
    const url = `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${RANGE}?key=${API_KEY}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        const rows = data.values;

        if (!rows) {
            console.error("No data found in Google Sheets.");
            return;
        }

        const tableBody = document.getElementById("applicant-data");
        tableBody.innerHTML = "";  // Clear previous data

        rows.forEach(row => {
            const [name, email, phone, resume] = row;
            const newRow = document.createElement("tr");

            newRow.innerHTML = `
                <td>${name || "N/A"}</td>
                <td>${email || "N/A"}</td>
                <td>${phone || "N/A"}</td>
                <td><a href="${resume}" target="_blank">View Resume</a></td>
            `;

            tableBody.appendChild(newRow);
        });
    } catch (error) {
        console.error("Error fetching data from Google Sheets:", error);
    }
}

// Load data on page load
document.addEventListener("DOMContentLoaded", fetchApplicants);
