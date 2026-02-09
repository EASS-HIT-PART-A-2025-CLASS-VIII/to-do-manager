import requests
from typing import List, Dict

API_URL = "http://backend:8000"

def fetch_tasks() -> List[Dict]:
    resp = requests.get(f"{API_URL}/tasks")
    resp.raise_for_status()
    return resp.json()

def create_task(payload: Dict):
    resp = requests.post(f"{API_URL}/tasks", json=payload)
    resp.raise_for_status()
    return resp.json()

def update_task(task_id: int, payload: Dict):
    resp = requests.put(f"{API_URL}/tasks/{task_id}", json=payload)
    resp.raise_for_status()
    return resp.json()

def toggle_favorite(task_id: int):
    resp = requests.patch(f"{API_URL}/tasks/{task_id}/favorite")
    resp.raise_for_status()
    return resp.json()

def delete_task(task_id: int):
    resp = requests.delete(f"{API_URL}/tasks/{task_id}")
    resp.raise_for_status()

def generate_ai_description(task_id):
    try:
        response = requests.patch(f"{API_URL}/tasks/{task_id}/generate-description")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error generating AI description: {e}")
        return None
