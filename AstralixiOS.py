import time
import sys
import select
import tty
import termios

# Simulated framebuf for desktop testing
class FakeFrameBuffer:
    def __init__(self):
        self.buffer = []

    def fill(self, color):
        self.buffer.clear()  # Clear the buffer (screen)

    def text(self, text, x, y, color):
        self.buffer.append((x, y, text))  # Add text to the buffer

    def render(self):
        print("\033c", end="")  # Clear terminal
        for x, y, text in self.buffer:
            print(f"[{y}px] {text}")  # Display the buffer content

# Simulated display for testing (replaces Pico display code)
class FakeDisplay:
    def blit(self, buffer, x, y):
        pass  # Not needed for simulation

    def show(self):
        fb.render()  # Render the frame buffer content

# === DISPLAY SETUP ===
width = 312
height = 312
fb = FakeFrameBuffer()
display = FakeDisplay()

menu_items = ["App Launcher", "File Manager", "Settings (coming soon)"]
selected_index = 0
current_scene = "menu"

# === INPUT SETUP ===
def get_keypress(timeout=0.1):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # Escape key
                next1 = sys.stdin.read(1)
                if next1 == '\r':
                    return "alt_enter"
                elif next1 == '[':
                    next2 = sys.stdin.read(1)
                    if next2 == 'A':
                        return "up"
                    elif next2 == 'B':
                        return "down"
            elif ch == '\r':
                return "enter"
            elif ch == 'w':
                return "up"
            elif ch == 's':
                return "down"
            elif ch == 'q':
                return "quit"
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

# === SCENE FUNCTIONS ===

def update_screen():
    display.blit(fb.buffer, 0, 0)
    display.show()

def draw_menu():
    fb.fill(0)  # Clear screen
    fb.text("Astralixi OS", 10, 5, 1)
    for i, item in enumerate(menu_items):
        prefix = ">" if i == selected_index else " "
        fb.text(prefix + item, 10, 20 + i * 10, 1)

# Updated File Manager with selection and file opening functionality
def draw_file_manager(key):
    fb.fill(0)  # Clear screen
    fb.text("File Manager", 10, 5, 1)

    # List of files (this could be dynamic in a real OS)
    files = ["notes.txt", "notes1.txt", "notes2.txt", "apps/", "config.sys"]

    # Loop through the files and display them
    for i, name in enumerate(files):
        prefix = ">" if i == selected_index else " "  # Highlight the selected file
        fb.text(prefix + name, 10, 20 + i * 10, 1)

    # If the user presses Enter, simulate "opening" the file
    if key == "enter":
        selected_file = files[selected_index]
        fb.fill(0)
        fb.text(f"Opening {selected_file}...", 10, 30, 1)
        time.sleep(2)  # Simulate file opening by pausing for a moment

    return "file"  # Stay in file manager if no key is pressed

# === MAIN LOOP ===
while True:
    key = get_keypress()  # Get user input

    if key == "quit":
        break  # Exit the program

    if current_scene == "menu":
        draw_menu()  # Display menu
        if key == "up":
            selected_index = (selected_index - 1) % len(menu_items)  # Move up
        elif key == "down":
            selected_index = (selected_index + 1) % len(menu_items)  # Move down
        elif key == "enter":
            selected_option = menu_items[selected_index]
            if "App" in selected_option:
                current_scene = "app"
            elif "File" in selected_option:
                current_scene = "file"
            elif "Settings" in selected_option:
                current_scene = "settings"

    elif current_scene == "app":
        fb.fill(0)
        fb.text("Launching App...", 10, 30, 1)

    elif current_scene == "file":
        # Draw the file manager and handle file opening
        current_scene = draw_file_manager(key)

    elif current_scene == "settings":
        fb.fill(0)
        fb.text("Settings Coming Soon!", 10, 30, 1)

    if key == "alt_enter":
        current_scene = "menu"  # Go back to the menu

    update_screen()  # Refresh the display after drawing
    time.sleep(0.1)  # Small delay to avoid overloading CPU
