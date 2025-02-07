# **HydroBuddy** 🚰

**HydroBuddy** is a simple yet effective hydration reminder application designed to help you stay hydrated throughout the day. It sends desktop notifications at regular intervals, plays a sound alert, and logs each reminder to a file.

---

## Features

✅ Sends desktop notifications with motivational messages to remind you to drink water.  
✅ Plays a customizable sound alert (`MGS_Alert.mp3`) to grab your attention.  
✅ Logs each reminder to a file (`hydration_log.txt`) for tracking your hydration habits.  
✅ Works seamlessly on both **Linux** and **Windows**.

---

## Project Structure

Here’s an overview of the key files in this project:

- [`app.py`](app.py): The main application script responsible for sending notifications, logging reminders, and playing sound alerts.
- [`hydration_log.txt`](hydration_log.txt): A log file that records the timestamp of each reminder.
- [`run_reminder.sh`](run_reminder.sh): A shell script to activate the virtual environment and run the application (for Linux/Mac users).
- [`run_reminder.bat`](run_reminder.bat): A batch script to run the application on Windows.

---

## Requirements

Before running the application, ensure you have the following installed:

- **Python 3.x**
- **Dependencies**:
  - [`plyer`](https://github.com/kivy/plyer): For sending desktop notifications.
  - [`pygame`](https://www.pygame.org/): For playing sound alerts.

You can install the required libraries using the `requirements.txt` file.

---

## Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/HydroBuddy.git
cd HydroBuddy
```

---

### Step 2: Create and Activate a Virtual Environment

### On Linux/Mac:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### On Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## Step 3: Install Dependencies
Install the required libraries using pip:
```bash
pip install -r requirements.txt
```

---

## Step 4: Add the Sound File
Ensure you have a sound file named [`MGS_Alert.mp3`](MGS_Alert.mp3) in the same directory as [`app.py`](app.py) You can replace this file with any .mp3 file of your choice.

## Usage
### Running the Application
### On Linux/Mac:
```bash
./run_reminder.sh
```

### On Windows:
```bash
run_reminder.bat
```

The application will notify you every 15 minutes to remind you to drink water. A log file [`hydration_log.txt`] will track all reminders.

### Preview
Here’s what the notification looks like in action:
```markdown
## Preview
![Notification Preview](images/notification_preview.gif)
