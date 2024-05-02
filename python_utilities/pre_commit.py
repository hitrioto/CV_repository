import subprocess

def format_code_with_isort_and_black():
    # Define the commands as lists
    isort_command = ["isort", "."]
    black_command = ["black", ".", "--line-length", "120"]

    # Run isort
    print("Running isort...")
    result_isort = subprocess.run(isort_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result_isort.returncode == 0:
        print("isort completed successfully.")
        print(result_isort.stdout)
    else:
        print("isort failed:")
        print(result_isort.stderr)

    # Run black
    print("Running black...")
    result_black = subprocess.run(black_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result_black.returncode == 0:
        print("black completed successfully.")
        print(result_black.stdout)
    else:
        print("black failed:")
        print(result_black.stderr)

if __name__ == "__main__":
    format_code_with_isort_and_black()
