# frontend/streamlit_app.py

from datetime import date
from typing import List, Dict

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"


def apply_custom_css():
    """Apply custom purple theme styling."""
    st.markdown("""
        <style>
        /* Main theme colors */
        :root {
            --primary-purple: #8154B3;
            --light-purple: #9B7BC4;
            --dark-purple: #6B42A0;
            --purple-bg: #F5F1FA;
            --purple-accent: #E8DEFF;
        }

        /* Main container background */
        .main {
            background: linear-gradient(135deg, #F5F1FA 0%, #FFFFFF 100%);
        }

        /* Headers styling */
        h1, h2, h3 {
            color: #000000 !important;
            font-weight: 700 !important;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #8154B3 0%, #6B42A0 100%);
        }

        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #FFFFFF;
            color: black;
            border: 2px solid #E8DEFF;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #6B42A0;
            border-color: #6B42A0;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(129, 84, 179, 0.3);
        }

        /* Form submit button - override for create task button */
        .stForm button,
        form button,
        [data-testid="stFormSubmitButton"] button,
        div[data-testid="stForm"] button {
            background-color: #FFFFFF !important;
            color: black !important;
            border: 2px solid #E8DEFF !important;
        }

        .stForm button:hover,
        form button:hover,
        [data-testid="stFormSubmitButton"] button:hover,
        div[data-testid="stForm"] button:hover {
            background-color: #6B42A0 !important;
            color: white !important;
            border: 2px solid #6B42A0 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(129, 84, 179, 0.3) !important;
        }

        /* Form styling */
        [data-testid="stForm"] {
            background-color: white;
            border: 2px solid #E8DEFF;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(129, 84, 179, 0.1);
        }

        /* Input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stDateInput > div > div > input {
            border: 2px solid #E8DEFF;
            border-radius: 8px;
            padding: 0.5rem;
            transition: border-color 0.3s ease;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus,
        .stDateInput > div > div > input:focus {
            border-color: #8154B3;
            box-shadow: 0 0 0 2px rgba(129, 84, 179, 0.1);
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #F5F1FA !important;
            border: 2px solid #E8DEFF !important;
            border-radius: 8px !important;
            color: #8154B3 !important;
            font-weight: 600 !important;
        }

        .streamlit-expanderHeader:hover {
            background-color: #E8DEFF !important;
        }

        /* Metrics styling */
        [data-testid="stMetricValue"] {
            color: #8154B3 !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricLabel"] {
            color: #6B42A0 !important;
            font-weight: 600 !important;
        }

        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #F5F1FA 0%, #E8DEFF 100%);
            border: 2px solid #E8DEFF;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 2px 8px rgba(129, 84, 179, 0.1);
        }

        /* Success/Error messages */
        .stSuccess {
            background-color: #E8DEFF !important;
            color: #6B42A0 !important;
            border-left: 4px solid #8154B3 !important;
        }

        .stError {
            border-left: 4px solid #8154B3 !important;
        }

        /* Info box */
        .stInfo {
            background-color: #F5F1FA !important;
            border-left: 4px solid #8154B3 !important;
        }

        /* Horizontal rule */
        hr {
            border-color: #E8DEFF !important;
            opacity: 0.5;
        }

        /* Caption text */
        .css-fg4pbf, .st-emotion-cache-fg4pbf {
            color: #9B7BC4 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def fetch_tasks() -> List[Dict]:
    """Fetch all tasks from the FastAPI backend."""
    resp = requests.get(f"{API_URL}/tasks")
    resp.raise_for_status()
    return resp.json()


def create_task(title: str, description: str, status: str, due_date: date | None):
    """Create a new task via the API."""
    payload = {
        "title": title,
        "description": description or None,
        "status": status,
        "due_date": due_date.isoformat() if due_date else None,
    }
    resp = requests.post(f"{API_URL}/tasks", json=payload)
    resp.raise_for_status()
    return resp.json()


def update_task_status(task_id: int, new_status: str):
    """Update an existing task's status."""
    payload = {"status": new_status}
    resp = requests.put(f"{API_URL}/tasks/{task_id}", json=payload)
    resp.raise_for_status()
    return resp.json()


def delete_task(task_id: int):
    """Delete a task via the API."""
    resp = requests.delete(f"{API_URL}/tasks/{task_id}")
    resp.raise_for_status()
    return resp.json()


def main():
    st.set_page_config(page_title="ToDo Manager", page_icon="✔️", layout="wide")

    # Apply custom CSS
    apply_custom_css()

    st.title("✔️ ToDo Manager – Task Dashboard")
    st.caption("Friendly interface on top of the FastAPI Task Service (EX2).")

    with st.sidebar:
        st.header("⚙️ Settings")
        st.write("Make sure the FastAPI server is running at:")
        st.markdown(f'<p style="color: #9B7BC4; background-color: rgba(155, 123, 196, 0.2); padding: 8px; border-radius: 4px; font-family: monospace;">{API_URL}</p>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 🔎 How to use")
        st.markdown(
            "- Start the FastAPI server (uvicorn)\n"
            "- Use the form to create tasks\n"
            "- See tasks below and mark them as done\n"
            "- Delete tasks you no longer need"
        )

    # --- Create new task form ---
    st.subheader("➕ Add a new task")
    with st.form("create_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title", placeholder="Finish FastAPI EX2", max_chars=200)
            description = st.text_area(
                "Description",
                placeholder="Optional – add details about the task",
                max_chars=1000,
                height=80,
            )
        with col2:
            status = st.selectbox(
                "Status",
                options=["todo", "in_progress", "done"],
                format_func=lambda s: s.replace("_", " ").title(),
            )
            due_date = st.date_input(
                "Due date (optional)",
                value=None,
                format="YYYY-MM-DD",
            )

        submitted = st.form_submit_button("Create task")
        if submitted:
            if not title.strip():
                st.error("Title is required.")
            else:
                try:
                    created = create_task(title.strip(), description.strip(), status, due_date if due_date else None)
                    st.success(f"Task created (id={created['id']})")
                except requests.HTTPError as e:
                    st.error(f"Failed to create task: {e.response.text}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

    st.markdown("---")

    st.subheader("📓 Tasks")

    try:
        tasks = fetch_tasks()
    except requests.ConnectionError:
        st.error("Could not connect to the API. Is the FastAPI server running on 127.0.0.1:8000?")
        return
    except Exception as e:
        st.error(f"Failed to fetch tasks: {e}")
        return

    if not tasks:
        st.info("No tasks yet. Use the form above to create your first task.")
        return

    # Extra: summary metric (counts per status)
    st.markdown("#### Summary")
    status_counts: Dict[str, int] = {"todo": 0, "in_progress": 0, "done": 0}
    for t in tasks:
        status_counts[t["status"]] = status_counts.get(t["status"], 0) + 1

    m1, m2, m3 = st.columns(3)
    m1.metric("📋 Todo", status_counts.get("todo", 0))
    m2.metric("⚡ In Progress", status_counts.get("in_progress", 0))
    m3.metric("✅ Done", status_counts.get("done", 0))

    st.markdown("#### All tasks")

    # Show tasks with actions
    for t in tasks:
        status_emoji = {"todo": "📋", "in_progress": "⚡", "done": "✅"}
        emoji = status_emoji.get(t["status"], "📋")

        with st.expander(f"{emoji} [#{t['id']}] {t['title']} – {t['status'].replace('_', ' ').title()}"):
            st.write("**Description:**", t.get("description") or "_No description_")
            st.write("**Due date:**", t.get("due_date") or "_None_")
            st.write("**Created at:**", t.get("created_at"))

            c1, c2, c3 = st.columns(3)
            with c1:
                new_status = st.selectbox(
                    "Update status",
                    options=["todo", "in_progress", "done"],
                    index=["todo", "in_progress", "done"].index(t["status"]),
                    key=f"status-{t['id']}",
                    format_func=lambda s: s.replace("_", " ").title(),
                )
            with c2:
                if st.button("💾 Save status", key=f"save-{t['id']}"):
                    try:
                        update_task_status(t["id"], new_status)
                        st.success("Status updated. Refresh to see changes.")
                    except requests.HTTPError as e:
                        st.error(f"Failed to update task: {e.response.text}")
                    except Exception as e:
                        st.error(f"Unexpected error: {e}")
            with c3:
                if st.button("🗑️ Delete task", key=f"delete-{t['id']}"):
                    try:
                        delete_task(t["id"])
                        st.success("Task deleted. Refresh to see changes.")
                    except requests.HTTPError as e:
                        st.error(f"Failed to delete task: {e.response.text}")
                    except Exception as e:
                        st.error(f"Unexpected error: {e}")

    if st.button("🔄 Refresh tasks"):
        st.rerun()


if __name__ == "__main__":
    main()