
// ==========================================
// API URL
// ==========================================

const API_URL = "http://localhost:8080/api/complaints";
let adminAuthHeader = "";

// ==========================================
// DASHBOARD MESSAGE
// ==========================================

function showDashboardMessage(message, isError = false) {

    const messageBox = document.getElementById("dashboard-message");

    messageBox.textContent = message;
    messageBox.hidden = false;

    messageBox.classList.toggle("error", isError);
}

// ==========================================
// LOAD CATEGORY STATISTICS FROM BACKEND
// ==========================================

async function loadCategoryStatistics() {

    try {
        const response = await fetch(
            `${API_URL}/analytics/categories`,
            {
                method: "GET",
                headers: {
                    "Authorization": adminAuthHeader
                }
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error("Error loading category statistics:", error);
        return {};
    }
}

// ==========================================
// LOAD PRIORITY STATISTICS FROM BACKEND
// ==========================================

async function loadPriorityStatistics() {

    try {
        const response = await fetch(
            `${API_URL}/analytics/priorities`,
            {
                method: "GET",
                headers: {
                    "Authorization": adminAuthHeader
                }
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error("Error loading priority statistics:", error);
        return {};
    }
}
// ==========================================
// LOAD STATUS STATISTICS FROM BACKEND
// ==========================================

async function loadStatusStatistics() {
    try {
        const response = await fetch(
            `${API_URL}/analytics/statuses`,
            {
                method: "GET",
                headers: {
                    "Authorization": adminAuthHeader
                }
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error("Error loading status statistics:", error);
        return {};
    }
}

// ==========================================
// LOAD DATE STATISTICS FROM BACKEND
// ==========================================

async function loadDateStatistics() {
    try {
        const response = await fetch(
            `${API_URL}/analytics/dates`,
            {
                method: "GET",
                headers: {
                    "Authorization": adminAuthHeader
                }
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error("Error loading date statistics:", error);
        return {};
    }
}
// Store all complaints received from backend

let allComplaints = [];

// Store chart instances
let categoryChartInstance = null;
let priorityChartInstance = null;
let statusChartInstance = null;
let dateChartInstance = null;
let sparkCategoryChartInstance = null;

// ==========================================
// PAGE INITIALIZATION
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // Admin Login
document.getElementById("admin-login-form")
    .addEventListener("submit", async function (event) {

        event.preventDefault();

        const username =
            document.getElementById("admin-username").value;

        const password =
            document.getElementById("admin-password").value;

        const loginMessage =
            document.getElementById("login-message");

        const loginButton =
            this.querySelector("button");

        const credentials = btoa(username + ":" + password);

        loginButton.disabled = true;
        loginButton.textContent = "Logging in...";

        try {

            const response = await fetch(API_URL, {
                method: "GET",
                headers: {
                    "Authorization": "Basic " + credentials
                }
            });

            if (!response.ok) {
                throw new Error("Invalid username or password.");
            }

            adminAuthHeader = "Basic " + credentials;

            const dashboardLoaded = await loadAdminComplaints();

            if (!dashboardLoaded) {
                adminAuthHeader = "";

                loginMessage.textContent =
                    "Login succeeded, but dashboard could not load. Please try again.";

                loginMessage.hidden = false;

                return;
            }

            document.getElementById("admin-login").hidden = true;
            document.getElementById("admin-dashboard").hidden = false;

            loginMessage.hidden = true;

            document.getElementById("admin-password").value = "";

        } catch (error) {

            loginMessage.textContent =
                "Login failed. Please check your username and password.";

            loginMessage.hidden = false;

        } finally {

            loginButton.disabled = false;
            loginButton.textContent = "Login";

        }

    });
    
    // Admin Logout
    document.getElementById("admin-logout")
        .addEventListener("click", function () {

            // Clear admin authentication
            adminAuthHeader = "";

            // Hide dashboard
            document.getElementById("admin-dashboard").hidden = true;

            // Show login section
            document.getElementById("admin-login").hidden = false;

            // Clear login fields
            document.getElementById("admin-username").value = "";
            document.getElementById("admin-password").value = "";

            // Clear login message
            document.getElementById("login-message").hidden = true;

        });
    // Search listener

    document.getElementById("search-complaints")
        .addEventListener("input", filterComplaints);

    // Status filter listener

    document.getElementById("status-filter")
        .addEventListener("change", filterComplaints);

    // Priority filter listener

    document.getElementById("priority-filter")
        .addEventListener("change", filterComplaints);

    // Category filter listener

    document.getElementById("category-filter")
        .addEventListener("change", filterComplaints);

});


// ==========================================
// LOAD COMPLAINTS FROM SPRING BOOT
// ==========================================

async function loadAdminComplaints() {

    const tableBody =
        document.getElementById("complaints-table-body");
        showDashboardMessage("Loading dashboard...");

    try {

        const response = await fetch(API_URL, {
            method: "GET",
            headers: {
                "Authorization": adminAuthHeader
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        allComplaints = await response.json();


        // Update dashboard statistics from backend

        await loadDashboardStatistics();


        // Display complaints

        displayAdminComplaints(allComplaints);

        // Update analytics charts

        updateAnalyticsCharts(allComplaints);

        document.getElementById("dashboard-message").hidden = true;

        return true;

    } catch (error) {

        console.error("Error loading complaints:", error);

        showDashboardMessage(
            "Unable to load dashboard. Please check your backend connection.",
            true
        );

        tableBody.innerHTML = `
            <tr>
                <td colspan="8">
                    Unable to load complaints. Check whether Spring Boot is running.
                </td>
            </tr>
        `;
        return false;

    }
    // ==========================================
    // LOAD DASHBOARD STATISTICS FROM BACKEND
    // ==========================================

    async function loadDashboardStatistics() {

        try {
            const response = await fetch(`${API_URL}/statistics`, {
                method: "GET",
                headers: {
                    "Authorization": adminAuthHeader
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            const statistics = await response.json();

            document.getElementById("total-complaints").textContent =
                statistics.totalComplaints;

            document.getElementById("open-complaints").textContent =
                statistics.open;

            document.getElementById("progress-complaints").textContent =
                statistics.inProgress;

            document.getElementById("resolved-complaints").textContent =
                statistics.resolved;

        } catch (error) {
            console.error("Error loading dashboard statistics:", error);
        }
    }

}


// ==========================================
// UPDATE DASHBOARD STATISTICS
// ==========================================

function updateStatistics(complaints) {

    const totalComplaints = complaints.length;


    const openComplaints = complaints.filter(function (complaint) {

        return complaint.status === "Open" ||
               complaint.status === "Pending";

    }).length;


    const progressComplaints = complaints.filter(function (complaint) {

        return complaint.status === "In Progress";

    }).length;


    const resolvedComplaints = complaints.filter(function (complaint) {

        return complaint.status === "Resolved";

    }).length;


    document.getElementById("total-complaints").textContent =
        totalComplaints;


    document.getElementById("open-complaints").textContent =
        openComplaints;


    document.getElementById("progress-complaints").textContent =
        progressComplaints;


    document.getElementById("resolved-complaints").textContent =
        resolvedComplaints;

}


// ==========================================
// GET PRIORITY CSS CLASS
// ==========================================

function getPriorityClass(priority) {

    if (priority === "Critical") {
        return "critical";
    }

    if (priority === "High") {
        return "high";
    }

    if (priority === "Medium") {
        return "medium";
    }

    if (priority === "Low") {
        return "low";
    }

    return "";

}


// ==========================================
// DISPLAY COMPLAINTS IN TABLE
// ==========================================

function displayAdminComplaints(complaints) {

    const tableBody =
        document.getElementById("complaints-table-body");


    // Clear previous table rows

    tableBody.innerHTML = "";


    // Check whether complaints exist

    if (complaints.length === 0) {

        tableBody.innerHTML = `
            <tr>
                <td colspan="8">
                    No complaints found.
                </td>
            </tr>
        `;

        return;
    }


    // Display each complaint

    complaints.forEach(function (complaint) {

        const row = document.createElement("tr");


        // Format date

        const complaintDate = complaint.createdAt
            ? new Date(complaint.createdAt).toLocaleString()
            : "N/A";


        // Create status dropdown

        const statusSelect = document.createElement("select");

        statusSelect.className = "status-select";


        const statuses = [
            "Pending",
            "Open",
            "In Progress",
            "Resolved"
        ];


        statuses.forEach(function (status) {

            const option = document.createElement("option");

            option.value = status;

            option.textContent = status;

            if (complaint.status === status) {
                option.selected = true;
            }

            statusSelect.appendChild(option);

        });


        // Update status when dropdown changes

        statusSelect.addEventListener("change", function () {

            updateComplaintStatus(
                complaint.id,
                statusSelect.value,
                statusSelect
            );

        });


        // Create table cells

        const idCell = document.createElement("td");
        idCell.textContent = complaint.id;


        const nameCell = document.createElement("td");
        nameCell.textContent = complaint.name || "N/A";


        const categoryCell = document.createElement("td");
        categoryCell.textContent = complaint.category || "N/A";

        // Create description cell
        const descriptionCell = document.createElement("td");

        const description = complaint.description || "N/A";

        descriptionCell.textContent = description;

        // Show complete description on hover
        descriptionCell.title = description;


        const predictionCell = document.createElement("td");
        predictionCell.textContent =
            complaint.predictedCategory || "N/A";


        const priorityCell = document.createElement("td");

        const prioritySpan = document.createElement("span");

        prioritySpan.className =
            `priority ${getPriorityClass(complaint.priority)}`;

        prioritySpan.textContent = complaint.priority || "N/A";

        priorityCell.appendChild(prioritySpan);


        const dateCell = document.createElement("td");
        dateCell.textContent = complaintDate;


        const statusCell = document.createElement("td");
        statusCell.appendChild(statusSelect);


        // Add cells to row

        row.appendChild(idCell);
        row.appendChild(nameCell);
        row.appendChild(categoryCell);
        row.appendChild(descriptionCell);
        row.appendChild(predictionCell);
        row.appendChild(priorityCell);
        row.appendChild(dateCell);
        row.appendChild(statusCell);


        // Add row to table

        tableBody.appendChild(row);

    });

}


// ==========================================
// SEARCH AND FILTER COMPLAINTS
// ==========================================

function filterComplaints() {

    const searchValue =
        document.getElementById("search-complaints")
            .value.toLowerCase();


    const selectedStatus =
        document.getElementById("status-filter").value;


    const selectedPriority =
        document.getElementById("priority-filter").value;

    const selectedCategory =
        document.getElementById("category-filter").value;


    // Apply all filters

    const filteredComplaints = allComplaints.filter(
        function (complaint) {

            const matchesSearch =
                String(complaint.id).includes(searchValue) ||
                (complaint.name || "")
                    .toLowerCase()
                    .includes(searchValue) ||
                (complaint.description || "")
                    .toLowerCase()
                    .includes(searchValue);


            const matchesStatus =
                selectedStatus === "" ||
                complaint.status === selectedStatus;


            const matchesPriority =
                selectedPriority === "" ||
                complaint.priority === selectedPriority;

            const matchesCategory =
                selectedCategory === "" ||
                complaint.category === selectedCategory;


            return matchesSearch &&
                   matchesStatus &&
                   matchesPriority &&
                   matchesCategory;

        }
    );


    // Display filtered complaints

    displayAdminComplaints(filteredComplaints);

}



// ==========================================
// UPDATE COMPLAINT STATUS - IMPROVED VERSION
// ==========================================

async function updateComplaintStatus(id, newStatus, statusSelect) {

    // Store the previous status
    const previousStatus = allComplaints.find(
        function (complaint) {
            return complaint.id === id;
        }
    )?.status || "Pending";


    // Disable dropdown while updating
    statusSelect.disabled = true;


    try {

        // Send PATCH request to Spring Boot
        const response = await fetch(`${API_URL}/${id}/status`, {

            method: "PATCH",

            headers: {
                "Content-Type": "application/json",
                "Authorization": adminAuthHeader
            },

            body: JSON.stringify({
                status: newStatus
            })

        });


        // Check API response
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }


        // Reload the latest data directly from backend
        await loadAdminComplaints();


        alert("Complaint status updated successfully!");


    } catch (error) {

        console.error("Status update failed:", error);


        // Reload backend data to restore the correct status
        await loadAdminComplaints();


        alert(
            `Failed to update complaint status.\n\nError: ${error.message}`
        );


    } finally {

        statusSelect.disabled = false;

    }

}


// ==========================================
// ANALYTICS CHARTS
// ==========================================

async function updateAnalyticsCharts(complaints) {

    // Do not continue if Chart.js is unavailable
    if (typeof Chart === "undefined") {
        console.error("Chart.js library is not loaded.");
        return;
    }


    // ==========================================
    // 1. COMPLAINTS BY CATEGORY
    // ==========================================

    const categoryCounts = await loadCategoryStatistics();

    if (categoryChartInstance) {
        categoryChartInstance.destroy();
    }

    categoryChartInstance = new Chart(
        document.getElementById("categoryChart"),
        {
            type: "doughnut",

            data: {
                labels: Object.keys(categoryCounts),

                datasets: [{
                    label: "Complaints",
                    data: Object.values(categoryCounts)
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: true
            }
        }
    );


    // ==========================================
    // 2. COMPLAINTS BY PRIORITY
    // ==========================================

    const priorities = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ];

    const priorityCountsFromBackend = await loadPriorityStatistics();

    const priorityCounts = priorities.map(function (priority) {
        return priorityCountsFromBackend[priority] || 0;
    });


    if (priorityChartInstance) {
        priorityChartInstance.destroy();
    }


    priorityChartInstance = new Chart(
        document.getElementById("priorityChart"),
        {
            type: "bar",

            data: {
                labels: priorities,

                datasets: [{
                    label: "Complaints",
                    data: priorityCounts
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: true,

                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        }
    );


    // ==========================================
    // 3. COMPLAINTS BY STATUS
    // ==========================================

    const statuses = [
        "Pending",
        "Open",
        "In Progress",
        "Resolved"
    ];

    const statusCountsFromBackend = await loadStatusStatistics();

    const statusCounts = statuses.map(function (status) {
        return statusCountsFromBackend[status] || 0;
    });


    if (statusChartInstance) {
        statusChartInstance.destroy();
    }


    statusChartInstance = new Chart(
        document.getElementById("statusChart"),
        {
            type: "pie",

            data: {
                labels: statuses,

                datasets: [{
                    label: "Complaints",
                    data: statusCounts
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: true
            }
        }
    );

    // ==========================================
    // 4. COMPLAINTS BY DATE
    // ==========================================

    const dateCounts = await loadDateStatistics();

    // Sort dates chronologically
    const sortedDates = Object.keys(dateCounts).sort();

    const dateLabels = sortedDates.map(function (date) {
        return new Date(date + "T00:00:00").toLocaleDateString();
    });

    const dateValues = sortedDates.map(function (date) {
        return dateCounts[date];
    });

    if (dateChartInstance) {
        dateChartInstance.destroy();
    }

    dateChartInstance = new Chart(
        document.getElementById("dateChart"),
        {
            type: "line",

            data: {
                labels: dateLabels,

                datasets: [{
                    label: "Complaints",
                    data: dateValues,
                    tension: 0.3
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: true,

                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        }
    );

    // Load Apache Spark Analytics
    await loadSparkCategoryAnalytics();
}

// ==========================================
// LOAD SPARK CATEGORY ANALYTICS
// ==========================================

async function loadSparkCategoryAnalytics() {

    try {

        // Request Spark analytics from Spring Boot
        const response = await fetch(
            `${API_URL}/spark/category-analytics`,
            {
                method: "GET",
                headers: {
                    "Authorization": adminAuthHeader
                }
            }
        );

        // Check API response
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        // Convert JSON response into JavaScript object
        const sparkCategoryCounts = await response.json();

        // Get category names and complaint counts
        const categories = Object.keys(sparkCategoryCounts);
        const counts = Object.values(sparkCategoryCounts);

        // Destroy previous chart if it exists
        if (sparkCategoryChartInstance) {
            sparkCategoryChartInstance.destroy();
        }

        // Create Spark analytics chart
        sparkCategoryChartInstance = new Chart(
            document.getElementById("sparkCategoryChart"),
            {
                type: "bar",

                data: {
                    labels: categories,

                    datasets: [{
                        label: "Complaints Processed by Spark",
                        data: counts
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: true,

                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            }
        );

    } catch (error) {

        console.error(
            "Error loading Spark category analytics:",
            error
        );

    }
}