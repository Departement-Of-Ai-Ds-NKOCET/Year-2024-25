// Function to extract LinkedIn profile data
function extractProfileData() {
    const profileData = {
        name: document.querySelector('h1.t-24.v-align-middle.break-words')?.innerText.trim() || "Name not found",
        headline: document.querySelector('.text-body-medium.break-words')?.innerText.trim() || "Headline not found",
        summary: document.querySelector('div.display-flex.full-width div.inline-show-more-text--is-collapsed span[aria-hidden="true"]')?.innerText.trim() || "Summary not found"

    };

    // Save the profile data to Chrome storage
    chrome.storage.local.set({ profileData: profileData }, () => {
        console.log("Profile data refreshed and saved:", profileData);
    });
}
// Listen for refresh request from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "refreshProfileData") {
        extractProfileData();
        sendResponse({ status: "Profile data refreshed" });
    }
    

    
});
