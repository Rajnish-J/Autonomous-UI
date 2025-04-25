import os

# List to collect logs
execution_logs = []

# Define the log file path
def get_log_file_path():
    agent_folder = os.path.dirname(__file__)
    log_file_path = os.path.join(agent_folder, "..", "execution_logs.txt")
    return log_file_path

# Add a log message to the execution_logs list
def add_log(log_message):
    execution_logs.append(log_message)

# Write all collected logs to a text file
def write_logs_to_file():
    log_file_path = get_log_file_path()
    try:
        with open(log_file_path, "a") as log_file:
            log_file.write("\n".join(execution_logs) + "\n")
        print("✅ Logs appended to execution_logs.txt.")
    except Exception as e:
        print(f"❌ Failed to write to log file: {str(e)}")