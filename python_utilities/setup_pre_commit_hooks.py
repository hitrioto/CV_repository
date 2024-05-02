import os
import subprocess
import sys


def install_dependencies():
    subprocess.run([sys.executable, "-m", "pip", "install", "isort", "black"], check=True)


def setup_pre_commit_hook(script_path):
    git_dir = subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, text=True).stdout.strip()
    hook_path = os.path.join(git_dir, "hooks", "pre-commit")
    hook_content = f"""#!/bin/sh
python {script_path}
if [ $? -ne 0 ]; then
  echo "Code formatting check failed. Commit aborted."
  exit 1
fi
"""

    with open(hook_path, "w") as hook_file:
        hook_file.write(hook_content)
    os.chmod(hook_path, 0o755)
    print(f"Pre-commit hook installed at {hook_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup_pre_commit_hook.py <path_to_format_code_script>")
        print("Should enter the second argument. Exiting now.")
        sys.exit(1)
    script_path = sys.argv[1]
    install_dependencies()
    setup_pre_commit_hook(script_path)
    print("Pre-commit hooks setup finished.")
