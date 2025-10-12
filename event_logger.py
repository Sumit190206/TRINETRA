import pandas as pd
from datetime import datetime
import os

# Define log file
LOG_FILE = 'event_log.xlsx'

def log_event(event_type, person='Unknown'):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    data = {
        'Timestamp': [timestamp],
        'Event': [event_type],
        'Person': [person]
    }

    df = pd.DataFrame(data)

    if not os.path.exists(LOG_FILE):
        df.to_excel(LOG_FILE, index=False)
        print("✅ Log file created and event logged.")
    else:
        old = pd.read_excel(LOG_FILE)
        new = pd.concat([old, df], ignore_index=True)
        new.to_excel(LOG_FILE, index=False)
        print("✅ Event logged successfully.")

# ➕ Test the function
log_event("Motion Detected", "Unknown Person")
log_event("Face Recognized", "John Doe")

