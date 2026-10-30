
const API_URL = "http://localhost:8080/api/complaints";

const form = document.getElementById("complaint-form");
const complaintsContainer = document.getElementById("complaints-container");
const emptyMessage = document.getElementById("empty-message");

// Load complaints from Spring Boot when the page opens.
loadComplaints();

async function loadComplaints() {
    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }

        const complaints = await response.json();
        displayComplaints(complaints);

    } catch (error) {
        console.error("Could not load complaints:", error);
        complaintsContainer.innerHTML =
            "<p>Could not load complaints. Please check that the backend is running.</p>";
    }
}

// Submit a new complaint to Spring Boot.
form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const category = document.getElementById("category").value;
    const priority = document.getElementById("priority").value;
    const description = document.getElementById("description").value.trim();

    if (!name || !email || !category || !priority || !description) {
        alert("Please fill in all fields.");
        return;
    }

    const complaint = {
        name,
        email,
        category,
        priority,
        description,
        status: "Pending"
    };

    const submitButton = form.querySelector('button[type="submit"]');

    try {
        if (submitButton) submitButton.disabled = true;

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(complaint)
        });

        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }

        const savedComplaint = await response.json();

        form.reset();
        alert("Complaint submitted successfully!");

        // Reload the authoritative list from the backend.
        await loadComplaints();

        console.log("Saved complaint:", savedComplaint);

    } catch (error) {
        console.error("Complaint submission failed:", error);
        alert(
            "Could not submit the complaint. Please check the backend connection and try again."
        );
    } finally {
        if (submitButton) submitButton.disabled = false;
    }
});

function displayComplaints(complaints) {
    complaintsContainer.innerHTML = "";

    if (!complaints.length) {
        complaintsContainer.appendChild(emptyMessage);
        emptyMessage.style.display = "block";
        return;
    }

    emptyMessage.style.display = "none";

    complaints.forEach(function (complaint) {
        addComplaintToScreen(complaint);
    });
}

function addComplaintToScreen(complaint) {
    const card = document.createElement("div");
    card.className = "complaint-card";

    const dateText = complaint.createdAt || "Date unavailable";

    const predictionText = complaint.predictedCategory
        ? `AI predicted category: ${escapeHTML(complaint.predictedCategory)}`
        : "AI prediction unavailable";

    const confidenceText =
        typeof complaint.confidence === "number"
            ? ` (${(complaint.confidence * 100).toFixed(2)}% confidence)`
            : "";

    card.innerHTML = `
        <div class="complaint-top">
            <h3>
                ${escapeHTML(complaint.name || "")}
                <span class="category-tag">
                    ${escapeHTML(complaint.category || "")}
                </span>
            </h3>

            <span class="status ${getStatusClass(complaint.status)}">
                ${escapeHTML(complaint.status || "Pending")}
            </span>
        </div>

        <div class="meta">
            ${escapeHTML(complaint.email || "")}
            •
            ${escapeHTML(dateText)}
            •
            Complaint ID: ${escapeHTML(String(complaint.id ?? ""))}
        </div>

        <div class="complaint-details">
            <span class="priority ${getPriorityClass(complaint.priority)}">
                ${escapeHTML(complaint.priority || "")}
            </span>
        </div>

        <p>${escapeHTML(complaint.description || "")}</p>

        <p class="ai-prediction">
            ${predictionText}${confidenceText}
        </p>
    `;

    complaintsContainer.appendChild(card);
}

function getPriorityClass(priority) {
    if (priority === "Critical") return "critical";
    if (priority === "High") return "high";
    if (priority === "Medium") return "medium";
    return "low";
}

function getStatusClass(status) {
    if (status === "Resolved") return "resolved";
    if (status === "In Progress") return "progress";
    return "open";
}

function escapeHTML(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
