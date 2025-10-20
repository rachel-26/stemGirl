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
document.getElementById('continue-btn').addEventListener('click', () => {
    if (!selectedInterest) {
        alert("Please select an interest to continue!");
        return;
    }
    // Store the interest for chat page (can also use sessionStorage)
    localStorage.setItem("userInterest", selectedInterest);

    // Redirect to chat interface
    window.location.href = "chatInterface.html"; 
});