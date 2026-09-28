
import os
import tkinter as tk
from tkinter import messagebox

from languages.python import create_py_project
from languages.react import create_react_project
from languages.rust import create_rust_project
from languages.tauri import create_tauri_project
from languages.cpp import create_cpp_project
from languages.reactnative import create_reactnative_project


# ============================================================
# CONFIG
# ============================================================

root = tk.Tk()
root.title("Project Creator")
root.geometry("430x500")
root.resizable(False, False)
root.configure(bg="#080808")

DEV_DIRECTORY = os.path.join(os.path.expanduser("~"), "Dev")
os.makedirs(DEV_DIRECTORY, exist_ok=True)


LANGUAGES = [
    "Python",
    "C++",
    "React",
    "React Native",
    "Rust",
    "Tauri",
]

PROJECT_CREATORS = {
    "Python": create_py_project,
    "C++": create_cpp_project,
    "React": create_react_project,
    "React Native": create_reactnative_project,
    "Rust": create_rust_project,
    "Tauri": create_tauri_project,
}


# ============================================================
# COLORS
# ============================================================

BG = "#080808"
PANEL = "#0D0D0D"
INPUT = "#111111"
BORDER = "#242424"
BORDER_ACTIVE = "#3A3A3A"

TEXT = "#F2F2F2"
MUTED = "#777777"
ACCENT = "#00D9FF"
ACCENT_DIM = "#007D94"

SUCCESS = "#00FF88"
ERROR = "#FF4D5F"


# ============================================================
# HELPERS
# ============================================================

def get_project_name():
    return entry1.get().strip()


def get_existing_projects():
    try:
        return {
            item.lower()
            for item in os.listdir(DEV_DIRECTORY)
            if os.path.isdir(os.path.join(DEV_DIRECTORY, item))
        }
    except OSError:
        return set()


def valid_project_name(name):
    if not name:
        return False

    invalid_chars = '<>:"/\\|?*'

    if any(char in name for char in invalid_chars):
        return False

    if name[-1] in (" ", "."):
        return False

    if not (name[0].isalpha() or name[0] == "_"):
        return False

    reserved = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }

    if name.upper() in reserved:
        return False

    return True


def show_status(text, color):
    button_frame.grid_remove()

    status_label.config(
        text=text.upper(),
        fg=color,
    )

    status_label.grid(
        row=0,
        column=0,
        padx=20,
        pady=(14, 0),
        sticky="w",
    )


# ============================================================
# PROJECT CREATION
# ============================================================

def create_project():
    name = get_project_name()
    language = selected_lang.get()

    if not name:
        return

    name = name.lower()

    if not valid_project_name(name):
        show_status("Name Not Possible", ERROR)
        return

    if name in get_existing_projects():
        show_status("Name Exists", ERROR)
        return

    creator = PROJECT_CREATORS.get(language)

    if creator is None:
        show_status("Unsupported Language", ERROR)
        return

    try:
        print(f"Creating {language} project...")
        print(f"Project: {name}")
        print(f"Directory: {DEV_DIRECTORY}")

        creator(name)

        print("Initialized Project")

        show_status("Project Initialized", SUCCESS)

        root.after(700, root.destroy)

    except Exception as error:
        print(f"Project creation failed: {error}")

        show_status("Creation Failed", ERROR)

        messagebox.showerror(
            "Project Creation Failed",
            str(error),
        )


# ============================================================
# UI STATE
# ============================================================

def update_button_state(*args):
    name = get_project_name()

    button_frame.grid_remove()
    status_label.grid_remove()

    if not name:
        return

    if not valid_project_name(name):
        show_status("Name Not Possible", ERROR)
        return

    if name.lower() in get_existing_projects():
        show_status("Name Exists", ERROR)
        return

    button_frame.grid(
        row=0,
        column=0,
        padx=20,
        pady=(14, 0),
        sticky="ew",
    )


def select_all(event=None):
    entry1.select_range(0, tk.END)
    return "break"


# ============================================================
# MAIN CONTAINER
# ============================================================

outer = tk.Frame(
    root,
    bg=BG,
)

outer.pack(
    fill="both",
    expand=True,
    padx=24,
    pady=24,
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    outer,
    bg=BG,
)

header.pack(
    fill="x",
    pady=(4, 28),
)


brand = tk.Label(
    header,
    text="PROJECT / CREATOR",
    font=("Consolas", 9, "bold"),
    bg=BG,
    fg=ACCENT,
)

brand.pack(anchor="w")


title = tk.Label(
    header,
    text="Initialize Project",
    font=("Segoe UI", 24, "bold"),
    bg=BG,
    fg=TEXT,
)

