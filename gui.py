#!/usr/bin/env python3
"""
HydroBuddy GUI - A graphical interface for the hydration reminder application.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import os
from datetime import datetime
import reminder

# Optional system tray support
try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
except Exception:
    # Handle other platform-specific issues
    TRAY_AVAILABLE = False

class HydroBuddyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HydroBuddy - Hydration Reminder")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Application state
        self.is_running = False
        self.reminder_thread = None
        self.reminder_interval = 15 * 60  # 15 minutes in seconds
        self.custom_messages = []
        self.minimized_to_tray = False
        self.tray_icon = None
        
        # Set up the GUI
        self.setup_gui()
        self.load_log_history()
        
        # Set up system tray if available
        try:
            if TRAY_AVAILABLE:
                self.setup_tray()
        except Exception as e:
            print(f"System tray not available: {e}")
            # Note: Can't modify global from here, but that's ok
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui(self):
        """Set up the main GUI interface."""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🚰 HydroBuddy", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="Reminder Status:").grid(row=0, column=0, sticky=tk.W)
        self.status_label = ttk.Label(status_frame, text="Stopped", foreground="red")
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(status_frame, text="Reminders Sent:").grid(row=1, column=0, sticky=tk.W)
        self.count_label = ttk.Label(status_frame, text="0")
        self.count_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(status_frame, text="Next Reminder:").grid(row=2, column=0, sticky=tk.W)
        self.next_reminder_label = ttk.Label(status_frame, text="Not scheduled")
        self.next_reminder_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # Control section
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(1, weight=1)
        
        # Start/Stop button
        self.start_stop_btn = ttk.Button(control_frame, text="Start Reminders", command=self.toggle_reminders)
        self.start_stop_btn.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Interval setting
        ttk.Label(control_frame, text="Reminder Interval (minutes):").grid(row=1, column=0, sticky=tk.W)
        self.interval_var = tk.StringVar(value="15")
        interval_spinbox = ttk.Spinbox(control_frame, from_=1, to=120, textvariable=self.interval_var, width=10)
        interval_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        interval_spinbox.bind('<FocusOut>', self.update_interval)
        
        # Manual reminder button
        manual_btn = ttk.Button(control_frame, text="Send Reminder Now", command=self.send_manual_reminder)
        manual_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Reminder History", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Create log text widget with scrollbar
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        refresh_btn = ttk.Button(buttons_frame, text="Refresh Log", command=self.load_log_history)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(buttons_frame, text="Clear Log", command=self.clear_log)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        settings_btn = ttk.Button(buttons_frame, text="Settings", command=self.open_settings)
        settings_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        if TRAY_AVAILABLE:
            minimize_btn = ttk.Button(buttons_frame, text="Minimize to Tray", command=self.minimize_to_tray)
            minimize_btn.pack(side=tk.LEFT)
    
    def toggle_reminders(self):
        """Start or stop the reminder system."""
        if self.is_running:
            self.stop_reminders()
        else:
            self.start_reminders()
    
    def start_reminders(self):
        """Start the reminder system."""
        self.is_running = True
        self.start_stop_btn.config(text="Stop Reminders")
        self.status_label.config(text="Running", foreground="green")
        
        # Update interval from GUI
        self.update_interval()
        
        # Start reminder thread
        self.reminder_thread = threading.Thread(target=self.reminder_loop, daemon=True)
        self.reminder_thread.start()
        
        self.update_next_reminder_time()
    
    def stop_reminders(self):
        """Stop the reminder system."""
        self.is_running = False
        self.start_stop_btn.config(text="Start Reminders")
        self.status_label.config(text="Stopped", foreground="red")
        self.next_reminder_label.config(text="Not scheduled")
    
    def reminder_loop(self):
        """Main reminder loop running in a separate thread."""
        while self.is_running:
            self.send_reminder()
            
            # Sleep in small intervals to allow for interruption
            sleep_time = 0
            while sleep_time < self.reminder_interval and self.is_running:
                time.sleep(1)
                sleep_time += 1
                
                # Update next reminder time every 10 seconds
                if sleep_time % 10 == 0:
                    self.root.after(0, self.update_next_reminder_time)
    
    def send_reminder(self):
        """Send a hydration reminder."""
        reminder.reminder_count += 1
        message = reminder.get_random_message()
        
        # Send notification
        try:
            reminder.notification.notify(
                title=f"Hydration Reminder {reminder.reminder_count}",
                message=message,
                app_name="HydroBuddy",
                timeout=10
            )
        except Exception as e:
            print(f"Notification error: {e}")
        
        # Log the reminder
        reminder.log_reminder()
        
        # Play sound
        try:
            reminder.play_sound()
        except Exception as e:
            print(f"Sound error: {e}")
        
        # Update GUI
        self.root.after(0, self.update_reminder_count)
        self.root.after(0, self.load_log_history)
    
    def send_manual_reminder(self):
        """Send a manual reminder immediately."""
        if not self.is_running:
            # Send reminder without affecting the counter or timing
            message = reminder.get_random_message()
            try:
                reminder.notification.notify(
                    title="Manual Hydration Reminder",
                    message=message,
                    app_name="HydroBuddy",
                    timeout=10
                )
                reminder.play_sound()
            except Exception as e:
                messagebox.showerror("Error", f"Could not send reminder: {e}")
        else:
            # If running, send a scheduled reminder now
            threading.Thread(target=self.send_reminder, daemon=True).start()
    
    def update_interval(self, event=None):
        """Update the reminder interval from the GUI."""
        try:
            minutes = int(self.interval_var.get())
            if minutes < 1:
                minutes = 1
                self.interval_var.set("1")
            elif minutes > 120:
                minutes = 120
                self.interval_var.set("120")
            
            self.reminder_interval = minutes * 60
            self.update_next_reminder_time()
        except ValueError:
            self.interval_var.set("15")
            self.reminder_interval = 15 * 60
    
    def update_reminder_count(self):
        """Update the reminder count display."""
        self.count_label.config(text=str(reminder.reminder_count))
    
    def update_next_reminder_time(self):
        """Update the next reminder time display."""
        if self.is_running:
            next_time = datetime.now().timestamp() + self.reminder_interval
            next_time_str = datetime.fromtimestamp(next_time).strftime("%H:%M:%S")
            self.next_reminder_label.config(text=next_time_str)
    
    def load_log_history(self):
        """Load and display the reminder history from the log file."""
        log_file_path = os.path.join(os.path.dirname(__file__), "hydration_log.txt")
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        
        try:
            if os.path.exists(log_file_path):
                with open(log_file_path, "r") as log_file:
                    lines = log_file.readlines()
                    # Show last 50 entries
                    for line in lines[-50:]:
                        self.log_text.insert(tk.END, line)
                
                # Scroll to the bottom
                self.log_text.see(tk.END)
            else:
                self.log_text.insert(tk.END, "No log file found. Start sending reminders to create one.\n")
        except Exception as e:
            self.log_text.insert(tk.END, f"Error reading log file: {e}\n")
        
        self.log_text.config(state=tk.DISABLED)
    
    def clear_log(self):
        """Clear the reminder log file."""
        if messagebox.askyesno("Clear Log", "Are you sure you want to clear the reminder history?"):
            log_file_path = os.path.join(os.path.dirname(__file__), "hydration_log.txt")
            try:
                if os.path.exists(log_file_path):
                    os.remove(log_file_path)
                self.load_log_history()
                messagebox.showinfo("Success", "Log cleared successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not clear log: {e}")
    
    def open_settings(self):
        """Open the settings window."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("HydroBuddy Settings")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        
        # Make window modal
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        frame = ttk.Frame(settings_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Sound file selection
        ttk.Label(frame, text="Sound File:").pack(anchor=tk.W)
        sound_frame = ttk.Frame(frame)
        sound_frame.pack(fill=tk.X, pady=(0, 10))
        
        current_sound = os.path.join(os.path.dirname(__file__), "MGS_Alert.mp3")
        sound_label = ttk.Label(sound_frame, text=os.path.basename(current_sound))
        sound_label.pack(side=tk.LEFT)
        
        def choose_sound():
            filename = filedialog.askopenfilename(
                title="Choose Sound File",
                filetypes=[("Audio files", "*.mp3 *.wav *.ogg")]
            )
            if filename:
                sound_label.config(text=os.path.basename(filename))
        
        ttk.Button(sound_frame, text="Browse", command=choose_sound).pack(side=tk.RIGHT)
        
        # Custom messages
        ttk.Label(frame, text="Custom Messages (one per line):").pack(anchor=tk.W, pady=(10, 0))
        
        messages_text = scrolledtext.ScrolledText(frame, height=8)
        messages_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Load current messages
        current_messages = "\n".join(reminder.get_random_message.__defaults__[0] if hasattr(reminder.get_random_message, '__defaults__') else [
            "Stay hydrated! Drink some water! 💧",
            "Your body needs water! Drink up! 🌊",
            "Don't forget to hydrate, it's important! 💦",
            "Drink water, it's great for your skin and energy! ✨",
            "Time to hydrate! Your body will thank you! 😄"
        ])
        messages_text.insert(tk.END, current_messages)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        def save_settings():
            # Note: This is a placeholder for settings functionality
            # In a more complete implementation, you'd save these settings
            messagebox.showinfo("Settings", "Settings saved! (Note: Custom messages and sound changes require restart)")
            settings_window.destroy()
        
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Save", command=save_settings).pack(side=tk.RIGHT, padx=(0, 10))
    
    def on_closing(self):
        """Handle application closing."""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Reminders are still running. Do you want to quit?"):
                self.stop_reminders()
                if self.tray_icon:
                    self.tray_icon.stop()
                self.root.destroy()
        else:
            if self.tray_icon:
                self.tray_icon.stop()
            self.root.destroy()

    def setup_tray(self):
        """Set up the system tray icon."""
        if not TRAY_AVAILABLE:
            return
        
        # Create a simple icon
        def create_icon():
            width = 64
            height = 64
            image = Image.new('RGB', (width, height), color='lightblue')
            dc = ImageDraw.Draw(image)
            dc.text((10, 20), "💧", fill='blue')
            return image
        
        # Create tray menu
        def show_window(icon, item):
            self.root.after(0, self.restore_from_tray)
        
        def quit_app(icon, item):
            self.root.after(0, self.on_closing)
        
        def toggle_reminders(icon, item):
            self.root.after(0, self.toggle_reminders)
        
        menu = pystray.Menu(
            pystray.MenuItem("Show HydroBuddy", show_window, default=True),
            pystray.MenuItem("Toggle Reminders", toggle_reminders),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", quit_app)
        )
        
        self.tray_icon = pystray.Icon("HydroBuddy", create_icon(), "HydroBuddy - Hydration Reminder", menu)

    def minimize_to_tray(self):
        """Minimize the application to the system tray."""
        if not TRAY_AVAILABLE or self.minimized_to_tray:
            return
        
        self.root.withdraw()
        self.minimized_to_tray = True
        
        # Start the tray icon in a separate thread
        def run_tray():
            self.tray_icon.run()
        
        tray_thread = threading.Thread(target=run_tray, daemon=True)
        tray_thread.start()

    def restore_from_tray(self):
        """Restore the application from the system tray."""
        if not self.minimized_to_tray:
            return
        
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.minimized_to_tray = False
        
        if self.tray_icon:
            self.tray_icon.stop()


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = HydroBuddyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()