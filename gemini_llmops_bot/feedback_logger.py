import json
from datetime import datetime

def log_feedback(question, response, rating):
    feedback = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "response": response,
        "rating": rating
    }

    with open("feedback_log.json", "a") as f:
        f.write(json.dumps(feedback) + "\n")
