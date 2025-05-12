import time
from machine import Pin, UART
import picoexplorer  # This is a library for PicoCalc's screen
import ustruct

# Stores the current typed command in the File Manager scene
command_input = ""

# === Setup PicoCalc Screen ===
# Initialize the screen and set it to a resolution of 240x240
screen = picoexplorer.get_screen()

# Menu navigation items
menu_items = ["App Launcher", "File Manager", "Settings (coming soon)"]
selected_index = 0
current_scene = "menu"  # Can be 'menu', 'file', 'app', or 'settings'

# === Key Mapping (simulating PicoCalc's keyboard input) ===
def get_keypress():
    # Check for keypresses on PicoCalc (replace with actual key checking method)
    key_map = {
        "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,
        "up": "up", "down": "down", "enter": "enter", "backspace": "backspace", "esc": "esc"
    }

    # Example simulation of input function (replace with PicoCalc-specific key check)
    key = None
    # Code to get actual key from PicoCalc's keypad should go here (via GPIO or UART)
    return key

# === Refresh screen ===
def update_screen():
    # Update the PicoCalc screen with the framebuffer
    screen.update()

# === Draw main menu ===
def draw_menu():
    screen.clear()  # Clear screen
    screen.set_pen(255, 255, 255)  # White color for text
    screen.text("Astralixi OS", 10, 5, scale=2)
    
    for i, item in enumerate(menu_items):
        prefix = ">" if i == selected_index else " "
        screen.text(prefix + item, 10, 30 + i * 20, scale=2)

# === File Manager Scene ===
def draw_file_manager(key):
    global command_input  # Allow modifying the global variable

    # Handle key input for the command line
    if isinstance(key, str):
        if key == "backspace":
            command_input = command_input[:-1]  # Remove last character
        elif key == "enter":
            # Placeholder: here is where you'd handle commands like "/new file type .txt"
            # For now we just clear the input to simulate handling
            command_input = ""
        elif len(key) == 1:
            command_input += key  # Add typed character

    screen.clear()  # Clear screen for redraw
    screen.set_pen(255, 255, 255)  # White color for text
    screen.text("File Manager", 10, 5, scale=2)

    # Command prompt at bottom
    screen.text("> " + command_input, 10, 220, scale=2)

    # Fake file list
    files = ["notes.txt", "notes1.txt", "notes2.txt", "apps/", "config.sys"]

    # Draw files with selection highlight
    for i, name in enumerate(files):
        prefix = ">" if i == selected_index else " "
        screen.text(prefix + name, 10, 30 + i * 20, scale=2)

    # Simulate opening a file (if Enter pressed while selecting)
    if key == "enter":
        selected_file = files[selected_index]
        screen.clear()
        screen.text(f"Opening {selected_file}...", 10, 30, scale=2)
        time.sleep(2)  # Simulate delay

    return "file"  # Stay in the file manager

# === MAIN LOOP ===
while True:
    key = get_keypress()  # Read keyboard input from PicoCalc

    # Global quit
    if key == "quit":
        break

    # === MENU ===
    if current_scene == "menu":
        draw_menu()
        if key == "up":
            selected_index = (selected_index - 1) % len(menu_items)
        elif key == "down":
            selected_index = (selected_index + 1) % len(menu_items)
        elif key == "enter":
            selected_option = menu_items[selected_index]
            if "App" in selected_option:
                current_scene = "app"
            elif "File" in selected_option:
                current_scene = "file"
            elif "Settings" in selected_option:
                current_scene = "settings"

    # === APP PLACEHOLDER ===
    elif current_scene == "app":
        screen.clear()
        screen.text("Launching App...", 10, 30, scale=2)

    # === FILE MANAGER ===
    elif current_scene == "file":
        current_scene = draw_file_manager(key)

    # === SETTINGS PLACEHOLDER ===
    elif current_scene == "settings":
        screen.clear()
        screen.text("Settings Coming Soon!", 10, 30, scale=2)

    # Shortcut to return to main menu
    if key == "esc":
        current_scene = "menu"

    update_screen()  # Refresh display
    time.sleep(0.1)  # Slight pause for performance
