#!/usr/bin/env python3
"""
HydroBuddy Launcher - Choose between GUI and CLI modes
"""

import sys
import os

def show_help():
    print("""
HydroBuddy - Hydration Reminder Application

Usage:
    python hydrobuddy.py [mode]

Modes:
    gui     - Launch the graphical user interface (default)
    cli     - Launch the command-line version
    help    - Show this help message

Examples:
    python hydrobuddy.py          # Launch GUI mode
    python hydrobuddy.py gui      # Launch GUI mode
    python hydrobuddy.py cli      # Launch CLI mode
    """)

def main():
    # Determine mode
    mode = "gui"  # Default to GUI
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["help", "-h", "--help"]:
            show_help()
            return
        elif arg == "cli":
            mode = "cli"
        elif arg == "gui":
            mode = "gui"
        else:
            print(f"Unknown mode: {arg}")
            show_help()
            return
    
    print(f"🚰 Starting HydroBuddy in {mode.upper()} mode...")
    
    if mode == "gui":
        try:
            import gui
            gui.main()
        except ImportError as e:
            print(f"Error: Could not import GUI module: {e}")
            print("Make sure tkinter is installed: sudo apt install python3-tk")
            print("Falling back to CLI mode...")
            mode = "cli"
        except Exception as e:
            print(f"Error starting GUI: {e}")
            print("Falling back to CLI mode...")
            mode = "cli"
    
    if mode == "cli":
        import reminder
        print("Starting command-line hydration reminders...")
        print("Press Ctrl+C to stop.")
        try:
            reminder.remind_to_drink()
        except KeyboardInterrupt:
            print("\nHydroBuddy stopped. Stay hydrated! 💧")

if __name__ == "__main__":
    main()