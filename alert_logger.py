import pandas as pd
from twilio.rest import Client
from datetime import datetime

# Your Twilio details here
account_sid = os.getenv("TWILIO_ACCOUNT_SID")

auth_token = '7a30785dedc4405555f34526b3905f02'
twilio_number = '+15109918299'
to_number = '+918080111951'

client = Client(account_sid, auth_token)

def send_sms(message):
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=to_number
        )
        print(f"✅ SMS sent! SID: {message.sid}")
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")

def log_event(event_message):
    log_file = 'event_log.xlsx'
    try:
        df = pd.read_excel(log_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Timestamp', 'Event'])

    new_event = {'Timestamp': datetime.now(), 'Event': event_message}
    df = pd.concat([df, pd.DataFrame([new_event])], ignore_index=True)

    df.to_excel(log_file, index=False)
    print("✅ Event logged successfully.")


# For testing standalone, you can uncomment below lines:
# if __name__ == "__main__":
#     send_sms("Test message from alert_logger")
#     log_event("Test event logged")
