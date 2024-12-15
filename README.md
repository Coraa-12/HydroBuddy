# Hydration Reminder

This project is a simple hydration reminder application that sends notifications to remind you to drink water at regular intervals. It also logs each reminder to a file and plays a sound to alert you.

## Project Structure

- [`app.py`](app.py): The main application script that sends notifications, logs reminders, and plays a sound.
- [`hydration_log.txt`](hydration_log.txt): A log file that records the timestamp of each reminder.
- [`run_reminder.sh`](run_reminder.sh): A shell script to activate the virtual environment and run the application.

## Requirements

- Python 3.x
- [`plyer`](.venv/lib/python3.12/site-packages/plyer/__init__.py) library for notifications
- [`pygame`](.venv/lib/python3.12/site-packages/pygame/__init__.py) library for playing sound

## Setup

1. Create a virtual environment:

    ```sh
    python3 -m venv .venv
    ```

2. Activate the virtual environment:

    ```sh
    source .venv/bin/activate
    ```

3. Install the required libraries:

    ```sh
    pip install plyer pygame
    ```

4. Ensure you have a sound file named [MGS_Alert.mp3](http://_vscodecontentref_/3) in the same directory as [app.py](http://_vscodecontentref_/4).

## Usage

To run the hydration reminder application, execute the [run_reminder.sh](http://_vscodecontentref_/5) script:

```sh
./run_reminder.sh

