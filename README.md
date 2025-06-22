🎲 Pixel D20 Roll Tracker API
This Flask API powers a logging and analytics backend for dice rolls sent from Pixel, a Bluetooth-enabled smart D20 die capable of firing off JSON payloads to any server.

📖 Overview
When a roll occurs, the Pixel die sends a POST request containing the rolled value and an associated unique pixelId. This app:

Stores that roll data in a SQLite database

Links it to a user

Exposes endpoints to create users, record rolls, and retrieve recent history

Includes a Swagger UI for exploring and testing the API

⚙️ Tech Stack
Python 3.8+

Flask

SQLAlchemy (with SQLite backend)

Flasgger (Swagger documentation)

Docker (optional containerized deployment)

🚚 Deployment (with Docker + deploy.sh)
This app includes a simple Docker setup and a deploy.sh helper script to streamline deployment.



📡 Start the App
bash
Copy
Edit
./deploy.sh
Then access it at: http://localhost:5000/apidocs

🔌 API Endpoints
➕ POST /api/users
Register a new user.

```
{
  "pixelId": "abc123",
  "username": "wizardroller"
}
Returns:

json
Copy
Edit
{
  "id": 1,
  "pixelId": "abc123",
  "username": "wizardroller"
}
```
🎲 POST /roll
Send a JSON payload from your Pixel die to log a roll.

```
{
  "pixelId": "abc123",
  "faceValue": 15
}
Returns:

{
  "message": "Roll recorded",
  "roll": {
    "id": 7,
    "value": 15,
    "timestamp": "2025-05-26T14:34:00Z",
    "user_id": 1,
    "pixelId": "abc123"
  }
}
```
📜 GET /rolls/<n?>
Retrieve the latest N rolls (default: 10) with associated user info.

Example:

```
GET /rolls/5
Returns:

json
Copy
Edit
[
  {
    "id": 21,
    "value": 18,
    "timestamp": "2025-06-21T18:04:00Z",
    "user": {
      "id": 1,
      "pixelId": "abc123",
      "username": "wizardroller"
    }
  }
]
```
🌐 Swagger UI
Explore and test endpoints at:

📍 http://localhost:5000/apidocs

🗃️ Database Info
SQLite file: ./assets/rolls.db. Please ensure this is mounted into the docker container.

Two tables: User, Roll

Each roll is linked to a user by user_id

📝 Logging
All HTTP requests (method, headers, body) are logged to the console using Python's built-in logging module.

📁 Project Structure
bash
Copy
Edit
project/
├── app.py              # Main application
├── models.py           # SQLAlchemy models
├── assets/             # Contains SQLite database
│   └── rolls.db
├── Dockerfile          # Docker config
├── deploy.sh           # Deployment helper script
├── requirements.txt    # Python dependencies
└── README.md           # You are here!
