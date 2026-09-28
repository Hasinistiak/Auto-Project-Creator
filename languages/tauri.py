import os
import re
import subprocess
import shutil
import json


# ============================================================
# CONFIG
# ============================================================

DEV_DIRECTORY = os.path.join(os.path.expanduser("~"), "Dev")


# ============================================================
# HELPERS
# ============================================================

def command_exists(command):
    return shutil.which(command) is not None


def run_command(command, cwd=None):
    return subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
    )


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


# ============================================================
# TAURI PROJECT CREATOR
# ============================================================

def create_tauri_project(name):

    project_directory = os.path.join(DEV_DIRECTORY, name)

    npm_command = "npm.cmd" if os.name == "nt" else "npm"
    code_command = "code.cmd" if os.name == "nt" else "code"

    # --------------------------------------------------------
    # Validate project name
    # --------------------------------------------------------

    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        raise ValueError(
            "Project name may only contain letters, numbers, "
            "underscores, and hyphens."
        )

    if os.path.exists(project_directory):
        raise FileExistsError(
            f"Project already exists:\n{project_directory}"
        )

    os.makedirs(DEV_DIRECTORY, exist_ok=True)

    # --------------------------------------------------------
    # Check required tools
    # --------------------------------------------------------

    missing = []

    if not command_exists(npm_command):
        missing.append("Node.js / npm")

    if not command_exists("cargo"):
        missing.append("Rust / Cargo")

    if not command_exists("rustc"):
        missing.append("Rust compiler")

    if missing:
        raise RuntimeError(
            "Required tools are missing:\n\n"
            + "\n".join(f"• {item}" for item in missing)
            + "\n\nInstall the required development tools first."
        )

    # --------------------------------------------------------
    # Tauri application identifier
    # --------------------------------------------------------

    identifier = f"com.{name.lower()}.app"

    identifier = re.sub(
        r"[^a-z0-9.-]",
        "",
        identifier,
    )

    # --------------------------------------------------------
    # Create Tauri + React + JavaScript project
    # --------------------------------------------------------

    command = [
        npm_command,
        "create",
        "tauri-app@latest",
        name,
        "--",
        "--template",
        "react",
        "--manager",
        "npm",
        "--flavor",
        "javascript",
        "--identifier",
        identifier,
    ]

    run_command(
        command,
        cwd=DEV_DIRECTORY,
    )

    # --------------------------------------------------------
    # Install frontend dependencies
    # --------------------------------------------------------

    run_command(
        [npm_command, "install"],
        cwd=project_directory,
    )

    # --------------------------------------------------------
    # Verify Tauri configuration
    # --------------------------------------------------------

    tauri_directory = os.path.join(
        project_directory,
        "src-tauri",
    )

    if not os.path.isdir(tauri_directory):
        raise RuntimeError(
            "Tauri project was created, but src-tauri "
            "was not found."
        )

    # --------------------------------------------------------
    # Configure .gitignore
    # --------------------------------------------------------

    gitignore = """\
node_modules/
dist/
build/

src-tauri/target/

.env
.env.local
.env.*.local

.vscode/
.idea/

.DS_Store
Thumbs.db
"""

    write_file(
        os.path.join(project_directory, ".gitignore"),
        gitignore,
    )

    # --------------------------------------------------------
    # Initialize Git automatically
    # --------------------------------------------------------

    if command_exists("git"):
        run_command(
            ["git", "init"],
            cwd=project_directory,
        )

        run_command(
            ["git", "add", "."],
            cwd=project_directory,
        )

        try:
            run_command(
                [
                    "git",
                    "commit",
                    "-m",
                    "Initial project setup",
                ],
                cwd=project_directory,
            )
        except subprocess.CalledProcessError:
            # Git may not have a configured user identity.
            # Project creation itself should still succeed.
            pass

    # --------------------------------------------------------
    # Open project in VS Code
    # --------------------------------------------------------

    if command_exists(code_command):
        subprocess.Popen(
            [code_command, "."],
            cwd=project_directory,
        )

    print(
        f"Created Tauri + React project:\n"
        f"{project_directory}"
    )

    return project_directory