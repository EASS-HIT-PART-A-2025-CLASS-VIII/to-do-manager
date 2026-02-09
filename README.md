# Task Service – ToDoManager (FastAPI + Streamlit)

A full-stack task management application integrated with local LLMs for smart categorization and task assistance.
- **Backend**: FastAPI microservice with SQLite persistence.
- **Frontend**: Streamlit UI with custom CSS, real-time API integration, and data export.

---

## 🌟 New Features
- **🤖 AI Smart Categorization**: Automatically classifies tasks into categories (Work, Study, Health, etc.) using `TinyLlama`.
- **🪄 AI Task Assistant**: Generates actionable tips and detailed descriptions for tasks with a single click.
- **💾 Persistence**: SQLite Database via SQLAlchemy ensures your tasks are saved permanently.
- **⭐ Favorites**: Toggle priority status for important tasks.
- **🐳 Dockerized Architecture**: Seamless multi-container setup with Docker Compose.
- **📊 Data Export**: Export your task list to CSV directly from the sidebar.
---

## 📂 Project Structure



```text
ToDoManager/
├── app/
│   ├── api/            # Route handlers (FastAPI)
│   ├── core/           # AI Logic (Ollama/TinyLlama integration)
│   ├── models/         # Database Models (SQLAlchemy)
│   ├── repository/     # CRUD & Business Logic
│   ├── schemas/        # Pydantic validation
│   └── database.py     # Session management
├── frontend/
│   ├── api_client.py   # API Communication Logic
│   └── streamlit_app.py# Streamlit UI
├── docker-compose.yml  # Multi-container orchestration
├── Dockerfile          # Backend containerization
└── requirements.txt
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
## Prerequisites

1. Download and install Ollama from ollama.com
2. Installed on your system, uv (pip install uv)
3. Ensure the Ollama app is running, then pull the model:
```bash
ollama pull tinyllama
```
4. Install Dependencies - from project root
```bash
uv sync
```

## Step 1: Start the FastAPI Backend

### Set environment variable so the backend knows where Ollama is
```bash
export OLLAMA_HOST=http://localhost:11434  # macOS/Linux
$env:OLLAMA_HOST="http://localhost:11434" # Windows PowerShell
```

### Start the FastAPI server:

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
- **AI Categorization** Simply type a task in English (e.g., "Study for Automata exam"), and the AI will assign a category and emoji automatically
- **Magic Info Button** (🪄): Click "AI Info" on any task card to generate a smart tip or description using the local LLM.

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
  - 🪄 AI Info

#### **🔄 Refresh Tasks Button**
Updates the task list with the latest data from the backend

---

# 🔌 API Overview

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/tasks` | List all tasks |
| GET    | `/tasks/{id}` | Retrieve a task by ID |
| POST   | `/tasks` | Create a task (triggers AI classification) |
| PUT    | `/tasks/{id}` | Update an existing task |
| PATCH  | `/tasks/{id}/favorite` | Toggle favorite status |
| PATCH  | `/tasks/{id}/generate-description` | Triggers AI description generation |
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

The easiest way to run the entire application, including the AI engine and the database, is using Docker Compose. This ensures all services (Frontend, Backend, and Ollama) are correctly networked.
**Build the Docker image:**
```bash
docker-compose up --build
```

**Initialize the AI Engine**
In a new terminal, download the lightweight AI model:
```bash
docker exec -it ollama ollama pull tinyllama
```

### 📝 Docker Notes:
- Persistence: A Docker Volume named ollama_data is created to ensure your AI models stay saved even if the containers are stopped.
- Networking: Inside the Docker network, the Frontend communicates with the Backend using the hostname http://backend:8000.
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
- **AI Engine**: Ollama (Model: tinyllama)

# 📝 Performance Notes
Local AI: The AI model runs locally on your CPU. Ensure Docker is allocated at least 4GB of RAM for smooth performance.

Persistence: Data is stored in a SQLite file that persists through container restarts thanks to Docker Volumes.