# frontend/streamlit_app.py

from datetime import date
from typing import List, Dict

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"


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
    st.title("✔️ ToDo Manager – Task Dashboard")
    st.caption("Friendly interface on top of the FastAPI Task Service (EX2).")

    with st.sidebar:
        st.header("⚙️ Settings")
        st.write("Make sure the FastAPI server is running at:")
        st.code(API_URL, language="bash")
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

    st.subheader("🎯 Tasks")

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

    st.markdown("#### Summary")
    status_counts: Dict[str, int] = {"todo": 0, "in_progress": 0, "done": 0}
    for t in tasks:
        status_counts[t["status"]] = status_counts.get(t["status"], 0) + 1

    m1, m2, m3 = st.columns(3)
    m1.metric("Todo", status_counts.get("todo", 0))
    m2.metric("In Progress", status_counts.get("in_progress", 0))
    m3.metric("Done", status_counts.get("done", 0))

    st.markdown("#### All tasks")

    # Show tasks with actions
    for t in tasks:
        with st.expander(f"[#{t['id']}] {t['title']} – {t['status'].replace('_', ' ').title()}"):
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
                if st.button("Save status", key=f"save-{t['id']}"):
                    try:
                        update_task_status(t["id"], new_status)
                        st.success("Status updated. Refresh to see changes.")
                    except requests.HTTPError as e:
                        st.error(f"Failed to update task: {e.response.text}")
                    except Exception as e:
                        st.error(f"Unexpected error: {e}")
            with c3:
                if st.button("Delete task", key=f"delete-{t['id']}"):
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
