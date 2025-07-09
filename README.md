# **HydroBuddy** 🚰

**HydroBuddy** is a simple yet effective hydration reminder application designed to help you stay hydrated throughout the day. It now features both a **graphical user interface (GUI)** and a **command-line interface (CLI)**. The application sends desktop notifications at regular intervals, plays a sound alert, and logs each reminder to a file.

---

## Features

✅ **GUI Mode**: Beautiful graphical interface with easy controls  
✅ **CLI Mode**: Traditional command-line operation  
✅ **Desktop Notifications**: Motivational messages to remind you to drink water  
✅ **Customizable Intervals**: Set your preferred reminder frequency  
✅ **Sound Alerts**: Plays a customizable sound alert (`MGS_Alert.mp3`)  
✅ **Activity Logging**: Records each reminder to a file (`hydration_log.txt`)  
✅ **System Tray Support**: Minimize to system tray (when available)  
✅ **Cross-Platform**: Works seamlessly on both **Linux** and **Windows**  
✅ **Manual Reminders**: Send immediate hydration reminders  
✅ **History Viewer**: View your hydration reminder history

---

## Project Structure

Here’s an overview of the key files in this project:

- [`hydrobuddy.py`](hydrobuddy.py): The main launcher script - choose between GUI and CLI modes
- [`gui.py`](gui.py): The graphical user interface implementation
- [`reminder.py`](reminder.py): Core reminder functionality (notifications, logging, sound)
- [`hydration_log.txt`](hydration_log.txt): A log file that records the timestamp of each reminder
- [`run_reminder.sh`](run_reminder.sh): Shell script to run the application (Linux/Mac)
- [`run_reminder.bat`](run_reminder.bat): Batch script to run the application (Windows)
- [`run_cli.sh`](run_cli.sh): Shell script to run CLI mode specifically (Linux/Mac)
- [`run_cli.bat`](run_cli.bat): Batch script to run CLI mode specifically (Windows)

---

## Requirements

Before running the application, ensure you have the following installed:

- **Python 3.x**
- **Dependencies**:
  - [`plyer`](https://github.com/kivy/plyer): For sending desktop notifications.
  - [`pygame`](https://www.pygame.org/): For playing sound alerts.
  - **For GUI mode** (optional):
    - [`tkinter`](https://docs.python.org/3/library/tkinter.html): For the graphical interface (usually included with Python)
    - [`pystray`](https://github.com/moses-palmer/pystray): For system tray support
    - [`Pillow`](https://python-pillow.org/): For image processing (tray icon)

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
Ensure you have a sound file named [`MGS_Alert.mp3`](MGS_Alert.mp3) in the same directory as [`reminder.py`](reminder.py). You can replace this file with any .mp3 file of your choice.

## Usage

HydroBuddy now offers two modes of operation:

### GUI Mode (Recommended)

Launch the graphical interface for the best user experience:

```bash
python hydrobuddy.py
# or explicitly
python hydrobuddy.py gui
```

**GUI Features:**
- 🎛️ **Easy Controls**: Start/stop reminders with a single click
- ⏰ **Custom Intervals**: Set reminder frequency from 1-120 minutes
- 📝 **History View**: See your past reminders in real-time
- 🔔 **Manual Reminders**: Send immediate hydration alerts
- ⚙️ **Settings Panel**: Customize messages and sound files
- 🔍 **System Tray**: Minimize to tray for unobtrusive operation

### CLI Mode (Traditional)

For users who prefer command-line operation:

```bash
python hydrobuddy.py cli
```

### Quick Start Scripts

#### On Linux/Mac:
```bash
./run_reminder.sh    # Launches GUI mode
./run_cli.sh         # Launches CLI mode
```

#### On Windows:
```bash
run_reminder.bat     # Launches GUI mode  
run_cli.bat          # Launches CLI mode
```

The application will notify you at your chosen intervals to remind you to drink water. A log file [`hydration_log.txt`] will track all reminders.

### Preview
Here’s what the notification looks like in action:
```markdown
## Preview
![Notification Preview](images/notification_preview.gif)
