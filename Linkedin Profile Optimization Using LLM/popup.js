import { GoogleGenerativeAI } from "@google/generative-ai";
import { jsPDF } from 'jspdf';
import { marked } from 'marked';

// Load profile data from storage and display in the popup
function loadProfileData() {
    chrome.storage.local.get("profileData", (data) => {
        const profileData = data.profileData || {};
        // If profile data exists, display it
        if (profileData && profileData.name && profileData.headline && profileData.summary) {
            document.getElementById("name").innerText = profileData.name || "Name not found";
            document.getElementById("headline").innerText = profileData.headline || "Headline not found";
            document.getElementById("summary").innerText = profileData.summary || "Summary not found";
        } else {
            // If no profile data, clear display or set to default message
            document.getElementById("name").innerText = "No profile data found.";
            document.getElementById("headline").innerText = "No profile data found.";
            document.getElementById("summary").innerText = "No profile data found.";
        }
    });
}

// Initial load of profile data
loadProfileData();

// Handle the refresh button click
document.getElementById("refreshButton").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: "refreshProfileData" }, (response) => {
            const statusMessage = document.getElementById("statusMessage");
            if (response && response.status === "Profile data refreshed") {
                statusMessage.innerText = "Profile data refreshed successfully!";
                statusMessage.className = 'success';
                loadProfileData(); // Reload profile data after refresh
            } else {
                statusMessage.innerText = "Error refreshing data. Make sure you are on the LinkedIn profile page.";
                statusMessage.className = 'error'; // Apply error class
                document.getElementById("name").innerText = "No profile data found.";
                document.getElementById("headline").innerText = "No profile data found.";
                document.getElementById("summary").innerText = "No profile data found.";
            }
        });
    });
});


// Button to download the PDF
document.getElementById("downloadPdfButton").addEventListener("click", () => { 
    const optimizedContent = document.getElementById("optimizedContent").innerText.trim();
    const profileName = document.getElementById("name").innerText || "Optimized_Profile";

    // Check if optimized content is empty
    if (!optimizedContent || optimizedContent === "Your optimized content will appear here...") {
        alert("No optimized content available to download.");
        return;
    }

    // Convert markdown to HTML
    const htmlContent = marked(optimizedContent);

    // Create a temporary container to hold the HTML content
    const tempContainer = document.createElement("div");
    tempContainer.innerHTML = htmlContent;

    // Create a new jsPDF instance
    const doc = new jsPDF();

    // Use jsPDF's html method to directly render the HTML into the PDF
    doc.html(tempContainer, {
        callback: function (doc) {
            // Save the PDF with the profile name (sanitized to avoid file system issues)
            doc.save(`${profileName.replace(/\s+/g, '_')}_Profile.pdf`);
        },
        x: 10, // Left margin
        y: 10, // Top margin
        width: 180, // Width of the content
        windowWidth: 800 // Adjust this for large content
    });
});

// Optimize LinkedIn profile button event listener
document.getElementById("optimize").addEventListener("click", optimizeProfile);

async function optimizeProfile() {
    const name = document.getElementById("name").innerText;
    const headline = document.getElementById("headline").innerText;
    const summary = document.getElementById("summary").innerText;

    const inputText = `"Optimize my profile with the following details: Name: ${name}, Headline: ${headline}, Summary: ${summary}. Please help me improve my profile."`;

    try {
        const optimizedContent = await callGoogleGenerativeAI(inputText);

        // Convert markdown to HTML
        const markdownHtml = marked(optimizedContent);

        // Display the HTML in the popup
        document.getElementById("optimizedContent").innerHTML = markdownHtml;

        // Save the profile data to storage after optimization
        const profileData = {
            name,
            headline,
            summary,
            optimizedContent
        };
        chrome.storage.local.set({ profileData });
    } catch (error) {
        console.error("Error optimizing profile:", error);
        document.getElementById("optimizedContent").innerText = "Failed to optimize profile. Please try again.";
        
        // Clear any invalid profile data from storage if optimization fails
        chrome.storage.local.remove("profileData");
        // Reset the UI elements if optimization fails
        document.getElementById("name").innerText = "No profile data found.";
        document.getElementById("headline").innerText = "No profile data found.";
        document.getElementById("summary").innerText = "No profile data found.";
    }
}

// Function to call Google Generative AI API
async function callGoogleGenerativeAI(inputText) {
    const apiKey = ""; // Ensure this is your actual API key
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    try {
        const result = await model.generateContent([inputText]);
        return result.response.text(); // Adjust based on the actual response structure
    } catch (error) {
        console.error("Error calling Google Generative AI:", error);
        throw new Error('Failed to generate optimized content');
    }
}
