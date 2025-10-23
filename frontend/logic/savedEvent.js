document.addEventListener("DOMContentLoaded", () => {
    const eventsContainer = document.querySelector("main .space-y-6");

    fetch("http://127.0.0.1:8000/getEvents")
        .then(res => res.json())
        .then(data => {
            // Ensure events is an array
            let events = [];
            if (Array.isArray(data)) {
                events = data;
            } else if (data && Array.isArray(data.events)) {
                events = data.events;
            } else {
                console.warn("Unexpected API response, defaulting to empty array:", data);
            }

            // Clear existing hardcoded events
            eventsContainer.innerHTML = "";

            events.forEach(event => {
                const card = document.createElement("div");
                card.className = "bg-white dark:bg-background-dark/50 rounded-lg shadow-sm p-6 flex gap-6 items-start";

                const thumbnailUrl = event.thumbnail || "https://via.placeholder.com/150";

                card.innerHTML = `
                    <div class="w-48 h-32 bg-cover bg-center rounded-lg" style="background-image: url('${thumbnailUrl}');"></div>
                    <div class="flex-1">
                        <span class="inline-block bg-primary/10 text-primary text-xs font-semibold px-2 py-1 rounded-full mb-2">${event.type || "Workshop"}</span>
                        <h3 class="text-lg font-bold text-gray-900 dark:text-white">${event.name || "Untitled Event"}</h3>
                        <p class="text-gray-600 dark:text-gray-400 mt-1 text-sm">${event.description || "No description available."}</p>
                        <p class="text-gray-500 text-xs mt-1">${event.date || "TBA"} | ${event.location || "Online"}</p>
                        ${event.link ? `<a href="${event.link}" target="_blank" class="text-sm font-semibold text-primary hover:underline mt-2 inline-block">Learn more</a>` : ""}
                    </div>
                `;

                eventsContainer.appendChild(card);
            });
        })
        .catch(err => {
            console.error("Failed to load events:", err);
            eventsContainer.innerHTML = `<p class="text-gray-500 dark:text-gray-400">No events available at the moment.</p>`;
        });

    // Saved Events icon navigation
    const savedEventsIcon = document.getElementById("saved-event-icon") || document.getElementById("saved-events-icon");
    if (savedEventsIcon) {
        savedEventsIcon.addEventListener("click", () => {
            window.location.href = "opportunities.html","_blank";
        });
    }
});
