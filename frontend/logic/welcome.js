console.log("welcome.js loaded!")
const buttons = document.querySelectorAll('.interest-button');
let selectedInterest = null;

// Only allow one interest to be selected
buttons.forEach(btn => {
    btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedInterest = btn.dataset.interest;
    });
});

// Handle continue button
document.getElementById('continue-btn').addEventListener('click', async () => {
    if (!selectedInterest) {
        alert("Please select an interest to continue!");
        return;
    }

    try {
        //Send the selected interest to backend
        const response = await fetch("http://127.0.0.1:8000/set-interest", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ interest: selectedInterest }),
        });

        const data = await response.json();
        if (data.success) {
            console.log("Interest stored in backend:", data.interest);

            // Save locally as well
            localStorage.setItem("userInterest", selectedInterest);

            //Fire the background event generator (no await)
        import("./autoEventGenerator.js")
            .then(module => module.generateEvents(selectedInterest))
            .catch(err => console.error("Could not start event generator:", err));

            // Redirect to chat interface
            window.location.href = "chatInterface.html";
        } else {
            alert("Failed to store interest on server.");
        }
    } catch (err) {
        console.error("Error sending interest to API:", err);
        alert("Something went wrong. Please try again.");
    }
});