
export async function generateEvents(interest) {
    console.log(`Auto event generation started for: ${interest}`);

    try {
        const res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: `Find and summarize the latest ${interest} related competitions, bootcamps, hackathons, and events for girls in STEM.`
            }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const data = await res.json();
        console.log(` Auto events generated for ${interest}:`, data.events?.length || 0);

    } catch (error) {
        console.error(" Error during auto event generation:", error);
    }
}
