import os
import re
import shutil
import subprocess


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
# REACT NATIVE / EXPO PROJECT CREATOR
# ============================================================

def create_reactnative_project(name):

    # --------------------------------------------------------
    # Validate project name
    # --------------------------------------------------------

    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        raise ValueError(
            "Project name may only contain letters, "
            "numbers, underscores, and hyphens."
        )

    project_directory = os.path.join(
        DEV_DIRECTORY,
        name,
    )

    if os.path.exists(project_directory):
        raise FileExistsError(
            f"Project already exists:\n{project_directory}"
        )

    os.makedirs(DEV_DIRECTORY, exist_ok=True)

    # --------------------------------------------------------
    # Commands
    # --------------------------------------------------------

    npx_command = (
        "npx.cmd"
        if os.name == "nt"
        else "npx"
    )

    npm_command = (
        "npm.cmd"
        if os.name == "nt"
        else "npm"
    )

    code_command = (
        "code.cmd"
        if os.name == "nt"
        else "code"
    )

    # --------------------------------------------------------
    # Check Node.js / npm
    # --------------------------------------------------------

    if not command_exists(npm_command):
        raise RuntimeError(
            "Node.js / npm was not found.\n\n"
            "Install Node.js before creating an Expo project."
        )

    if not command_exists(npx_command):
        raise RuntimeError(
            "npx was not found.\n\n"
            "Install Node.js before creating an Expo project."
        )

    # --------------------------------------------------------
    # Create Expo project
    # --------------------------------------------------------

    run_command(
        [
            npx_command,
            "create-expo-app@latest",
            name,
        ],
        cwd=DEV_DIRECTORY,
    )

    # --------------------------------------------------------
    # Install dependencies
    # --------------------------------------------------------

    run_command(
        [npm_command, "install"],
        cwd=project_directory,
    )

    # --------------------------------------------------------
    # Verify Expo project
    # --------------------------------------------------------

    package_json = os.path.join(
        project_directory,
        "package.json",
    )

    if not os.path.isfile(package_json):
        raise RuntimeError(
            "Expo project was created, but package.json "
            "was not found."
        )

    # --------------------------------------------------------
    # Git configuration
    # --------------------------------------------------------

    gitignore = """\
node_modules/

.expo/
.expo-shared/

dist/
web-build/

.env
.env.local
.env.*.local

.vscode/
.idea/

.DS_Store
Thumbs.db
"""

    write_file(
        os.path.join(
            project_directory,
            ".gitignore",
        ),
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
                    "Initial Expo project",
                ],
                cwd=project_directory,
            )
        except subprocess.CalledProcessError:
            # Git identity may not be configured.
            # Don't fail project creation because of it.
            pass

    # --------------------------------------------------------
    # Open VS Code
    # --------------------------------------------------------

    if command_exists(code_command):
        subprocess.Popen(
            [code_command, "."],
            cwd=project_directory,
        )

    print(
        f"Created React Native + Expo project:\n"
        f"{project_directory}"
    )

    return project_directory