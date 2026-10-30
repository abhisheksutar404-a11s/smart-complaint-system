
import csv
import random
from datetime import datetime, timedelta

# Generate repeatable sample data
random.seed(42)

# Output CSV file
output_file = "../data/synthetic_complaints.csv"

# Sample complaint information
complaints = {
    "Road": [
        "Road is damaged near my area",
        "Potholes are causing traffic problems",
        "Road repair work is incomplete"
    ],
    "Technical": [
        "My computer is not working",
        "Internet connection is unavailable",
        "Computer lab systems are not starting"
    ],
    "Finance": [
        "My scholarship payment is delayed",
        "Fee payment is not updated",
        "Incorrect amount charged in my account"
    ],
    "Library": [
        "Library books are unavailable",
        "Library computer is not working",
        "Unable to return a library book"
    ],
    "Maintenance": [
        "Water leakage in the building",
        "Classroom lights are not working",
        "Fans are not working properly"
    ],
    "Account": [
        "Unable to log in to my account",
        "Password reset is not working",
        "Account details are incorrect"
    ],
    "Other": [
        "I need assistance with a general issue",
        "Please look into this problem",
        "Request for administrative support"
    ]
}

categories = list(complaints.keys())
priorities = ["Low", "Medium", "High"]
statuses = ["Open", "Pending", "In Progress", "Resolved"]

locations = ["Kolhapur", "Pune", "Mumbai", "Nashik", "Nagpur"]

names = ["Rahul", "Amit", "Priya", "Sneha", "Rohit",
         "Neha", "Akash", "Pooja", "Kiran", "Anjali"]

fieldnames = [
    "id", "category", "created_at", "description",
    "email", "location", "name", "priority",
    "status", "confidence", "predicted_category"
]

# Generate 5000 synthetic records
with open(output_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for complaint_id in range(18, 5018):

        category = random.choice(categories)
        description = random.choice(complaints[category])

        created_at = datetime.now() - timedelta(
            days=random.randint(0, 180),
            minutes=random.randint(0, 1440)
        )

        confidence = round(random.uniform(0.60, 0.99), 4)

        # Randomly simulate missing values
        if random.random() < 0.15:
            location = "NULL"
        else:
            location = random.choice(locations)

        if random.random() < 0.10:
            confidence_value = "NULL"
            predicted_category = "NULL"
        else:
            confidence_value = confidence
            predicted_category = category

        writer.writerow({
            "id": complaint_id,
            "category": category,
            "created_at": created_at.strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            ),
            "description": description,
            "email": f"user{complaint_id}@example.com",
            "location": location,
            "name": random.choice(names),
            "priority": random.choice(priorities),
            "status": random.choice(statuses),
            "confidence": confidence_value,
            "predicted_category": predicted_category
        })

print("Synthetic dataset generated successfully!")
print("Total synthetic complaints: 5000")
print("Output file:", output_file)
