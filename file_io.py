import json


def save_markdown(task_output):
    data = json.loads(task_output.raw)
    with open("data.json", "w") as f:
        json.dump(data, f)
