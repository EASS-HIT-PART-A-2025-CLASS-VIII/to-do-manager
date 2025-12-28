# Task Service – ToDoManager (FastAPI + Streamlit)

This project implements a full-stack task management application with:

- **Backend**: FastAPI microservice with SQLite persistence.
- **Frontend**: Streamlit UI with custom CSS, real-time API integration, and data export.

---

## 🌟 New Professional Features
- **Persistence**: Switched from in-memory to a **SQLite Database** via SQLAlchemy. Your tasks remain saved after restarts.
- **Layered Architecture**: Organized into API, Repository, and Model layers for clean, maintainable code.
- **Mark Favorites**: Toggle a ⭐ status on tasks to highlight priorities.
- **Data Export**: Sidebar tool to download your task list as a **CSV file**.
- **Refined UI**: Left-aligned action buttons and custom purple-themed components.

---

## 📂 Project Structure



```text
ToDoManager/
├── app/
│   ├── api/            # Route handlers (FastAPI Decorators)
│   │   └── tasks.py
│   ├── core/           # Configuration & Global Constants
│   │   └── config.py
│   ├── models/         # Database Models (SQLAlchemy)
│   │   └── task_db.py
│   ├── repository/     # Data Access Logic (CRUD + Business Logic)
│   │   └── task_repo.py
│   ├── schemas/        # Data Validation (Pydantic)
│   │   └── task_schema.py
│   ├── database.py     # Connection setup & Session management
│   ├── exceptions.py   # Custom Error types
│   └── main.py         # App Entry Point & Global Exception Handlers
│   └── __init__.py
├── frontend/
│   ├── assets/         # UI styling
│   │   └── style.css
│   ├── api_client.py   # API Communication Logic (Separated from UI)
│   └── streamlit_app.py# Main Streamlit UI Layout
├── tests/
│   └── test_to_do_manager.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# 🚀 Getting Started

This project uses **uv** for environment management and dependency installation.

## 1. Create a uv virtual environment

From the project root:

```bash
uv venv
```

## 2. Activate the environment

**Windows (PowerShell):**
```bash
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

# 🖥️ Running the Application

## Step 1: Start the FastAPI Backend

First, start the FastAPI server:

```bash
uv run uvicorn app.main:app --reload
```

The backend server runs on: **http://127.0.0.1:8000**

Swagger UI documentation: **http://127.0.0.1:8000/docs**

## Step 2: Start the Streamlit Frontend

In a **new terminal window** (with the virtual environment activated), run:

```bash
streamlit run frontend/streamlit_app.py
```

The Streamlit UI will open automatically in your browser at: **http://localhost:8501**

---

# 🎨 Streamlit UI Overview

The Streamlit frontend provides a beautiful, purple-themed interface for managing your tasks.

## UI Features

### **Sidebar**
- **Settings**: Displays the FastAPI server address
- **Backup**: Export to CSV button to download your data
- **How to use**: Quick guide for getting started

### **Main Dashboard**

#### **➕ Add a new task**
A form to create new tasks with the following fields:
- **Title** (required): Short description of the task
- **Description** (optional): Additional details
- **Status**: Choose from Todo, In Progress, or Done
- **Due date** (optional): Set a deadline

The "Create task" button has a custom hover effect (white background → dark purple on hover).

#### **📓 Tasks Section**

**Summary Metrics**: 
- Visual count cards showing:
  - 📋 Todo tasks
  - ⚡ In Progress tasks
  - ✅ Done tasks

**All Tasks List**:
- Tasks displayed in expandable cards with status emojis
- Each task shows:
  - Task ID and title
  - Description
  - Due date
  - Created timestamp
- **Actions per task**:
  - Update status dropdown
  - Mark as favorite
  - 💾 Save status button
  - 🗑️ Delete task button

#### **🔄 Refresh Tasks Button**
Updates the task list with the latest data from the backend

---

# 🔌 API Overview

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/tasks` | List all tasks |
| GET    | `/tasks/{id}` | Retrieve a task by ID |
| POST   | `/tasks` | Create a new task |
| PUT    | `/tasks/{id}` | Update an existing task |
| PATCH  | `/tasks/{id}/favorite` | Toggle favorite status |
| DELETE | `/tasks/{id}` | Delete a task by ID |

## Request/Response Examples

**GET** `/tasks`
```json
[
  {
    "title": "Do laundry",
    "description": "important",
    "status": "todo",
    "due_date": "2025-12-01",
    "id": 1,
    "created_at": "2025-12-01T10:16:01.071856"
  }
]
```

**POST** `/tasks`
```json
{
  "title": "Do laundry",
  "description": "important",
  "status": "todo",
  "due_date": "2025-12-01"
}
```

**DELETE** `/tasks/{id}`
```json
{
  "message": "Task 1 deleted successfully"
}
```

---

# 🧪 Running Tests

The project uses pytest + FastAPI's TestClient.

To run the test suite:

```bash
uv run pytest
```

---

# 🐳 Docker

This project includes a Dockerfile so the API can run inside a container.

**Build the Docker image:**
```bash
docker build -t todo-manager .
```

**Run the container:**
```bash
docker run -p 8000:8000 todo-manager
```

**Note**: When using Docker, update the `API_URL` in `streamlit_app.py` if accessing from a different host.

---

# 📝 Notes

- Make sure the FastAPI backend is running before starting the Streamlit frontend
- The application uses an in-memory repository, so data will be lost when the server restarts
- All task operations are performed through the REST API
- The UI automatically refreshes after creating, updating, or deleting tasks

---

# 🛠️ Troubleshooting

**Cannot connect to API error in Streamlit:**
- Ensure the FastAPI server is running on http://127.0.0.1:8000
- Check that no firewall is blocking the connection

**Port already in use:**
- FastAPI default: 8000
- Streamlit default: 8501
- Use different ports if these are occupied

---

# 📚 Technology Stack

- **Backend**: FastAPI, Pydantic, Uvicorn
- **Frontend**: Streamlit
- **Testing**: pytest, TestClient
- **Environment**: uv (Python package manager)
- **Containerization**: Docker