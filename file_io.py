import json

def save_markdown(task_output):
    print(f"Raw task output: {task_output.raw}")
    if not task_output.raw:
        print("Error: task_output.raw is empty.")
        return None
    
    try:
        data = json.loads(task_output.raw)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)  # Add indent for readability
    