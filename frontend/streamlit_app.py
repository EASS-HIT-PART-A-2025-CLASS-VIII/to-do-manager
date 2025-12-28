import streamlit as st
import pandas as pd
import api_client as api


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="ToDo Manager", page_icon="✔️", layout="wide")

    try:
        local_css("frontend/assets/style.css")
    except:
        pass

    st.title("✔️ ToDo Manager – Task Dashboard")
    st.caption("Professional interface for your FastAPI Task Service.")

    with st.sidebar:
        st.header("⚙️ Settings")
        st.write("Make sure the FastAPI server is running at:")
        st.markdown(
            f'<p style="color: #9B7BC4; background-color: rgba(155, 123, 196, 0.2); padding: 8px; border-radius: 4px; font-family: monospace;">{api.API_URL}</p>',
            unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 🔎 How to use")
        st.markdown(
            "- Start the FastAPI server (uvicorn)\n"
            "- Use the form to create tasks\n"
            "- See tasks below and mark them as done\n"
            "- Delete tasks you no longer need"
        )

        st.markdown("---")

        try:
            tasks = api.fetch_tasks()
            if tasks:
                st.markdown("### 📥 Backup")
                df = pd.DataFrame(tasks)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Export to CSV", data=csv, file_name="tasks_export.csv", mime="text/csv")
        except:
            tasks = []
            st.error("Backend unreachable.")

    # Create Task Form
    st.subheader("➕ Add a new task")
    with st.form("create_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title", max_chars=200)
            description = st.text_area("Description", max_chars=1000, height=80)
        with col2:
            status = st.selectbox("Status", options=["todo", "in_progress", "done"],
                                  format_func=lambda s: s.replace("_", " ").title())
            due_date = st.date_input("Due date (optional)", value=None)

        if st.form_submit_button("Create task"):
            if title.strip():
                api.create_task({"title": title.strip(), "description": description.strip(), "status": status,
                                 "due_date": str(due_date) if due_date else None})
                st.rerun()

    st.markdown("---")

    # Summary Metrics
    if tasks:
        st.subheader("📓 Summary")
        status_counts = {"todo": 0, "in_progress": 0, "done": 0}
        for t in tasks: status_counts[t["status"]] = status_counts.get(t["status"], 0) + 1

        m1, m2, m3 = st.columns(3)
        m1.metric("📋 Todo", status_counts.get("todo", 0))
        m2.metric("⚡ In Progress", status_counts.get("in_progress", 0))
        m3.metric("✅ Done", status_counts.get("done", 0))

        st.markdown("#### All tasks")
        for t in tasks:
            status_emoji = {"todo": "📋", "in_progress": "⚡", "done": "✅"}
            emoji = status_emoji.get(t["status"], "📋")
            fav_icon = "⭐" if t.get("is_favorite") else "☆"

            with st.expander(f"{fav_icon} {emoji} [#{t['id']}] {t['title']}"):
                st.markdown(f"**Description:** {t.get('description') or '_No description_'}")
                st.markdown(f"**Due Date:** `{t.get('due_date') or 'None'}`")

                st.write("---")

                # Mapping for display vs logic to fix 422 error
                status_options = ["todo", "in_progress", "done"]
                status_display = {"todo": "ToDo", "in_progress": "In Progress", "done": "Done"}

                # Layout for alignment
                st.caption("Update Status")
                c_select, _ = st.columns([1, 3])
                with c_select:
                    new_status = st.selectbox(
                        "Status",
                        options=status_options,
                        index=status_options.index(t["status"]),
                        format_func=lambda x: status_display[x],
                        key=f"s-{t['id']}",
                        label_visibility="collapsed"
                    )

                # Grouped Action Buttons on the Left
                b1, b2, b3, _ = st.columns([0.15, 0.2, 0.15, 1.5])
                with b1:
                    if st.button("💾 Save", key=f"sv-{t['id']}"):
                        api.update_task(t['id'], {"status": new_status})
                        st.rerun()
                with b2:
                    fav_label = "⭐ Fav" if t.get("is_favorite") else "☆ Fav"
                    if st.button(fav_label, key=f"fv-{t['id']}"):
                        api.toggle_favorite(t['id'])
                        st.rerun()
                with b3:
                    if st.button("🗑️ Delete", key=f"dl-{t['id']}"):
                        api.delete_task(t['id'])
                        st.rerun()


if __name__ == "__main__":
    main()