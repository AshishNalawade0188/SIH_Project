import pywhatkit as kit
import os
import time

# Path to the snapshot folder
snapshot_path = r"E:\Project\data\alerts"  # Folder containing snapshots

# WhatsApp configuration
receiver_numbers = ["7028481133", "9850715293"]  # List of receiver's phone numbers with country code
message = "Review of Public counting"

# Function to get the latest snapshot file in the folder
def get_latest_snapshot(folder_path):

    try:
        # Get all files in the folder
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            return None
        # Sort files by modification time (newest first)
        latest_file = max(files, key=os.path.getmtime)
        return latest_file
    except Exception as e:
        print(f"Error fetching the latest snapshot: {e}")
        return None

# Function to send WhatsApp alert with the latest image
def send_whatsapp_alert(snapshot_path):
    try:
        # Get the latest snapshot
        snapshot_file_path = get_latest_snapshot(snapshot_path)
        if not snapshot_file_path:
            print("No snapshot files found in the folder.")
            return

        print(f"Latest snapshot: {snapshot_file_path}")

        # Open WhatsApp Web in one tab and send the message to all receivers
        print("Sending WhatsApp message to multiple receivers...")
        for receiver_number in receiver_numbers:
            kit.sendwhatmsg_instantly(
                phone_no=f"+91{receiver_number}",
                message=message,
                wait_time=10,  # Wait time in seconds for WhatsApp Web to load
                tab_close=False  # Keep browser tab open
            )
            time.sleep(3)  # Slight delay before sending the next message to avoid multiple tab openings

        print("Message sent successfully!")

        # Send the image to all receivers in the same session
        for receiver_number in receiver_numbers:
            print(f"Sending snapshot to {receiver_number}...")
            kit.sendwhats_image(
                receiver=f"+91{receiver_number}",
                img_path=snapshot_file_path,
                caption="Snapshot for review."
            )
            time.sleep(3)  # Slight delay to prevent message flooding

        print("Snapshot sent successfully!")

    except Exception as e:
        print(f"Error sending WhatsApp alert: {e}")




