import subprocess

def run_formatter():
    print("Running isort...")
    subprocess.run(['isort', '.'], check=True)
    print("Running black...")
    subprocess.run(['black', '.', '--line-length=120'], check=True)

if __name__ == "__main__":
    run_formatter()