title.pack(
    anchor="w",
    pady=(7, 0),
)


subtitle = tk.Label(
    header,
    text="Create a new workspace inside ~/Dev",
    font=("Consolas", 9),
    bg=BG,
    fg=MUTED,
)

subtitle.pack(
    anchor="w",
    pady=(7, 0),
)


# ============================================================
# PROJECT NAME
# ============================================================

name_section = tk.Frame(
    outer,
    bg=BG,
)

name_section.pack(
    fill="x",
)


name_label = tk.Label(
    name_section,
    text="PROJECT NAME",
    font=("Consolas", 9, "bold"),
    bg=BG,
    fg=MUTED,
)

name_label.pack(
    anchor="w",
    pady=(0, 8),
)


# Input border
entry_border = tk.Frame(
    name_section,
    bg=BORDER,
    height=52,
)

entry_border.pack(
    fill="x",
)

entry_border.pack_propagate(False)


entry1 = tk.Entry(
    entry_border,
    font=("Consolas", 14),
    bg=INPUT,
    fg=TEXT,
    insertbackground=ACCENT,
    selectbackground=ACCENT_DIM,
    selectforeground=TEXT,
    relief="flat",
    borderwidth=0,
)

entry1.pack(
    fill="both",
    expand=True,
    padx=14,
    pady=1,
)


# ============================================================
# LANGUAGE
# ============================================================

language_section = tk.Frame(
    outer,
    bg=BG,
)

language_section.pack(
    fill="x",
    pady=(25, 0),
)


language_label = tk.Label(
    language_section,
    text="RUNTIME / FRAMEWORK",
    font=("Consolas", 9, "bold"),
    bg=BG,
    fg=MUTED,
)

language_label.pack(
    anchor="w",
    pady=(0, 8),
)


selected_lang = tk.StringVar(
    value=LANGUAGES[0]
)


language_border = tk.Frame(
    language_section,
    bg=BORDER,
    height=52,
)

language_border.pack(
    fill="x",
)

language_border.pack_propagate(False)


entry2 = tk.OptionMenu(
    language_border,
    selected_lang,
    *LANGUAGES,
)

entry2.config(
    font=("Consolas", 12),
    bg=INPUT,
    fg=TEXT,
    activebackground=INPUT,
    activeforeground=ACCENT,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    anchor="w",
)

entry2["menu"].config(
    font=("Consolas", 11),
    bg="#111111",
    fg=TEXT,
    activebackground="#1A1A1A",
    activeforeground=ACCENT,
    borderwidth=0,
    relief="flat",
)

entry2.pack(
    fill="both",
    expand=True,
    padx=5,
    pady=1,
)


# ============================================================
# STATUS / ACTION
# ============================================================

action_area = tk.Frame(
    outer,
    bg=BG,
)

action_area.pack(
    fill="x",
    pady=(28, 0),
)


button_frame = tk.Frame(
    action_area,
    bg=BG,
)


button = tk.Button(
    button_frame,
    text="INITIALIZE  →",
    font=("Consolas", 11, "bold"),
    command=create_project,
    bg=ACCENT,
    fg="#001014",
    activebackground="#55E8FF",
    activeforeground="#001014",
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    cursor="hand2",
)

button.pack(
    fill="x",
    ipady=13,
)


status_label = tk.Label(
    action_area,
    font=("Consolas", 10, "bold"),
    bg=BG,
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Frame(
    outer,
    bg=BG,
)

footer.pack(
    side="bottom",
    fill="x",
)


footer_line = tk.Frame(
    footer,
    bg=BORDER,
    height=1,
)

footer_line.pack(
    fill="x",
)


footer_content = tk.Frame(
    footer,
    bg=BG,
)

footer_content.pack(
    fill="x",
    pady=(12, 0),
)


path_label = tk.Label(
    footer_content,
    text="TARGET",
    font=("Consolas", 8, "bold"),
    bg=BG,
    fg=MUTED,
)

path_label.pack(
    side="left",
)


path_value = tk.Label(
    footer_content,
    text="~/Dev",
    font=("Consolas", 8),
    bg=BG,
    fg="#555555",
)

path_value.pack(
    side="right",
)


# ============================================================
# EVENTS
# ============================================================

entry1.bind(
    "<KeyRelease>",
    update_button_state,
)

entry1.bind(
    "<Return>",
    lambda event: create_project(),
)

entry1.bind(
    "<Control-a>",
    select_all,
)

selected_lang.trace_add(
    "write",
    update_button_state,
)


# ============================================================
# START
# ============================================================

entry1.focus_set()
update_button_state()

root.mainloop()

