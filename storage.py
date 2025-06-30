
import json, pathlib, datetime
DATA_PATH = pathlib.Path("pdi_data.json")

def load_data():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_session(email, session_data):
    data = load_data()
    timestamp = datetime.datetime.utcnow().isoformat()
    data.setdefault(email, {})[timestamp] = session_data
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
