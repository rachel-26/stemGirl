// savedEvent.js
document.addEventListener("DOMContentLoaded", () => {
    // Select the "Saved Events" icon/button in your sidebar
    const savedEventsIcon = document.getElementById("saved-events-icon");

    if (savedEventsIcon) {
        savedEventsIcon.addEventListener("click", () => {
            // Navigate to the opportunities page when clicked
            window.location.href = "opportunities.html";
        });
    } else {
        console.error("Saved Events icon not found in sidebar!");
    }
});
