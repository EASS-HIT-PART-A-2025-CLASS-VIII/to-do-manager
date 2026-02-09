import ollama
import os


def get_client():
    host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    return ollama.Client(host=host)


def categorize_task(title: str, description: str):
    t = title.lower()
    if any(w in t for w in ["clean", "laundry", "house", "kitchen", "home"]):
        return {"category": "Personal", "emoji": "🏠"}
    if any(w in t for w in ["run", "workout", "gym", "fitness", "health", "walk"]):
        return {"category": "Health", "emoji": "🏥"}
    if any(w in t for w in ["exam", "study", "learn", "university", "algorithms", "test"]):
        return {"category": "Study", "emoji": "📚"}
    if any(w in t for w in ["sprint", "project", "report", "work", "meeting", "api"]):
        return {"category": "Work", "emoji": "💻"}
    if any(w in t for w in ["buy", "shop", "groceries", "order", "price"]):
        return {"category": "Shopping", "emoji": "🛒"}

    client = get_client()
    prompt = f"Task: {title}\nCategory (Work, Study, Personal, Shopping, Health):"

    try:
        response = client.generate(
            model='tinyllama',
            prompt=prompt,
            options={"num_predict": 5, "temperature": 0}
        )
        res = response['response'].strip().lower()

        if "studi" in res or "study" in res: return {"category": "Study", "emoji": "📚"}
        if "work" in res: return {"category": "Work", "emoji": "💻"}
        if "person" in res: return {"category": "Personal", "emoji": "🏠"}
        if "shop" in res: return {"category": "Shopping", "emoji": "🛒"}
        if "health" in res: return {"category": "Health", "emoji": "🏥"}

        return {"category": "General", "emoji": "📝"}
    except Exception:
        return {"category": "General", "emoji": "📝"}


def generate_task_description(title: str):
    client = get_client()

    prompt = f"Provide a 4-word expert tip for: {title}\nTip:"

    try:
        response = client.generate(
            model='tinyllama',
            prompt=prompt,
            options={
                "num_predict": 15,
                "temperature": 0.3,
                "stop": ["\n", ".", "!", "Task:"]
            }
        )

        res = response['response'].strip()

        clean_res = res.replace("Tip:", "").replace('"', "").strip()

        if len(clean_res) < 10 or clean_res.endswith(",") or "an" == clean_res[-2:]:
            if any(w in title.lower() for w in ["exam", "test", "study"]):
                return "Review key formulas and practice."
            if any(w in title.lower() for w in ["bug", "fix", "code"]):
                return "Isolate the logic and debug."
            return "Plan your execution steps carefully."

        return clean_res.capitalize()

    except Exception:
        return "Focus on the main objectives."